# /take-notes

Save persistent context for an alexandria book or library: decisions, user preferences,
session history, open questions, and useful Q&A. Maintains the book's `context.md` (or
the library's `library-context.md`) and updates the "Recent context" summary in CLAUDE.md.

## Detection

Walk up from the current directory looking for `.library-index.yaml` (the only definitive
marker that we're inside an alexandria library):

1. **`.library-index.yaml` found in an ancestor:**
   - If the current directory IS the library root → target is `library-context.md` at the
     library root
   - If the current directory is (or is inside) one of the books listed in the index →
     target is that book's `context.md`
   - Otherwise (inside the library tree but not in a recognized book) → explain to the
     user and exit

2. **No `.library-index.yaml` found in any ancestor** → not an alexandria context.
   Explain that take-notes is for alexandria libraries and exit.

## Process

1. Locate the target file (`context.md` for a book, `library-context.md` for the library
   root) using detection above. If it doesn't exist yet, create it with this initial
   structure:

   ```markdown
   # Context: {book or library name}

   Interaction history, decisions, and observed user preferences.
   This file is updated automatically when significant work is done. You can read and
   edit it freely — it's plain markdown.
   ```

2. Search backward in the file for `SESSION_NOTES_CHECKPOINT`:
   - If found: scope notes to what happened AFTER that point
   - If not found: scope notes from the start of the current session

3. Decide what to record under each category, using best judgment:
   - **Accomplished**: what was done in this session (concrete, brief)
   - **Decisions**: choices made with their rationale (or "none")
   - **User preferences**: patterns observed about how this user thinks about this domain
     (or "none new")
   - **Open questions**: unresolved items the user mentioned but didn't act on (or "none")
   - **Q&A worth keeping**: substantive questions and answers, with links to where the
     answer was filed if it became part of the book (or "none")

   Only record what's actually useful for future sessions. Don't pad. "None" is a fine
   answer for any section.

4. Append to the target file:

   ```markdown

   ## [YYYY-MM-DD HH:MM] Checkpoint

   **Accomplished:** {what was done}

   **Decisions:** {decisions with rationale, or "none"}

   **User preferences:** {patterns observed, or "none new"}

   **Open questions:** {unresolved items, or "none"}

   **Q&A worth keeping:** {substantive Q&A, or "none"}

   SESSION_NOTES_CHECKPOINT
   ```

5. Update the "Recent context" section in the same directory's CLAUDE.md (if a CLAUDE.md
   exists). Replace its contents with a 3-5 line summary of the checkpoint just appended:
   the most important accomplishment, the most important decision (if any), and the most
   important user preference (if any). Keep it terse — this section is auto-loaded into
   every session and burns context.

   If CLAUDE.md exists but has no "Recent context" section, add one immediately before
   the final "For full decision history..." pointer.

6. End your response with exactly:

SESSION_NOTES_CHECKPOINT
