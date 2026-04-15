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
   - **Yes, rename the directory too** — rename the directory to match
     the new name (slugified: lowercase, spaces to hyphens). Warn the
     user that they'll need to `cd` to the new path afterward.
   - **No, just change the display name** — the directory stays where it
     is, only `.collection-index.yaml` and the wiki change.

4. **Update `.collection-index.yaml`**: change `collection_name` to the
   new name.

5. **If renaming the directory**: rename it using `mv`. Tell the user
   the new path.

6. **Regenerate the wiki** so the header, footer, and all pages reflect
   the new name:

   ```
   uv run python tools/generate_wiki.py .
   ```

   (If the directory was renamed, run this from the new path.)

7. **Confirm what was done and remind the user:**

   > Collection renamed to "{new name}".
   >
   > {if directory renamed:}
   > The directory was moved to `{new path}`. Start your next session from there:
   > ```
   > cd {new path}
   > claude
   > ```

## What this changes

- `collection_name` in `.collection-index.yaml`
- All wiki HTML (via regeneration)
- Optionally the directory name

## What this does NOT change

- Item directories, metadata, notes, or any content
- Section structure
- Slugs
