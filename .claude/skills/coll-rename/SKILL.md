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

   Regenerate the wiki:
   ```
   uv run python tools/generate_wiki.py .
   ```

   Done. Confirm the new name is live.

6. **If renaming the directory**:

   a. Update `.collection-index.yaml` with the new name (do this first,
      while the current path still works).
   b. Rename the directory with `mv`.
   c. **Do NOT attempt to regenerate the wiki or do any further file
      operations** — the working directory no longer exists. Everything
      after the `mv` will fail, and that's expected.
   d. Tell the user:

      > Collection renamed. Start a new session from the new location:
      >
      > ```
      > cd {new_path}
      > claude
      > ```
      >
      > Then regenerate the wiki: `uv run python tools/generate_wiki.py .`

## What this changes

- `collection_name` in `.collection-index.yaml`
- All wiki HTML (via regeneration)
- Optionally the directory name

## What this does NOT change

- Item directories, metadata, notes, or any content
- Section structure
- Slugs
