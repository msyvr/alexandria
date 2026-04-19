# /coll-add-item-notes

Add personal notes to an item in your collection. Write notes in any text
editor, then bring them in here. Each note is a separate file in the item's
`notes/` directory — you can accumulate many notes on a single item over time.

## Before starting

Detect the collection context by walking up from the current directory looking
for `.collection-index.yaml`. If not found, explain that this skill must run
inside a collection.

## The workflow

1. **Ask which item to add notes to.** The user provides the item's name or
   slug. Search `.collection-index.yaml` to find a match. If ambiguous (multiple
   partial matches), show the options and let the user pick. Confirm the match.

2. **Ask what to do:**

   - **Add a new note** — import a file as a new note
   - **Update/replace an existing note** — replace a specific note that's
     already in the item's `notes/` directory
   - **Cancel**

3. **For a new note:**

   a. Ask for the notes file path. Verify it exists and is readable.
   b. Ask for a short name for the note (used in the filename). Default:
      derive from the source filename.
   c. Generate the filename: `YYYY-MM-DD-{name}.{ext}` — date-prefixed
      so notes sort chronologically.
   d. Handle based on file type:

      **Markdown (`.md`):**
      Copy into `{item}/notes/` with the generated filename.

      **Plain text (`.txt`):**
      Copy into `{item}/notes/` with `.md` extension (plain text renders
      fine as markdown).

      **PDF (`.pdf`) or other binary formats:**
      Refuse with a plain-English explanation: notes are for the user's
      own writing about an item, which should be text (markdown or plain
      text) so it can be read and edited by any tool. If the user has a
      PDF they want alongside the item, suggest placing it in the item
      directory as content (not in `notes/`) — it lives with the item's
      other files. If they want text *about* the PDF, write it as
      markdown.

      **Other formats:**
      Explain that supported formats are `.md` and `.txt`. Offer to
      treat the file as plain text if appropriate.

   e. Create the `notes/` directory if it doesn't exist yet.

4. **For updating an existing note:**

   a. List the notes currently in `{item}/notes/`.
   b. Let the user pick which note to replace.
   c. Ask for the replacement file path.
   d. Copy the new file over the existing one (same filename).

5. **Confirm what was done.** Tell the user the note's filename and that it
   will appear on the item's wiki page after regenerating.

6. **Suggest regenerating the wiki:**

   > Note saved. To see it in the wiki, regenerate it:
   >
   > ```
   > uv run python tools/generate_wiki.py .
   > ```
   >
   > Or use `/coll-menu` → regenerate wiki.

## How notes appear in the wiki

Each item's wiki page has a "Notes" section that shows all notes from the
`notes/` directory, sorted chronologically by filename. Notes are text
(markdown or plain text) and render inline on the item's wiki page.

## The notes/ directory

```
causal-inference-primer/
├── metadata.yaml
├── README.md
├── original.pdf
└── notes/
    ├── 2026-04-14-reading-notes.md
    └── 2026-04-21-seminar-followup.md
```

Each note is independent. The user can:
- Edit any note directly in their text editor
- Delete a note by removing the file
- Rename a note (the date prefix keeps sort order)

## What this does NOT do

- Does not create or edit notes — the user writes them externally
- Does not accept PDFs or other binary formats (notes are the user's own
  writing, stored as text)
- Does not modify the item's metadata or README
