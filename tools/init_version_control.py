#!/usr/bin/env python3
"""Initialize git version control for a collection.

Used by two skills:
  - coll-build-new-collection (at build time, after the manifest step)
  - coll-enable-version-control (for collections that opted out or pre-date
    the version-control feature)

What it does:
  1. Verifies the collection path.
  2. Refuses if a .git/ directory already exists.
  3. Runs `git init` in the collection.
  4. Copies tools/collection-gitignore.template to {collection}/.gitignore.
  5. Resolves git identity (global if set; prompts if not).
  6. Stages the gitignore and all non-ignored existing files, makes an
     initial commit.

Error messages follow the plain-English template described in
docs/guides/troubleshooting.md.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

TROUBLESHOOTING = "docs/guides/troubleshooting.md"


def print_error(what: str, details: str, what_to_do: str, anchor: str) -> None:
    print(f"\n{what}\n", file=sys.stderr)
    print(f"  Details: {details}", file=sys.stderr)
    print(f"  What to do: {what_to_do}", file=sys.stderr)
    print(f"  More info: {TROUBLESHOOTING}#{anchor}\n", file=sys.stderr)


def check_git_installed() -> bool:
    return shutil.which("git") is not None


def read_global_config(key: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "config", "--global", "--get", key],
            capture_output=True,
            text=True,
            check=True,
        )
        value = result.stdout.strip()
        return value or None
    except subprocess.CalledProcessError:
        return None


def resolve_identity() -> tuple[str, str, bool]:
    """Return (name, email, from_global). Prompts user if missing."""
    name = read_global_config("user.name")
    email = read_global_config("user.email")

    if name and email:
        return name, email, True

    print(
        "\nGit needs a name and email to label your commits. These are\n"
        "stored only on your machine — nothing is sent anywhere unless\n"
        "you later push your collection to GitHub.\n"
    )
    print(
        "Any name and email works for now; you can change them later. If\n"
        "you have a GitHub account and might push there eventually, use\n"
        "that account's email so commits attribute to you.\n"
    )

    import getpass, socket

    default_name = name or getpass.getuser() or "user"
    default_email = email or f"{default_name}@{socket.gethostname() or 'local'}"

    name_in = input(f"Name [{default_name}]: ").strip() or default_name
    email_in = input(f"Email [{default_email}]: ").strip() or default_email

    return name_in, email_in, False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Initialize git for an alexandria collection."
    )
    parser.add_argument("collection", help="Path to the collection directory.")
    parser.add_argument(
        "--message",
        default="Initialize collection",
        help="Commit message for the initial commit.",
    )
    args = parser.parse_args(argv)

    collection = Path(args.collection).resolve()
    repo = Path(__file__).resolve().parent.parent

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

    # Git installed?
    if not check_git_installed():
        print_error(
            "I can't set up version control because git isn't installed.",
            "`git` command not found.",
            "macOS: run `xcode-select --install`. Linux: "
            "`sudo apt install git` (Debian/Ubuntu) or "
            "`sudo dnf install git` (Fedora).",
            "git-not-installed",
        )
        return 2

    # Already a git repo?
    if (collection / ".git").exists():
        print_error(
            "This collection already has git version control enabled. I'm "
            "stopping to avoid overwriting existing history.",
            f"{collection / '.git'} already exists.",
            "if you want to start fresh, run /coll-disable-version-control "
            "first (note: this removes existing git history).",
            "version-control-already-enabled",
        )
        return 2

    # Locate gitignore template
    template = repo / "tools" / "collection-gitignore.template"
    if not template.is_file():
        print_error(
            "I can't find the gitignore template in the alexandria repo.",
            f"expected {template} to exist.",
            "make sure you're running from a complete alexandria repo. "
            "Re-clone or re-pull if the file is missing.",
            "gitignore-template-missing",
        )
        return 2

    # git init
    print("Initializing git in your collection...", flush=True)
    try:
        subprocess.run(
            ["git", "init", "-b", "main", str(collection)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print_error(
            "git init didn't complete cleanly.",
            f"git init exit code {e.returncode}: {e.stderr.strip()}",
            "check permissions on the collection directory and try again.",
            "git-init-failed",
        )
        return 1

    # Copy gitignore
    gitignore_path = collection / ".gitignore"
    shutil.copy(template, gitignore_path)

    # Resolve identity
    name, email, from_global = resolve_identity()
    try:
        subprocess.run(
            ["git", "-C", str(collection), "config", "--local", "user.name", name],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "-C", str(collection), "config", "--local", "user.email", email],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print_error(
            "Couldn't save git identity for this collection.",
            f"git config exit code {e.returncode}: {e.stderr.strip()}",
            "the .git directory has been created; you can set identity "
            "manually with `git config --local user.name/email` inside the "
            "collection.",
            "git-identity-save-failed",
        )
        return 1

    if from_global:
        print()
        print(
            "Git version control is now enabled for this collection. This lets"
        )
        print(
            "you rewind changes later, and (optionally, later) back up to a"
        )
        print("private GitHub repo.")
        print()
        print("Using your existing global git identity:")
        print(f"  Name:  {name}")
        print(f"  Email: {email}")
        print()
        print("To use a different name or email just for this collection:")
        print("  git config --local user.name \"Your Name\"")
        print("  git config --local user.email \"you@example.com\"")
        print()
        print(
            "If you don't want git for this collection, run "
            "/coll-disable-version-control (one command, reversible)."
        )
        print()
        print(
            "See docs/guides/version-control-for-your-collection.md for more."
        )
        print()

    # Initial commit
    print(f"Making initial commit: {args.message!r}", flush=True)
    try:
        subprocess.run(
            ["git", "-C", str(collection), "add", "-A"],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "-C", str(collection), "commit", "-m", args.message],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print_error(
            "I set up git but couldn't make the initial commit.",
            f"git commit exit code {e.returncode}: {e.stderr.strip()}",
            "inside the collection, run `git status` to see what's going "
            "on, then `git commit -m \"Initial commit\"` when ready.",
            "git-initial-commit-failed",
        )
        return 1

    print(f"Done. Version control is now enabled for {collection.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
