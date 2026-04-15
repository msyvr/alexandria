# /coll-update-from-latest-alexandria

Update an existing collection to match the current alexandria repo — skills,
tools, dependencies, and generated views. Run this from the alexandria repo
directory after pulling the latest changes.

## When to use this

After updating your alexandria clone:

```
cd ~/alexandria
git pull
uv sync
```

Then start Claude Code from the alexandria repo and run this skill.

## The workflow

1. **Find and offer known collections.** Before asking for a path, scan for
   directories containing `.collection-index.yaml` in likely locations:
   - `~/` (direct children only — e.g., `~/my-collection`)
   - `~/Documents/` (direct children)
   - The parent directory of the current project (siblings of the repo)

   For each found, read the `collection_name` from the index file.

   If collections are found, present them as numbered options plus a manual
   entry option:

   > Found these collections:
   > 1. my-collection (~/my-collection)
   > 2. work-references (~/Documents/work-references)
   > 3. Enter a different path

   If no collections are found, ask for the path directly.

2. **Verify the collection.** Whether selected from the list or entered
   manually, check that the path contains a `.collection-index.yaml`. If
   not, explain and ask again.

3. **Copy skills.** Copy every directory from this repo's `.claude/skills/`
   into the collection's `.claude/skills/`, replacing existing files.

4. **Copy tools.** Copy the `tools/` directory from this repo into the
   collection's `tools/`, replacing existing files:
   - `generate_wiki.py` — the wiki generator
   - `_wiki_templates.py` — HTML templates
   - `_wiki_style.css` — the stylesheet

5. **Copy pyproject.toml.** Copy `pyproject.toml` from this repo into the
   collection root, replacing the existing one. This ensures the collection's
   dependency list matches the current alexandria version.

6. **Run `uv sync` in the collection** to install any new or updated
   dependencies:

   ```
   cd {collection_path} && uv sync
   ```

7. **Regenerate the wiki.** Run the wiki generator from the collection's
   own copy of the tools (not the repo's):

   ```
   cd {collection_path} && uv run python tools/generate_wiki.py .
   ```

8. **Report what was updated:**
   - Skills: list directories copied (note any new ones)
   - Tools: updated (generator, templates, stylesheet)
   - Dependencies: synced
   - Wiki: regenerated with latest styling and templates

9. **Remind the user.** Updated skills take effect in the next Claude Code
   session from the collection directory:

   > Collection at `{path}` updated:
   > - Skills, tools, and dependencies: latest versions
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
- Wiki generator and templates (`tools/`)
- Stylesheet (`tools/_wiki_style.css` → copied into `wiki/_assets/` on regen)
- Python dependency list (`pyproject.toml`)
- All generated wiki HTML

## What this does NOT modify

- The collection's data (items, metadata, sections, journal content)
- Item directories or their contents (README, metadata.yaml, notes/)
- The `.collection-index.yaml` catalog (read for wiki generation, not written)
