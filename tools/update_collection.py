#!/usr/bin/env python3
"""Update a collection to the latest alexandria state.

Detects local modifications and prompts the user before overwriting files they
may have customized. The manifest at {collection}/.alexandria-manifest.yaml
records what was installed so local changes can be distinguished from upstream
changes on the next update.

Invocation:
    python tools/update_collection.py <collection_path>
    python tools/update_collection.py <collection_path> --dry-run
    python tools/update_collection.py <collection_path> --init

--init is used by coll-build-new-collection after copying files into a fresh
collection; it records the manifest and does not run uv sync or regenerate the
wiki.

See docs/guides/troubleshooting.md for the error-anchor targets.
"""

from __future__ import annotations

import argparse
import datetime
import difflib
import hashlib
import os
import subprocess
import sys
from pathlib import Path

import yaml

SCHEMA_VERSION = 1
MANIFEST_FILENAME = ".alexandria-manifest.yaml"
BACKUP_DIR = ".alexandria-backups"
TROUBLESHOOTING = "docs/guides/troubleshooting.md"

# Files and directories that should never be tracked even if they live under
# a managed directory. Ephemeral / tool-generated artifacts only; anything a
# human would reasonably edit does not belong here.
EXCLUDE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}
EXCLUDE_FILE_NAMES = {".DS_Store", "Thumbs.db"}


def _is_excluded(rel: Path) -> bool:
    if rel.name in EXCLUDE_FILE_NAMES:
        return True
    if rel.suffix in EXCLUDE_SUFFIXES:
        return True
    for part in rel.parts:
        if part in EXCLUDE_DIR_NAMES:
            return True
    return False


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_stamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def repo_commit(repo: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def print_error(what: str, details: str, what_to_do: str, anchor: str) -> None:
    """Plain-English message first, then details, then action, then docs link."""
    print(f"\n{what}\n", file=sys.stderr)
    print(f"  Details: {details}", file=sys.stderr)
    print(f"  What to do: {what_to_do}", file=sys.stderr)
    print(f"  More info: {TROUBLESHOOTING}#{anchor}\n", file=sys.stderr)


def expand_managed_paths(repo: Path) -> list[Path]:
    """Read tools/managed-paths.yaml and return a sorted list of relative
    file paths (directories expanded recursively)."""
    cfg = repo / "tools" / "managed-paths.yaml"
    if not cfg.is_file():
        print_error(
            "I can't find the list of files alexandria manages.",
            f"expected {cfg} to exist in the alexandria repo.",
            "make sure you're running this from an alexandria repo that has "
            "tools/managed-paths.yaml.",
            "managed-paths-missing",
        )
        sys.exit(2)
    with cfg.open() as f:
        data = yaml.safe_load(f) or {}
    paths = data.get("paths", []) or []
    result: set[Path] = set()
    for raw in paths:
        if raw.endswith("/"):
            base = repo / raw.rstrip("/")
            if base.is_dir():
                for f in base.rglob("*"):
                    if f.is_file():
                        rel = f.relative_to(repo)
                        if not _is_excluded(rel):
                            result.add(rel)
        else:
            rel = Path(raw)
            if (repo / rel).is_file() and not _is_excluded(rel):
                result.add(rel)
    return sorted(result)


def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.is_file():
        return {}
    try:
        with manifest_path.open() as f:
            data = yaml.safe_load(f)
        return data or {}
    except yaml.YAMLError as e:
        backup = manifest_path.with_name(
            f"{manifest_path.name}.corrupted-{now_stamp()}"
        )
        manifest_path.rename(backup)
        print_error(
            "I can't read your collection's manifest file — it may be damaged "
            "or from a newer version of alexandria than this one.",
            f"YAML parse error: {e}",
            f"the damaged file has been moved to {backup.name} for reference. "
            "Re-run the update; the manifest will be rebuilt from scratch and "
            "every file will be surfaced for your decision (a one-time event).",
            "manifest-corrupted",
        )
        return {}


def save_manifest(manifest_path: Path, manifest: dict) -> None:
    """Atomic write via temp file + rename."""
    tmp = manifest_path.with_name(manifest_path.name + ".tmp")
    with tmp.open("w") as f:
        yaml.safe_dump(
            manifest,
            f,
            default_flow_style=False,
            sort_keys=True,
            allow_unicode=True,
        )
    tmp.replace(manifest_path)


def atomic_copy(src: Path, dst: Path) -> None:
    """Write dst atomically: write to tempfile, then rename."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".tmp")
    tmp.write_bytes(src.read_bytes())
    tmp.replace(dst)


def atomic_write(dst: Path, content: bytes) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".tmp")
    tmp.write_bytes(content)
    tmp.replace(dst)


def backup_file(backup_dir: Path, rel_path: Path, content: bytes, suffix: str) -> Path:
    """Save content to backup_dir/{rel_path}.{suffix}. Creates directories."""
    dst = backup_dir / f"{rel_path}.{suffix}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(content)
    return dst


def classify(
    rel_path: Path,
    repo: Path,
    collection: Path,
    manifest: dict,
) -> tuple[str, dict]:
    """Classify a single managed path. Returns (state, info)."""
    upstream = repo / rel_path
    local = collection / rel_path

    upstream_sha = sha256_file(upstream)
    local_sha = sha256_file(local)
    manifest_entry = manifest.get("files", {}).get(str(rel_path), {})
    installed_sha = manifest_entry.get("sha256")

    info = {
        "upstream_sha": upstream_sha,
        "local_sha": local_sha,
        "installed_sha": installed_sha,
        "manifest_entry": manifest_entry,
    }

    # 1. Missing locally, present upstream: NEW
    if local_sha is None:
        return ("NEW", info)
    # 2. local == upstream: UNCHANGED regardless of manifest (self-heals
    #    interrupted updates: files already match upstream get silently
    #    reconciled)
    if local_sha == upstream_sha:
        return ("UNCHANGED", info)
    # 3. File present locally but not in manifest: UNMANAGED_CONFLICT
    if installed_sha is None:
        return ("UNMANAGED_CONFLICT", info)
    # 4. local == installed, upstream changed
    if local_sha == installed_sha:
        return ("UPSTREAM_ONLY", info)
    # 5. upstream == installed, local changed
    if upstream_sha == installed_sha:
        return ("LOCAL_ONLY", info)
    # 6. All three differ
    return ("BOTH_CHANGED", info)


def show_diff(left: Path, right: Path, left_label: str, right_label: str) -> None:
    left_lines = left.read_text().splitlines(keepends=True) if left.is_file() else []
    right_lines = (
        right.read_text().splitlines(keepends=True) if right.is_file() else []
    )
    diff = difflib.unified_diff(
        left_lines,
        right_lines,
        fromfile=f"{left} ({left_label})",
        tofile=f"{right} ({right_label})",
    )
    text = "".join(diff)
    if not text:
        print("(no differences)")
        return
    _page(text)


def show_upstream_changes(rel_path: Path, info: dict, repo: Path) -> None:
    """Show diff between the upstream version at last install and current upstream."""
    commit = info["manifest_entry"].get("installed_from_commit")
    if not commit:
        print(
            "(No record of which alexandria version this file was installed from, "
            "so I can't show the upstream-only diff.)"
        )
        return
    try:
        old = subprocess.run(
            ["git", "-C", str(repo), "show", f"{commit}:{rel_path}"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError:
        print_error(
            "The version of alexandria you last updated from isn't in the "
            "current repo history, so I can't show what changed upstream.",
            f"commit {commit} not found (repo may have been re-cloned or "
            "history was rewritten).",
            "pick [k], [u], or [d] — the two-way diff still works.",
            "ancestor-commit-unreachable",
        )
        return
    new_path = repo / rel_path
    new = new_path.read_text() if new_path.is_file() else ""
    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f"{rel_path} @ {commit}",
        tofile=f"{rel_path} (current upstream)",
    )
    text = "".join(diff)
    if not text:
        print("(no upstream changes since your last update)")
        return
    _page(text)


def _page(text: str) -> None:
    """Pipe text through less if stdout is a TTY; otherwise print directly."""
    if sys.stdout.isatty():
        try:
            proc = subprocess.Popen(["less", "-R"], stdin=subprocess.PIPE)
            proc.communicate(text.encode())
            return
        except FileNotFoundError:
            pass
    print(text)


def edit_merge(
    rel_path: Path,
    info: dict,
    local: Path,
    upstream: Path,
    repo: Path,
) -> bytes | None:
    """Open a conflict-marker file in $EDITOR, return merged bytes, or None
    if the user cancelled."""
    editor = os.environ.get("EDITOR")
    if not editor:
        print_error(
            "Your text editor isn't set, so I can't open the merge view.",
            "$EDITOR environment variable is empty.",
            "set EDITOR to your preferred editor "
            "(e.g., `export EDITOR=nano`) and re-run the update, or choose "
            "[k], [u], or [d] for this file instead.",
            "editor-not-set",
        )
        return None

    # Try to reconstruct ancestor for a 3-way merge view
    commit = info["manifest_entry"].get("installed_from_commit")
    ancestor_content = ""
    ancestor_available = False
    if commit:
        try:
            ancestor_content = subprocess.run(
                ["git", "-C", str(repo), "show", f"{commit}:{rel_path}"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            ancestor_available = True
        except subprocess.CalledProcessError:
            pass

    local_content = local.read_text()
    upstream_content = upstream.read_text()

    def _ensure_newline(s: str) -> str:
        return s if s.endswith("\n") else s + "\n"

    if ancestor_available:
        body = (
            "<<<<<<< local (your version)\n"
            + _ensure_newline(local_content)
            + "||||||| ancestor (last installed from upstream)\n"
            + _ensure_newline(ancestor_content)
            + "=======\n"
            + _ensure_newline(upstream_content)
            + ">>>>>>> upstream (current)\n"
        )
    else:
        print(
            "\n(The ancestor version isn't available in local git history, "
            "so I'm showing a two-way merge view.)"
        )
        body = (
            "<<<<<<< local (your version)\n"
            + _ensure_newline(local_content)
            + "=======\n"
            + _ensure_newline(upstream_content)
            + ">>>>>>> upstream (current)\n"
        )

    merge_path = local.with_name(local.name + ".merging")
    merge_path.write_text(body)

    markers = ("<<<<<<<", "|||||||", "=======", ">>>>>>>")
    try:
        while True:
            subprocess.run([editor, str(merge_path)])
            content = merge_path.read_text()
            if any(m in content for m in markers):
                choice = (
                    input(
                        "\nI still see conflict markers in the file.\n"
                        "  [r] Re-open in editor\n"
                        "  [k] Keep the file as-is (markers included)\n"
                        "  [c] Cancel merging this file (no changes)\n"
                        "Choice: "
                    )
                    .strip()
                    .lower()
                )
                if choice == "r":
                    continue
                if choice == "c":
                    return None
                # choice == "k" or anything else: keep as-is
            return content.encode()
    finally:
        if merge_path.is_file():
            merge_path.unlink()


def prompt_conflict(
    rel_path: Path,
    info: dict,
    idx: int,
    total: int,
    state: str,
    repo: Path,
    collection: Path,
) -> str:
    """Prompt for a single conflict. Returns 'keep', 'take', or 'edit'."""
    upstream = repo / rel_path
    local = collection / rel_path
    header = f"\n[{idx}/{total}] {rel_path}\n"
    if state == "UNMANAGED_CONFLICT":
        explanation = (
            "This file exists in your collection but wasn't recorded in the "
            "manifest — it may predate the manifest feature, or something "
            "else added it. Upstream has its own version of this file."
        )
    else:  # BOTH_CHANGED
        explanation = (
            "You have local changes to this file. Upstream has also changed "
            "it since the last update."
        )

    while True:
        print(header)
        print(explanation)
        print()
        print("  [k] Keep your version")
        print("  [u] Take the upstream version")
        print("  [e] Edit manually — open a merge view with conflict markers")
        print("  [d] Show the diff (local vs. upstream)")
        print("  [c] What changed upstream since the last update?")
        choice = input("\nChoice: ").strip().lower()
        if choice == "k":
            return "keep"
        if choice == "u":
            return "take"
        if choice == "e":
            return "edit"
        if choice == "d":
            show_diff(local, upstream, "local", "upstream")
        elif choice == "c":
            show_upstream_changes(rel_path, info, repo)
        else:
            print(f"  (unrecognized input: {choice!r} — please choose k, u, e, d, or c)")


def verify_collection(collection: Path) -> None:
    if not (collection / ".collection-index.yaml").is_file():
        print_error(
            "The path you gave me doesn't look like an alexandria collection.",
            f"no .collection-index.yaml found at {collection}",
            "check the path, or run /coll-build-new-collection to create a "
            "new collection there.",
            "not-a-collection",
        )
        sys.exit(2)


def handle_removed_files(
    collection: Path,
    manifest: dict,
    managed_set: set[str],
    get_backup_dir: "callable",
) -> list[str]:
    """Handle files in manifest that upstream no longer ships.
    Returns list of paths that were removed."""
    removed: list[str] = []
    for manifest_path_str in list(manifest.get("files", {}).keys()):
        if manifest_path_str in managed_set:
            continue
        local = collection / manifest_path_str
        local_sha = sha256_file(local)
        installed_sha = manifest["files"][manifest_path_str]["sha256"]

        if local_sha is None:
            # Already gone
            del manifest["files"][manifest_path_str]
        elif local_sha == installed_sha:
            # Unmodified — remove quietly. Left-behind empty directories are
            # harmless; the user can remove them if they notice.
            local.unlink()
            del manifest["files"][manifest_path_str]
            removed.append(manifest_path_str)
        else:
            # Modified locally, removed upstream — ask
            print(
                f"\n{manifest_path_str} was removed from upstream, but you've "
                "edited it since the last update."
            )
            print("  [d] Delete the file (your version is backed up first)")
            print("  [k] Keep it (alexandria will stop tracking it)")
            ch = input("Choice: ").strip().lower()
            if ch == "d":
                backup_dir = get_backup_dir()
                backup_file(
                    backup_dir,
                    Path(manifest_path_str),
                    local.read_bytes(),
                    "local",
                )
                local.unlink()
                removed.append(manifest_path_str)
            del manifest["files"][manifest_path_str]
    return removed


def run_init(collection: Path, repo: Path) -> int:
    """Write an initial manifest for a freshly-built collection. Used by
    coll-build-new-collection after it copies files in."""
    verify_collection(collection)
    manifest_path = collection / MANIFEST_FILENAME
    if manifest_path.is_file():
        print_error(
            "A manifest already exists in this collection, so I'm stopping to "
            "avoid overwriting it.",
            f"{manifest_path} already exists.",
            "if you meant to refresh it, delete the file first and re-run. "
            "If you meant to update the collection, use the update flow "
            "instead of --init.",
            "init-manifest-exists",
        )
        return 2

    paths = expand_managed_paths(repo)
    now = now_iso()
    commit = repo_commit(repo)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "last_updated_at": now,
        "files": {},
    }
    for rel in paths:
        local = collection / rel
        if local.is_file():
            manifest["files"][str(rel)] = {
                "sha256": sha256_file(local),
                "installed_at": now,
                "installed_from_commit": commit,
            }
    save_manifest(manifest_path, manifest)
    print(f"Manifest written: {manifest_path}")
    print(f"  Tracked files: {len(manifest['files'])}")
    return 0


def run_update(collection: Path, repo: Path, dry_run: bool) -> int:
    verify_collection(collection)
    manifest_path = collection / MANIFEST_FILENAME
    manifest = load_manifest(manifest_path)
    if not manifest:
        manifest = {"schema_version": SCHEMA_VERSION, "files": {}}

    # Schema check
    schema = manifest.get("schema_version", SCHEMA_VERSION)
    if schema > SCHEMA_VERSION:
        print_error(
            "Your collection's manifest was written by a newer version of "
            "alexandria than this one. I don't want to risk mis-interpreting "
            "it, so I'm stopping here.",
            f"manifest schema_version is {schema}, this script understands "
            f"up to {SCHEMA_VERSION}.",
            "update the alexandria repo to a newer version, then try again.",
            "schema-too-new",
        )
        return 2

    # Classify everything upstream ships
    paths = expand_managed_paths(repo)
    classifications = []
    for p in paths:
        state, info = classify(p, repo, collection, manifest)
        classifications.append((p, state, info))

    conflicts = [
        (p, s, i)
        for p, s, i in classifications
        if s in ("BOTH_CHANGED", "UNMANAGED_CONFLICT")
    ]
    auto = [(p, s, i) for p, s, i in classifications if s in ("NEW", "UPSTREAM_ONLY")]
    preserved = [(p, s, i) for p, s, i in classifications if s == "LOCAL_ONLY"]
    unchanged = [(p, s, i) for p, s, i in classifications if s == "UNCHANGED"]

    # Dry-run: report and exit
    if dry_run:
        print("\nDry run — no changes will be made.\n")
        print(f"  Already up to date:  {len(unchanged)}")
        n_new = sum(1 for _, s, _ in auto if s == "NEW")
        n_upd = sum(1 for _, s, _ in auto if s == "UPSTREAM_ONLY")
        print(f"  Would be added:      {n_new}")
        print(f"  Would be updated:    {n_upd}")
        print(f"  Would be preserved:  {len(preserved)} (your local edits)")
        print(f"  Needs your decision: {len(conflicts)}")
        for p, s, _ in conflicts:
            reason = (
                "both upstream and local changes"
                if s == "BOTH_CHANGED"
                else "file not in manifest"
            )
            print(f"    - {p} ({reason})")
        return 1 if conflicts else 0

    # Prepare backup dir (lazy)
    backup_dir_path = [None]  # holder for closure

    def get_backup_dir() -> Path:
        if backup_dir_path[0] is None:
            bd = collection / BACKUP_DIR / now_stamp()
            bd.mkdir(parents=True, exist_ok=True)
            backup_dir_path[0] = bd
        return backup_dir_path[0]

    # Resolve conflicts
    decisions: dict[Path, str | bytes] = {}
    if conflicts:
        bd = get_backup_dir()
        print(f"\n{len(conflicts)} file(s) need your decision:")
        for i, (p, _, _) in enumerate(conflicts, 1):
            print(f"  {i}. {p}")
        rel_bd = bd.relative_to(collection)
        print(
            f"\nBackups of any unchosen versions will be saved under {rel_bd}/"
        )
        print("Nothing is discarded.\n")
        print("Press Enter to review them one at a time,")
        print(
            "[A] to take the upstream version for all,"
            " [K] to keep your version for all,"
        )
        print("or q to cancel the update.")
        choice = input("\nChoice: ").strip().lower()
        if choice == "q":
            print("Update cancelled. No changes made.")
            return 0
        if choice == "a":
            for p, _, _ in conflicts:
                decisions[p] = "take"
        elif choice == "k":
            for p, _, _ in conflicts:
                decisions[p] = "keep"
        else:
            for idx, (p, state, info) in enumerate(conflicts, 1):
                d = prompt_conflict(
                    p, info, idx, len(conflicts), state, repo, collection
                )
                if d == "edit":
                    merged = edit_merge(
                        p, info, collection / p, repo / p, repo
                    )
                    if merged is None:
                        # Editor cancelled or EDITOR missing: treat as keep
                        decisions[p] = "keep"
                    else:
                        decisions[p] = merged  # bytes
                else:
                    decisions[p] = d

    # Apply changes
    now = now_iso()
    commit = repo_commit(repo)
    copied_new = 0
    copied_updated = 0
    kept_with_backup = 0
    taken_with_backup = 0
    merged_count = 0

    # Auto-updates
    for rel, state, _ in auto:
        src = repo / rel
        dst = collection / rel
        atomic_copy(src, dst)
        manifest.setdefault("files", {})[str(rel)] = {
            "sha256": sha256_file(dst),
            "installed_at": now,
            "installed_from_commit": commit,
        }
        if state == "NEW":
            copied_new += 1
        else:
            copied_updated += 1

    # Conflict decisions
    for rel, state, info in conflicts:
        decision = decisions.get(rel)
        src = repo / rel
        dst = collection / rel
        if decision == "keep":
            # Back up upstream for reference; leave dst alone.
            # Deliberately do NOT update the manifest entry: this preserves
            # the LOCAL_ONLY / BOTH_CHANGED state next run, so we'll prompt
            # again if upstream changes further. Prevents silent data loss.
            bd = get_backup_dir()
            backup_file(bd, rel, src.read_bytes(), "upstream")
            kept_with_backup += 1
        elif decision == "take":
            bd = get_backup_dir()
            if dst.is_file():
                backup_file(bd, rel, dst.read_bytes(), "local")
            atomic_copy(src, dst)
            manifest.setdefault("files", {})[str(rel)] = {
                "sha256": sha256_file(dst),
                "installed_at": now,
                "installed_from_commit": commit,
            }
            taken_with_backup += 1
        elif isinstance(decision, bytes):
            # Merged content from editor
            bd = get_backup_dir()
            if dst.is_file():
                backup_file(bd, rel, dst.read_bytes(), "local")
            backup_file(bd, rel, src.read_bytes(), "upstream")
            atomic_write(dst, decision)
            manifest.setdefault("files", {})[str(rel)] = {
                "sha256": sha256_file(dst),
                "installed_at": now,
                "installed_from_commit": commit,
            }
            merged_count += 1

    # Files removed upstream
    managed_set = {str(p) for p in paths}
    removed_upstream = handle_removed_files(
        collection, manifest, managed_set, get_backup_dir
    )

    # Update manifest metadata and flush
    manifest["schema_version"] = SCHEMA_VERSION
    manifest["last_updated_at"] = now
    save_manifest(manifest_path, manifest)

    # Auto-commit the update to the collection's git repo if version control
    # is enabled. Captures the files this update touched plus the manifest.
    if (collection / ".git").is_dir() and shutil.which("git") is not None:
        touched_paths: list[str] = [MANIFEST_FILENAME]
        for rel, _, _ in auto:
            touched_paths.append(str(rel))
        for rel, _, _ in conflicts:
            decision = decisions.get(rel)
            if decision in ("take",) or isinstance(decision, bytes):
                touched_paths.append(str(rel))
        if touched_paths:
            msg = f"Update from alexandria {commit}" if commit else "Update from alexandria"
            try:
                subprocess.run(
                    [
                        "uv",
                        "run",
                        "python",
                        "tools/commit_change.py",
                        str(collection),
                        "--message",
                        msg,
                    ]
                    + touched_paths,
                    cwd=collection,
                    check=False,
                )
            except Exception:
                pass  # commit_change.py prints its own errors

    # Post-processing: uv sync and wiki regen. Flush stdout before each
    # subprocess so the banner prints before the subprocess output, not after.
    print("\nSyncing dependencies...", flush=True)
    try:
        subprocess.run(["uv", "sync"], cwd=collection, check=True)
    except subprocess.CalledProcessError as e:
        print_error(
            "Dependencies were not synced. The file updates succeeded but "
            "uv sync returned an error.",
            f"uv sync exit code {e.returncode}",
            "run `uv sync` manually inside the collection directory. The "
            "manifest and file updates are already saved.",
            "uv-sync-failed",
        )
        return 1

    print("Regenerating wiki...", flush=True)
    try:
        subprocess.run(
            ["uv", "run", "python", "tools/generate_wiki.py", "."],
            cwd=collection,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print_error(
            "The wiki was not regenerated. The file updates succeeded but "
            "the wiki generator returned an error.",
            f"wiki generator exit code {e.returncode}",
            "run `uv run python tools/generate_wiki.py .` manually inside "
            "the collection directory.",
            "wiki-regen-failed",
        )
        return 1

    # Summary
    print("\nUpdate complete.\n")
    total_copied = copied_new + copied_updated
    print(f"  Files copied from upstream: {total_copied}")
    if total_copied:
        print(f"    (new: {copied_new}, updated: {copied_updated})")
    preserved_total = len(preserved) + kept_with_backup
    if preserved_total:
        print(f"  Local edits preserved:      {preserved_total}")
        if kept_with_backup:
            print(
                f"    Including {kept_with_backup} file(s) where upstream "
                "changes you chose to ignore are backed up for reference"
            )
    if taken_with_backup:
        print(
            f"  Took upstream over local:   {taken_with_backup} "
            "(your old versions backed up)"
        )
    if merged_count:
        print(f"  Merged manually:            {merged_count}")
    if removed_upstream:
        print(f"  Removed (no longer in upstream): {len(removed_upstream)}")
    if backup_dir_path[0] is not None:
        rel_bd = backup_dir_path[0].relative_to(collection)
        print(f"  Backups saved to:           {rel_bd}/")
    print()

    # Flag kept-local tools/ versions explicitly (wiki was regenerated with
    # the user's version, not upstream)
    kept_tools = [
        rel
        for rel, _, _ in conflicts
        if isinstance(decisions.get(rel), str)
        and decisions[rel] == "keep"
        and str(rel).startswith("tools/")
    ]
    if kept_tools:
        print(
            "Note: you kept your local version of one or more files under "
            "tools/. The wiki was regenerated using your version, not the "
            "current upstream generator:"
        )
        for rel in kept_tools:
            print(f"  - {rel}")
        print()

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Update a collection from the alexandria repo, with "
        "safety checks against overwriting your local edits.",
    )
    parser.add_argument(
        "collection", help="Path to the collection directory."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Classify files and report without making changes.",
    )
    group.add_argument(
        "--init",
        action="store_true",
        help="Write an initial manifest for a freshly-built collection. "
        "Used by coll-build-new-collection; does not sync or regenerate.",
    )
    args = parser.parse_args(argv)

    collection = Path(args.collection).resolve()
    repo = Path(__file__).resolve().parent.parent

    if args.init:
        return run_init(collection, repo)
    return run_update(collection, repo, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
