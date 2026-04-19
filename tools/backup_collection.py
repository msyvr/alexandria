#!/usr/bin/env python3
"""Back up a collection to disk via rsync.

First run: prompt for a destination, offering detected cloud-synced folders
first. Subsequent runs: confirm the stored destination. The skill always
appends `alexandria-backup-{collection-name}/` as a subdirectory so
`rsync --delete` is scoped and never touches unrelated content.

Before backing up, scans the collection root for stray files (things not
part of the expected alexandria structure) and notifies the user.

Destination state is stored at `.claude/state/backup-destination` inside
the collection (per-machine, gitignored).

Error messages follow the plain-English template described in
docs/guides/troubleshooting.md.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

TROUBLESHOOTING = "docs/guides/troubleshooting.md"
STATE_PATH = ".claude/state/backup-destination"
BACKUP_SUBDIR_PREFIX = "alexandria-backup-"

# Files expected at the collection root. Anything else at root is "stray".
EXPECTED_ROOT_FILES = {
    ".collection-index.yaml",
    "README.md",
    "CLAUDE.md",
    "collection-context.md",
    "pyproject.toml",
    "uv.lock",
    ".gitignore",
    ".alexandria-manifest.yaml",
    ".python-version",
}
EXPECTED_ROOT_DIRS = {
    ".git",
    ".claude",
    ".venv",
    ".alexandria-backups",
    "tools",
    "wiki",
}

# Cloud-folder detection patterns. Paths support glob (via pathlib).
# Ordered by how most users would recognize the service.
CLOUD_PATTERNS: list[tuple[str, list[str]]] = [
    (
        "iCloud Drive",
        [
            "~/Library/Mobile Documents/com~apple~CloudDocs",
            "~/Library/CloudStorage/iCloud*",
        ],
    ),
    (
        "Google Drive",
        [
            "~/Library/CloudStorage/GoogleDrive-*/My Drive",
            "~/Library/CloudStorage/GoogleDrive-*",
            "~/Google Drive",
        ],
    ),
    ("Dropbox", ["~/Library/CloudStorage/Dropbox", "~/Dropbox"]),
    (
        "OneDrive",
        [
            "~/Library/CloudStorage/OneDrive-Personal",
            "~/Library/CloudStorage/OneDrive-*",
            "~/OneDrive",
        ],
    ),
]


def print_error(what: str, details: str, what_to_do: str, anchor: str) -> None:
    print(f"\n{what}\n", file=sys.stderr)
    print(f"  Details: {details}", file=sys.stderr)
    print(f"  What to do: {what_to_do}", file=sys.stderr)
    print(f"  More info: {TROUBLESHOOTING}#{anchor}\n", file=sys.stderr)


def detect_cloud_folders() -> list[tuple[str, Path]]:
    """Return list of (service_name, resolved_path) for cloud folders that exist."""
    found: list[tuple[str, Path]] = []
    for service, patterns in CLOUD_PATTERNS:
        for pat in patterns:
            expanded = Path(pat).expanduser()
            if "*" in expanded.name or "*" in str(expanded):
                # Glob expansion. Walk parents that have no wildcards until
                # we reach a level with a wildcard, then glob.
                parts = expanded.parts
                static: list[str] = []
                for p in parts:
                    if "*" in p:
                        break
                    static.append(p)
                static_path = Path(*static)
                remaining = Path(*parts[len(static) :])
                if not static_path.is_dir():
                    continue
                matches = list(static_path.glob(str(remaining)))
                hit: Path | None = next(
                    (m for m in matches if m.is_dir()), None
                )
                if hit is not None:
                    found.append((service, hit))
                    break
            elif expanded.is_dir():
                found.append((service, expanded))
                break
    return found


def load_collection_name(collection: Path) -> str:
    """Read collection_name from .collection-index.yaml; fallback to dir name."""
    index = collection / ".collection-index.yaml"
    try:
        data = yaml.safe_load(index.read_text()) or {}
        name = data.get("collection_name") or collection.name
    except Exception:
        name = collection.name
    # Normalize for filesystem safety
    return "".join(c if (c.isalnum() or c in ("-", "_")) else "-" for c in name)


def load_stored_destination(collection: Path) -> Path | None:
    state = collection / STATE_PATH
    if not state.is_file():
        return None
    raw = state.read_text().strip()
    if not raw:
        return None
    return Path(raw).expanduser()


def save_stored_destination(collection: Path, destination: Path) -> None:
    state = collection / STATE_PATH
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(str(destination) + "\n")


def prompt_destination(
    collection: Path, collection_name: str
) -> Path | None:
    """First-run prompt flow. Returns resolved absolute destination or None if cancelled."""
    cloud = detect_cloud_folders()

    print("\nWhere would you like to back up to?\n")

    options: list[tuple[str, str, Path | None]] = []
    # label (shown), kind ("cloud" | "external" | "custom"), path (for cloud)
    idx = 1
    if cloud:
        print("I found these cloud-synced folders on your machine:")
        for service, path in cloud:
            display = f"  [{idx}] {service:<14} (~{str(path)[len(os.path.expanduser('~')):]})" if str(path).startswith(os.path.expanduser("~")) else f"  [{idx}] {service:<14} ({path})"
            print(display)
            options.append((service, "cloud", path))
            idx += 1
        print()
        print("Other options:")
    external_idx = idx
    print(f"  [{idx}] External drive or folder")
    options.append(("External drive or folder", "external", None))
    idx += 1
    custom_idx = idx
    print(f"  [{idx}] Another location on this machine (paste a path)")
    options.append(("Another location", "custom", None))

    print()
    choice_str = input("Choice: ").strip()
    if not choice_str:
        return None
    try:
        choice = int(choice_str)
    except ValueError:
        print(f"Unrecognized choice: {choice_str!r}")
        return None
    if choice < 1 or choice > len(options):
        print(f"Choice out of range: {choice}")
        return None

    label, kind, path = options[choice - 1]

    subdir_name = f"{BACKUP_SUBDIR_PREFIX}{collection_name}"

    if kind == "cloud":
        assert path is not None
        return (path / subdir_name).resolve()

    if kind == "external":
        print(
            "\nPaste the path to your external drive (or a folder on it):"
        )
        raw = input("> ").strip()
    else:  # custom
        print("\nPaste the path you'd like to back up to:")
        raw = input("> ").strip()

    if not raw:
        return None
    base = Path(raw).expanduser().resolve()
    return base / subdir_name


def validate_destination(
    collection: Path, destination: Path
) -> str | None:
    """Return error message if destination is unsafe, None if ok."""
    # Resolve both
    collection = collection.resolve()
    # destination may not exist yet; resolve its parent if it doesn't
    try:
        dest_resolved = destination.resolve()
    except OSError:
        dest_resolved = destination

    # Refuse absolute root, home directly, or bare drive roots
    if str(dest_resolved) in {"/", str(Path.home())}:
        return (
            f"destination {dest_resolved} is too broad — backups must go into "
            "a specific folder, not the filesystem root or your home directory "
            "directly."
        )

    # Refuse if destination is inside the collection (would recurse)
    try:
        dest_resolved.relative_to(collection)
        return (
            f"destination is inside the collection being backed up. That would "
            "cause an infinite loop as the backup mirrors itself."
        )
    except ValueError:
        pass

    # Refuse if collection is inside destination (parent relationship —
    # source is inside destination = --delete would wipe unrelated stuff
    # outside the subdirectory we're scoping to, but since we always append
    # a subdirectory, this is specifically the case where the destination
    # subdirectory would contain the collection, which is still bad.)
    try:
        collection.relative_to(dest_resolved)
        return (
            f"your collection is inside the backup destination. The backup "
            f"subdirectory would overlap with the live collection, which isn't "
            "a safe backup target."
        )
    except ValueError:
        pass

    return None


def scan_stray_root_entries(
    collection: Path, known_section_dirs: set[str]
) -> list[str]:
    """List files/dirs at the collection root that aren't recognized."""
    stray: list[str] = []
    for entry in sorted(collection.iterdir()):
        name = entry.name
        if entry.is_dir():
            if name in EXPECTED_ROOT_DIRS or name in known_section_dirs:
                continue
            stray.append(f"{name}/")
        else:
            if name in EXPECTED_ROOT_FILES:
                continue
            stray.append(name)
    return stray


def read_section_dirs(collection: Path) -> set[str]:
    """Infer section directories from the catalog's item paths."""
    index = collection / ".collection-index.yaml"
    dirs: set[str] = set()
    try:
        data = yaml.safe_load(index.read_text()) or {}
    except Exception:
        return dirs
    sections = data.get("sections") or {}
    # sections is typically a dict of section_name -> list of item slugs/info
    # We also pick up directory names from item paths if present.
    if isinstance(sections, dict):
        for section in sections.keys():
            dirs.add(str(section))
    return dirs


def confirm_destination(destination: Path, first_run: bool) -> bool:
    if first_run:
        print(f"\nFirst backup will be written to:\n  {destination}\n")
        print(
            "Files inside that subdirectory will be mirrored from your collection."
        )
        print("Anything else in the parent folder is untouched.\n")
        ans = input("Proceed? [y/N]: ").strip().lower()
        return ans == "y"
    else:
        print(f"\nBackup destination: {destination}")
        ans = input("Use this target? [Y/n]: ").strip().lower()
        return ans in ("", "y", "yes")


def check_rsync_installed() -> bool:
    return shutil.which("rsync") is not None


def run_rsync(source: Path, destination: Path) -> int:
    destination.mkdir(parents=True, exist_ok=True)
    # Trailing slashes: copy *contents* of source into destination.
    src = f"{source}/"
    dst = f"{destination}/"
    cmd = ["rsync", "-a", "--delete", "--stats", "--human-readable", src, dst]
    print(f"\nRunning: rsync -a --delete {src} {dst}\n", flush=True)
    result = subprocess.run(cmd)
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Back up an alexandria collection via rsync."
    )
    parser.add_argument("collection", help="Path to the collection directory.")
    parser.add_argument(
        "--force-new-destination",
        action="store_true",
        help="Ignore any stored destination and prompt fresh.",
    )
    args = parser.parse_args(argv)

    collection = Path(args.collection).resolve()

    # Verify collection
    if not (collection / ".collection-index.yaml").is_file():
        print_error(
            "The path you gave me doesn't look like an alexandria collection.",
            f"no .collection-index.yaml found at {collection}",
            "check the path, or run /coll-build-new-collection to create a "
            "new collection there.",
            "not-a-collection",
        )
        return 2

    # rsync installed?
    if not check_rsync_installed():
        print_error(
            "rsync isn't installed, so I can't back up your collection.",
            "`rsync` command not found.",
            "macOS: rsync is built-in; try opening a new terminal. "
            "Linux: `sudo apt install rsync` (Debian/Ubuntu) or "
            "`sudo dnf install rsync` (Fedora). "
            "Windows (WSL): `sudo apt install rsync` in your WSL terminal.",
            "rsync-not-installed",
        )
        return 2

    collection_name = load_collection_name(collection)

    # Resolve destination: stored or prompt
    first_run = False
    destination = (
        None if args.force_new_destination else load_stored_destination(collection)
    )
    if destination is None:
        first_run = True
        destination = prompt_destination(collection, collection_name)
        if destination is None:
            print("Backup cancelled. No changes made.")
            return 0
    else:
        # Confirm existing
        if not confirm_destination(destination, first_run=False):
            destination = prompt_destination(collection, collection_name)
            if destination is None:
                print("Backup cancelled. No changes made.")
                return 0
            first_run = True  # treat new destination as first run for that target

    # Validate destination
    err = validate_destination(collection, destination)
    if err:
        print_error(
            "That destination isn't safe to back up to.",
            err,
            "pick a folder outside the collection, like an external drive "
            "or a cloud-synced folder.",
            "backup-destination-unsafe",
        )
        return 2

    # Scan for stray files at the collection root
    section_dirs = read_section_dirs(collection)
    strays = scan_stray_root_entries(collection, section_dirs)
    if strays:
        print()
        print(
            "Noticed files/directories in your collection root that aren't "
            "part of the usual structure — these will be included in the backup:"
        )
        for s in strays:
            print(f"  - {s}")
        print()
        print(
            "If that's intentional, no action needed. If not, you can remove "
            "them before running the backup again."
        )
        print()

    # Confirm (first run only; subsequent runs confirmed above)
    if first_run:
        if not confirm_destination(destination, first_run=True):
            print("Backup cancelled. No changes made.")
            return 0

    # Run rsync
    rc = run_rsync(collection, destination)
    if rc != 0:
        print_error(
            "Backup didn't complete cleanly.",
            f"rsync exit code {rc}",
            "check the rsync output above for details. Your collection "
            "itself is untouched; the backup may be partial.",
            "rsync-failed",
        )
        return 1

    # Save destination for next time
    save_stored_destination(collection, destination)

    # Final guidance
    print()
    print("Backup complete.")
    print()
    print("To restore from this backup to a new or rebuilt collection:")
    print(f"  rsync -a {destination}/ <new-collection-path>/")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
