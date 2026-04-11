# /new-author

Create an author book — a container for content you write yourself. Notes, research,
drafts, project plans, task lists, journal entries, essays, or any other form of
personal writing you want to organize and keep in your library.

Unlike other book types:
- **/new-physical** catalogs a book you own in physical form (no content copied)
- **/new-digital** brings in digital content from elsewhere (files, URLs, pasted text)
- **/new-scout** has AI build a knowledge base for you through a seven-phase process
- **/new-author** creates an empty structure you fill in yourself

Author books are the simplest type to create: the skill sets up the book's structure
(universal files + a starter README suited to your purpose) and hands off to you for
writing. Claude Code can help you draft, review, or organize content later — but the
content itself is yours.

Every author book conforms to the universal book shape (see
`docs/library/book-shape.md`).

## Before starting

Detect the library context by walking up from the current directory looking for
`.library-index.yaml`. If not found, explain that /new-author must run inside an
alexandria library and offer to help create one with /library.

## The workflow

Three things need to happen, conversationally:

1. **Gather intent** — what the user is writing and what kind of structure fits
2. **Classify** — which section the book belongs in
3. **Create and hand off** — write the universal files, tell the user where to start

### 1. Gather intent

Ask the user what they're working on. Then ask what kind of writing this is — this
determines the starter README structure and the `purpose` metadata field:

- **project**: a focused working project (a thesis, a startup idea, a course of study,
  a hobby build). Typically has multiple related documents and an evolving state.
- **collection**: a set of individual items sharing a theme (essays, recipes, short
  stories, reviews, travel logs). Each item is typically self-contained.
- **journal**: chronological entries — a reading log, research journal, daily notes,
  a scratchpad. Organized by date.
- **notes**: topical notes that don't fit the other shapes. Meeting notes, lecture
  notes, book notes, course notes. Organized by topic.
- **freeform**: the user explicitly doesn't want a suggested structure. Empty starter;
  they'll figure it out.

If the user isn't sure which purpose fits, recommend **notes** as the flexible default.
If they explicitly don't want any starter structure, use **freeform**.

### 2. Classify

Same as other book types: propose a section based on existing library sections and the
topic. Let the user confirm or choose a different section. If none of the existing
sections fit, offer to create a new one.

Generate a slug from the title (see `docs/library/book-shape.md` for rules). Check
uniqueness within the library; suffix with `-2`, `-3` if needed.

### 3. Create and hand off

Create the book directory at `{library}/{section}/{slug}/`.

Write the universal files:
- `metadata.yaml` (template below)
- `README.md` — starter template based on `purpose` (see templates below)
- `CLAUDE.md` — operational context for return sessions

Do **not** create content files or subdirectories automatically. The starter README
suggests a structure appropriate to the purpose (e.g., "consider a `notes/` subdirectory
for working notes"), but alexandria doesn't pre-create them. The user creates whatever
they actually need as they go.

Update `.library-index.yaml` with the new book's universal fields.

Invoke `/take-notes` once at the end to log the acquisition to `library-context.md`.

Tell the user where the book is and how to get started:

> Your author book is ready at `{section}/{slug}/`. Open `README.md` and start writing,
> or `cd` into the directory and create your own files. If you want me to help draft
> something, outline a structure, or review what you have, just ask.

## metadata.yaml template

```yaml
# Universal fields
slug: "{generated-slug}"
title: "{title the user provided}"
book_type: "author"
section: "{selected section}"
description: "{one-line description from the user, or a default from the title}"
date_added: "{today's date, YYYY-MM-DD}"
form: "digital"
media_type: "text:markdown"
status: "active"

# Universal optional
author: null                          # the user is the author; typically omitted
provenance:
  source: "User-authored content"
  notes: "{any notable context, or omit}"

# Author-specific
purpose: "project"                    # project, collection, journal, notes, or freeform
```

## README starter templates

Each starter is short, flexible, and suggestive rather than prescriptive. The user
edits it as they go.

### purpose: project

```markdown
# {title}

{description}

## About this project

(what this is, what you're trying to accomplish, current state)

## Structure

Suggestions for how to organize your work — create these as you need them:

- `notes/` — working notes, ideas, scratch work
- `drafts/` — work-in-progress drafts
- `refs/` — reference material and notes from sources

## Current focus

(what you're working on right now; update as the project evolves)

## Open questions

(things you're uncertain about; update and resolve as you learn)

## Recent progress

(log of meaningful progress; update as you go)
```

### purpose: collection

```markdown
# {title}

{description}

## About this collection

(what these items have in common, the thread that connects them)

## Items

(list items here as you add them, or organize by subtopic)

- Example: `my-first-essay.md` — a short description
```

### purpose: journal

```markdown
# {title}

{description}

## About

(what this journal is for, how often you write in it, conventions you follow)

## Entries

Chronological, newest first. Add entries as dated files (e.g., `2026-04-11.md`) or as
sections below.

### 2026-04-11

(your first entry goes here)
```

### purpose: notes

```markdown
# {title}

{description}

## About these notes

(what this collection of notes is for)

## Topics

Organize by topic as you accumulate notes. Example subheadings:

### Topic 1

(notes go here; or link to a separate file if they grow long)

### Topic 2

(etc.)
```

### purpose: freeform

```markdown
# {title}

{description}

(Start writing. Structure this however makes sense to you. Create additional files or
subdirectories as you need them.)
```

## CLAUDE.md template

```markdown
# {title}

An author book — content the user is writing themselves. Purpose: {purpose}.

## Details

- **Title**: {title}
- **Purpose**: {purpose}
- **Section**: {section}
- **Started**: {date_added}

## Files
- `metadata.yaml` — catalog entry
- `README.md` — the book's spine (currently the starter; user edits freely)
- `context.md` — interaction history (written by /take-notes)

Additional files and subdirectories are created by the user as needed. The README
suggests a structure appropriate to the purpose, but the user decides the actual shape.

## Helping the user

On return visits, the user may ask for help with:
- Drafting new content (a section, an essay, an entry)
- Reviewing what they've written (critique, structural feedback, line editing)
- Organizing existing content (restructuring, splitting files, creating an index)
- Tracking progress (updating the "current focus" or "recent progress" sections)

You can read any file in the book to understand the context. You can suggest changes,
but the user makes the edits. The content is theirs.

## Updating this record

- Edit `metadata.yaml` to change metadata fields
- Use `/library` to move the book to a different section or rename it
- Use `/take-notes` to log significant decisions or state

## Recent context

(updated automatically by /take-notes after significant work sessions)
```

## Adapting to the user

Use plain language. "Your writing" not "user-authored content." "Start with the README"
not "populate the initial document." When describing purposes, give concrete examples
tied to the user's own situation if possible.

Don't over-explain the structure. The user wants to start writing, not read documentation
about their writing space. Keep the creation conversation short (three questions max:
title, description, purpose). Classify the section, create the files, hand off.

## What /new-author does not do

- Does not pre-create subdirectories or content files beyond the universal files
- Does not impose a specific structure; the purpose-based starter is a suggestion
- Does not analyze or extract content from anywhere — this book type starts empty
- Does not fill the book with AI-generated content (that's a different tool; the
  user's writing is theirs)
