# /coll-disable-version-control

Disable git version control for a collection. Removes the `.git/` directory
and the collection's `.gitignore`. Does not touch any of the collection's
items, metadata, notes, or wiki content.

This is reversible — the user can re-enable version control any time with
`/coll-enable-version-control`, which starts a fresh git history from that
point forward.

## Before starting

Detect the collection context by walking up from the current directory
looking for `.collection-index.yaml`. If not found, explain that this skill
must run inside a collection directory.

Check whether the collection has a `.git/` directory. If not, explain that
version control isn't currently enabled and there's nothing to disable.

## The workflow

1. **Warn the user plainly.** Tell them:

   - `.git/` and `.gitignore` will be removed from the collection
   - Any git history will be deleted — including the ability to rewind
     accidental edits that predate this skill
   - Their items, metadata, notes, and wiki are untouched
   - They can re-enable later with `/coll-enable-version-control`, but
     that starts a fresh history
   - `.alexandria-backups/` (from any prior `/coll-backup` runs) are
     unaffected

2. **Confirm they want to proceed.** Require a clear yes before doing
   anything destructive. If the user hesitates or asks what git does,
   answer their questions rather than pushing them forward.

3. **If confirmed, remove both files**:

   ```
   rm -rf {collection_path}/.git
   rm {collection_path}/.gitignore
   ```

   (The `.gitignore` is alexandria-managed; removing it along with `.git`
   keeps the collection in a clean, consistent state for a non-git
   collection.)

4. **Report what was done.** One-line summary, plus the reminder:

   > Version control has been disabled for this collection. You can enable
   > it again any time with /coll-enable-version-control.

## What this does NOT do

- Does not delete any of the collection's actual content — items, metadata,
  notes, READMEs, wiki, catalog all remain intact
- Does not affect `.alexandria-backups/` or any external backups the user
  has made via `/coll-backup`
- Does not push anything or change any remote state (there is no push in
  alexandria yet regardless)
