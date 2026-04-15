# /coll-import-collection

Import all items from another collection into this one. Use this when you
want to merge two collections, migrate from an old collection to a new one,
or consolidate multiple collections into one.

## Before starting

Detect the collection context by walking up from the current directory
looking for `.collection-index.yaml`. If not found, explain that this
skill must be run inside a collection — the current collection is the
**destination**; the user provides the **source** collection path.

## The workflow

1. **Ask for the source collection path.** The user provides the path
   to the collection they want to import from (e.g., `~/old-collection`).
   Verify it contains a `.collection-index.yaml`.

2. **Read both collections.** Load the source and destination indexes.
   Show a summary:

   > Source: "{source name}" at {source path} — {N} items in {M} sections
   > Destination: "{dest name}" (this collection) — {N} items in {M} sections

3. **Check for conflicts.** Compare slugs between source and destination.
   If any slugs match (same directory name in both collections):
   - List the conflicts
   - For each, ask: skip (don't import this item), rename (add a suffix
     to the imported item's slug/directory), or replace (overwrite the
     destination item)
   - Default recommendation: rename with `-imported` suffix

4. **Handle sections.** For each section in the source:
   - If the section already exists in the destination, import items into
     the existing section
   - If the section doesn't exist, create it in the destination
   - Ask the user to confirm the section mapping (they may want to
     reclassify some items into different destination sections)

5. **Copy the items.** For each source item (after conflict resolution):
   - Copy the entire item directory into the destination under the
     appropriate section
   - The item keeps its metadata.yaml, README.md, notes/, and all content
   - Update the `section` field in metadata.yaml if the item is going
     into a different section than it was in the source

6. **Copy the source's collection-context.md** (if it exists) as a
   journal entry into the destination's collection-context.md, prefixed
   with a note: "Imported from {source name} on {date}".

7. **Rebuild the destination's `.collection-index.yaml`** by scanning
   all metadata.yaml files. This is safer than trying to merge two
   index files.

8. **Regenerate the wiki.**

   ```
   uv run python tools/generate_wiki.py .
   ```

9. **Report what was done:**

   > Imported {N} items from "{source name}" into "{dest name}".
   > - {X} items added to existing sections
   > - {Y} items added to new sections: {list}
   > - {Z} items skipped (conflicts)
   > - {W} items renamed (conflict resolution)
   >
   > The source collection at {source path} is unchanged.

10. **Invoke `/coll-notes`** to log the import in the destination's
    collection-context.md.

## What this does

- Copies item directories from source to destination
- Creates new sections in the destination as needed
- Resolves slug conflicts with user input
- Rebuilds the destination index
- Regenerates the destination wiki
- Logs the import in the destination journal

## What this does NOT do

- Does not modify or delete the source collection (it's read-only)
- Does not merge metadata.yaml fields (each item keeps its own metadata)
- Does not deduplicate items with the same title but different slugs
  (that's a manual curation decision)
- Does not copy the source's `.claude/skills/` or `tools/` (the
  destination already has its own)
