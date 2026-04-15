# /coll-add-item-notes

Add personal notes to an item in your collection. You can write notes in any
text editor and bring them in here — markdown, plain text, or PDF.

## Before starting

Detect the collection context by walking up from the current directory looking
for `.collection-index.yaml`. If not found, explain that this skill must run
inside a collection.

## The workflow

1. **Ask which item to add notes to.** The user provides the item's name or
   slug. Search `.collection-index.yaml` to find a match. If ambiguous (multiple
   partial matches), show the options and let the user pick. Confirm the match.

2. **Ask for the notes file.** The user provides the path to their notes file.
   Verify it exists and is readable.

3. **Handle based on file type:**

   **Markdown (`.md`):**
   - Copy the file into the item's directory as `notes.md`
   - If `notes.md` already exists, ask the user: replace it, append to it, or
     cancel?
   - The wiki will render this as a "Notes" section on the item's page

   **Plain text (`.txt`):**
   - Read the content and convert to simple markdown: wrap each paragraph
     (separated by blank lines) in its own block, preserve line breaks within
     paragraphs
   - Save as `notes.md` in the item's directory
   - If `notes.md` already exists, same replace/append/cancel choice
   - The wiki will render this the same as any other markdown notes

   **PDF (`.pdf`):**
   - Copy the file into the item's directory as `notes.pdf`
   - If `notes.pdf` already exists, ask the user: replace or cancel?
   - The wiki will link to the PDF from the item's page (PDFs can't be rendered
     inline in static HTML)

   **Other formats:**
   - Explain that the supported formats are `.md`, `.txt`, and `.pdf`
   - Offer to treat the file as plain text if the user wants

4. **Confirm what was done.** Tell the user where the notes file was saved and
   how it will appear in the wiki.

5. **Suggest regenerating the wiki** so the notes appear on the item's page:

   > Notes saved. To see them in the wiki, regenerate it:
   >
   > ```
   > uv run python ~/alexandria/tools/generate_wiki.py ~/my-collection
   > ```
   >
   > Or use `/coll-menu` → regenerate wiki.

## Appending notes

When the user chooses to append (for `.md` and `.txt` files when `notes.md`
already exists):

- Add a horizontal rule (`---`) and a timestamp header before the new content:

  ```markdown
  ---

  *Added YYYY-MM-DD:*

  {new content}
  ```

- This preserves the existing notes and makes it clear where new content starts.

## What this does NOT do

- Does not create or edit notes — the user writes them in their preferred editor
- Does not convert PDF content to text (the PDF is preserved as-is)
- Does not modify the item's metadata or README
