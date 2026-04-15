# /coll-update-from-latest-alexandria

Update an existing collection to match the current alexandria repo — skills,
wiki styling, and generated views. Run this from the alexandria repo directory
after pulling the latest changes.

## When to use this

After updating your alexandria clone:

```
cd ~/alexandria
git pull
uv sync
```

Then start Claude Code from the alexandria repo and run this skill.

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

4. **Regenerate the wiki.** Run the wiki generator from this repo against
   the collection. This updates the stylesheet, templates, and all generated
   HTML to reflect any changes in the tools:

   ```
   uv run python {this_repo}/tools/generate_wiki.py {collection_path}
   ```

5. **Report what was updated:**
   - List skill directories that were copied (note any new ones)
   - Confirm the wiki was regenerated with the latest styling and templates

6. **Remind the user.** Updated skills take effect in the next Claude Code
   session from the collection directory:

   > Collection at `{path}` updated:
   > - Skills: latest versions copied
   > - Wiki: regenerated with current styling
   >
   > To use the updated skills, start a new Claude Code session:
   >
   > ```
   > cd {path}
   > claude
   > ```

## What this updates

- Skill instruction files (`.claude/skills/coll-*/SKILL.md`)
- Wiki HTML, stylesheet, and all generated views (homepage, index pages,
  item pages, journal)

## What this does NOT modify

- The collection's data (items, metadata, sections, journal content)
- Item directories or their contents (README, metadata.yaml, notes/)
- The `.collection-index.yaml` catalog (it's read, not written)
- Python dependencies — `uv sync` (done before this skill) handles that
