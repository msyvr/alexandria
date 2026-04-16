# /coll-notes

Save persistent context for an alexandria item or library: decisions, user preferences,
session history, open questions, and useful Q&A. Maintains the item's `context.md` (or
the collection's `collection-context.md`) and updates the "Recent context" summary in CLAUDE.md.

## Detection

Walk up from the current directory looking for `.collection-index.yaml` (the only definitive
marker that we're inside an alexandria collection):

1. **`.collection-index.yaml` found in an ancestor:**
   - If the current directory IS the collection root → target is `collection-context.md` at the
     collection root
   - If the current directory is (or is inside) one of the items listed in the index →
     target is that item's `context.md`
   - Otherwise (inside the collection tree but not in a recognized item) → explain to the
     user and exit

2. **No `.collection-index.yaml` found in any ancestor** → not an alexandria context.
   Explain that take-notes is for alexandria libraries and exit.

## Process

1. Locate the target file (`context.md` for an item, `collection-context.md` for the collection
   root) using detection above. If it doesn't exist yet, create it with this initial
   structure:

   ```markdown
   # Context: {item or library name}

   Interaction history, decisions, and observed user preferences.
   This file is updated automatically when significant work is done. You can read and
   edit it freely — it's plain markdown.
   ```

2. Search backward in the file for `SESSION_NOTES_CHECKPOINT`:
   - If found: scope notes to what happened AFTER that point
   - If not found: scope notes from the start of the current session

3. **Invite a personal note.** Offer the user a chance to add free-form
   text to this checkpoint — this is how they add personal details to
   the journal timeline rendered in the wiki. Ask, verbatim or close
   to it:

   > Anything you want to add to this checkpoint as a personal note?
   > Thoughts, plans, reactions, reminders — anything you want to see
   > in the journal later. (Press Enter to skip, or type / paste your
   > note.)

   Record exactly what the user types, preserving line breaks. If the
   user presses Enter with no input, treat this as "no personal note"
   and omit the **Personal notes** field from the checkpoint below.

4. Decide what to record under each category, using best judgment:
   - **Accomplished**: what was done in this session (concrete, brief)
   - **Decisions**: choices made with their rationale (or "none")
   - **User preferences**: patterns observed about how this user thinks about this domain
     (or "none new")
   - **Open questions**: unresolved items the user mentioned but didn't act on (or "none")
   - **Q&A worth keeping**: substantive questions and answers, with links to where the
     answer was filed if it became part of the item (or "none")

   Only record what's actually useful for future sessions. Don't pad. "None" is a fine
   answer for any section.

5. Append to the target file. Include the **Personal notes** field only
   if the user provided text in step 3 — otherwise omit that line
   entirely:

   ```markdown

   ## [YYYY-MM-DD HH:MM] Checkpoint

   **Accomplished:** {what was done}

   **Personal notes:** {user's text from step 3 — include only if provided}

   **Decisions:** {decisions with rationale, or "none"}

   **User preferences:** {patterns observed, or "none new"}

   **Open questions:** {unresolved items, or "none"}

   **Q&A worth keeping:** {substantive Q&A, or "none"}

   SESSION_NOTES_CHECKPOINT
   ```

6. Update the "Recent context" section in the same directory's CLAUDE.md (if a CLAUDE.md
   exists). Replace its contents with a 3-5 line summary of the checkpoint just appended:
   the most important accomplishment, the most important decision (if any), and the most
   important user preference (if any). Keep it terse — this section is auto-loaded into
   every session and burns context.

   If CLAUDE.md exists but has no "Recent context" section, add one immediately before
   the final "For full decision history..." pointer.

7. End your response with exactly:

SESSION_NOTES_CHECKPOINT
