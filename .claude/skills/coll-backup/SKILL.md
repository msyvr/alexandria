# /coll-backup

Back up the entire collection — catalog, items (including binary content like
PDFs and photos), notes, generated wiki, git repo — to an external drive, a
cloud-synced folder, or any other location the user picks. Uses `rsync` to
mirror the collection, so repeated runs are incremental and fast.

Complements git: git tracks the textual backbone of the collection (catalog,
metadata, notes, skills). This skill backs up *everything* including binaries
and state. Both mechanisms together give a complete recovery story — see
`docs/guides/backing-up-your-collection.md`.

## Before starting

Detect the collection context by walking up from the current directory
looking for `.collection-index.yaml`. If not found, explain that this skill
must run inside a collection directory.

## The workflow

Run the backup script from the alexandria repo directory, pointing at the
user's collection:

```
uv run python tools/backup_collection.py {collection_path}
```

The script handles the full flow:

1. **First run:** detects cloud-synced folders on the user's machine
   (iCloud Drive, Dropbox, Google Drive, OneDrive) and offers them as
   numbered options alongside "External drive or folder" and "Another
   location." The user picks one; the script appends
   `alexandria-backup-{collection-name}/` as a subdirectory so the
   `--delete` mirror semantics are scoped.
2. **Subsequent runs:** confirms the stored destination (`[Y/n]` default
   yes). Pass `--force-new-destination` to prompt fresh instead.
3. **Before copying:** scans the collection root for files/directories
   that aren't part of the usual alexandria structure and notifies the
   user (soft — doesn't block). Lets them remove stray files if they
   weren't intentional.
4. **Validates the destination:** refuses paths that would recurse into
   the collection or overlap with it; refuses `/` and `$HOME` directly.
5. **Runs rsync** with `-a --delete` to mirror the collection's current
   state into the backup destination's subdirectory.
6. **Saves the destination** to `.claude/state/backup-destination` for
   next time.
7. **Prints restore guidance** — a one-line `rsync` command to restore
   to a new collection path.

Pass the script's output through to the user as-is. The prompts and
notices are written for the user directly; do not summarize or rephrase
the destination choices.

## Important behavior notes

- **Nothing is ever deleted from the source.** The script only mirrors
  collection → destination, never the other way.
- **The `alexandria-backup-{collection-name}/` subdirectory scopes the
  mirror.** Files elsewhere on the destination drive or folder are
  untouched.
- **Binaries go to the backup, not to git.** PDFs, photos, audio, video,
  and the generated wiki are gitignored by default and covered by this
  backup instead.
- **Cloud-synced destinations work as regular folders.** Choosing
  "iCloud Drive" puts the backup in your iCloud folder on disk; iCloud
  then syncs it to Apple's servers via the normal iCloud mechanism.

## If something goes wrong

If the script errors out, surface the error message to the user (it
includes a plain-English description and a link to the troubleshooting
guide). Common cases covered: rsync not installed, destination unsafe,
destination unreachable.

Do not attempt to re-run or repair by running `rsync` manually unless
the user explicitly asks.

## What this skill does NOT do

- Does not push to GitHub or any remote (that's git's job; future
  skill for GitHub is planned but not yet available)
- Does not restore from a backup (the restore is one `rsync` command,
  printed at the end of a successful backup; to restore, run that
  command manually)
- Does not version the backup itself — each run overwrites the
  destination to match the current collection state
