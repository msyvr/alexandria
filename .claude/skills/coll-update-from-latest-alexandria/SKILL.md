# /coll-update-from-latest-alexandria

Update an existing collection's skills to match the current alexandria repo.
Run this from the alexandria repo directory after pulling the latest changes.

## When to use this

After updating your alexandria clone:

```
cd ~/alexandria
git pull
uv sync
```

Then start Claude Code from the alexandria repo and run this skill to push
the updated skills to your collection.

## The workflow

1. **Ask which collection to update.** The user provides the path to their
   collection directory (e.g., `~/my-collection`). There's no stored default —
   ask every time, since the user may have multiple collections.

2. **Verify the collection exists.** Check that the path contains a
   `.collection-index.yaml`. If not, explain that the path doesn't appear
   to be a collection and ask for the correct path.

3. **Copy the skills.** Copy every directory from this repo's
   `.claude/skills/` into the collection's `.claude/skills/`, replacing
   existing files.

4. **Report what was updated.** List the skill directories that were copied.
   Note any new skills that weren't in the collection before (these are
   additions from the latest alexandria version).

5. **Remind the user.** The updated skills take effect when they start a
   new Claude Code session from the collection directory:

   > Skills updated in your collection at `{path}`. To use the latest
   > versions, start a new Claude Code session from there:
   >
   > ```
   > cd {path}
   > claude
   > ```

## What this updates

- Skill instruction files (`.claude/skills/coll-*/SKILL.md`) — the
  instructions Claude reads when `/coll-*` commands are invoked from
  the collection

## What this does NOT update or modify

- The collection's data (items, metadata, sections, wiki, journal)
- Python tools (`tools/generate_wiki.py`, etc.) — these are invoked
  from the alexandria repo directly, so pulling already updated them
- Python dependencies — `uv sync` (done before this skill) handles that
