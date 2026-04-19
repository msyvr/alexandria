#!/usr/bin/env python3
"""Auto-commit helper, called by skills that modify collection files.

Silent no-op when the collection has no .git/ (user opted out of version
control, or the collection pre-dates the feature). When git is enabled,
stages the specified files and makes a commit with the given message.

Usage:
    uv run python tools/commit_change.py <collection_path> \\
        --message "Add physical item: The Dispossessed" \\
        <file1> [<file2> ...]

Any paths that are gitignored are silently skipped. If no files are
staged (all ignored or nothing to commit), the helper exits 0 without
committing. Commit failures are surfaced to stderr but do not fail the
calling skill's primary action.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def is_git_enabled(collection: Path) -> bool:
    return (collection / ".git").is_dir() and shutil.which("git") is not None


def filter_non_ignored(collection: Path, paths: list[str]) -> list[str]:
    """Return paths that are NOT gitignored. Uses `git check-ignore`.

    check-ignore exit codes:
      0 = all listed paths are ignored
      1 = none are ignored
      128 = error
    Regardless of exit, stdout lists the ignored ones (one per line).
    """
    if not paths:
        return []
    try:
        result = subprocess.run(
            ["git", "-C", str(collection), "check-ignore", "--verbose", "--"]
            + paths,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return paths  # git gone; return as-is and let add fail

    if result.returncode not in (0, 1):
        # Error; fall back to returning all paths (the add may warn but
        # we'll still catch errors at commit time)
        return paths

    ignored: set[str] = set()
    for line in result.stdout.splitlines():
        # Each line: "<source>:<linenum>:<pattern>\t<path>"
        # The path is after the tab.
        if "\t" in line:
            ignored.add(line.split("\t", 1)[1])
    return [p for p in paths if p not in ignored]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Auto-commit helper for alexandria collection skills."
    )
    parser.add_argument("collection", help="Path to the collection directory.")
    parser.add_argument(
        "--message",
        required=True,
        help="Commit message (one line, human-readable).",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files to stage for this commit. Paths may be absolute or "
        "relative to cwd; ignored files are skipped automatically.",
    )
    args = parser.parse_args(argv)

    collection = Path(args.collection).resolve()

    # Silent no-op if git isn't enabled on this collection
    if not is_git_enabled(collection):
        return 0

    # No paths given: nothing to do
    if not args.paths:
        return 0

    # Filter out gitignored paths so `git add` doesn't error on them
    non_ignored = filter_non_ignored(collection, args.paths)
    if not non_ignored:
        return 0

    # Stage
    try:
        subprocess.run(
            ["git", "-C", str(collection), "add", "--"] + non_ignored,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"Auto-commit: couldn't stage files ({e.stderr.strip() or 'unknown error'}). "
            "File changes are on disk; you can commit manually when ready.",
            file=sys.stderr,
        )
        return 1

    # Check whether anything is actually staged; if not, skip the commit
    status = subprocess.run(
        ["git", "-C", str(collection), "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
    )
    if not status.stdout.strip():
        return 0

    # Commit
    try:
        subprocess.run(
            ["git", "-C", str(collection), "commit", "-m", args.message],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"Auto-commit: staged but couldn't commit ({e.stderr.strip() or 'unknown error'}). "
            "Changes are staged; run `git commit` manually in the collection to finalize.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
