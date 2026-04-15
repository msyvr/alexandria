# /coll-rename

Rename the current collection. Changes the display name used in the wiki
header, footer, and generated pages. Optionally renames the directory too.

## Before starting

Detect the collection context by walking up from the current directory
looking for `.collection-index.yaml`. If not found, explain that this
skill must be run inside a collection.

## The workflow

1. **Show the current name.** Read `collection_name` from
   `.collection-index.yaml` and show it.

2. **Ask for the new name.**

3. **Ask whether to also rename the directory.** The collection directory
   doesn't have to match the collection name, but most users will want
   them consistent. Options:
   - **Yes, rename the directory too**
   - **No, just change the display name**

4. **Update `.collection-index.yaml`**: change `collection_name` to the
   new name.

5. **If NOT renaming the directory** (display name only):

   Regenerate the wiki immediately:
   ```
   uv run python tools/generate_wiki.py .
   ```

   Confirm:
   > Collection display name changed to "{new name}". Wiki regenerated.

6. **If renaming the directory**: do NOT run `mv` during this session.
   Renaming the directory while Claude Code is running from it will break
   all subsequent operations.

   Instead, update `.collection-index.yaml` with the new name (this works
   because the file is written before anything moves), then give the user
   clear instructions to do the rest themselves:

   > Display name updated to "{new name}" in `.collection-index.yaml`.
   >
   > To rename the directory, exit this session and run these commands:
   >
   > ```
   > exit
   > mv {current_path} {new_path}
   > cd {new_path}
   > uv run python tools/generate_wiki.py .
   > claude
   > ```
   >
   > The `mv` renames the directory, the next line regenerates the wiki
   > with the new name, and then you start a fresh Claude Code session
   > from the new location.

   This is three commands the user pastes into their terminal. The wiki
   regeneration must happen from the new path (after the mv).

## What this changes

- `collection_name` in `.collection-index.yaml`
- All wiki HTML (via regeneration — either done in-session or by the user
  after the directory rename)
- Optionally the directory name (done by the user, not by Claude)

## What this does NOT change

- Item directories, metadata, notes, or any content
- Section structure
- Slugs
