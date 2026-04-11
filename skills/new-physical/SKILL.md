# /new-physical

Create a catalog record for a physical book (or other physical item) the user owns. No
content is copied — the book lives on a shelf; this directory becomes its entry in the
library. Photo-based creation is the primary path; manual entry is supported as a
fallback or supplement.

Every book created by this skill conforms to the universal book shape (see
`docs/library/book-shape.md` in the alexandria repo).

## Before starting

Detect the library context by walking up from the current directory looking for
`.library-index.yaml`. If not found, explain that /new-physical must run inside an
alexandria library and offer to help create one with /library.

Read the library index to understand existing sections; you'll need them for
classification.

## The workflow

Four things need to happen, in a conversational flow — not a rigid sequence:

1. **Gather intent and input** — what's being cataloged and how
2. **Extract candidates** — produce a list of draft book records
3. **Confirm, edit, optionally enrich** — user reviews each candidate
4. **Classify, create, record** — write the book directories and update the index

### 1. Gather intent and input

Ask the user what they're cataloging. The primary options:
- **A photo of one book** — fastest path for a single item
- **A photo of a shelf** — multiple books from one photo
- **Manual entry** — type in title and author by hand
- **Manual entry plus a photo** — preserve a visual record alongside hand-entered metadata

Photo and manual entry can coexist in a single invocation: a shelf photo might yield
three clean extractions, one that needs manual correction, and one that's unidentifiable
— all handled in one workflow.

If the user wants to skip per-book confirmation and accept all clean extractions as-is,
they can opt into **yolo mode** here. This is for batch-cataloging a large shelf when
the user trusts the extraction. Yolo still requires user input for partial or failed
extractions — it means "trust the clean ones," not "guess."

If a photo is involved, ask for the file path. Verify the file exists and the format is
supported (JPEG, PNG, HEIC, WebP). If the format isn't supported or the file is
unreadable, explain and ask for a different file or offer to switch to manual entry.

### 2. Extract candidates

The goal: produce a list of candidate books, each with draft metadata.

**From a photo**: use vision to identify visible books and extract what's legible —
title, author, publisher, ISBN, edition, publication date. A single-book photo usually
yields one candidate; a shelf photo yields one candidate per identifiable spine.

Candidates vary in confidence:
- **Clean**: title and author both clear
- **Partial**: one field clear, another missing or unclear
- **Failed**: a book is visible but nothing is legible (mark as "needs manual entry")

**From manual entry**: collect what the user provides. Both paths produce the same
candidate structure.

**Failure modes**:
- Photo contains no books (or is unrelated): report this, offer a different photo or
  manual entry. Don't silently fail.
- No books visible in a shelf photo: same handling.
- Extraction fails for specific books within a shelf: continue with the successful
  ones and flag the failures for manual entry.

### 3. Confirm, edit, optionally enrich

**Media type**: each book's metadata includes a `media_type` field. Default suggestions
are `text:hardcover` for photographed books, but common options include `text:paperback`,
`text:magazine`, `text:journal`, `audio:vinyl`, `audio:cd`, `video:dvd`, `video:blu-ray`,
`image:photograph`, `image:print`, or `other`.

- **Single-book photo**: ask the user once for the media_type with a default suggestion
- **Shelf photo**: ask once for a shelf-level default (applied to all candidates), with
  per-book override available during confirmation. Shelves are typically homogeneous —
  one question covers the batch. A mixed shelf is rare; override is there when needed.
- **Shortcut skills** (`/new-hardcover`, `/new-paperback`): media_type is pre-set by the
  shortcut; this question is skipped entirely.

**Default confirmation**: for each candidate, show the draft metadata (including
media_type) and ask the user to confirm, edit fields, or skip. A skipped candidate
doesn't become a book. A failed extraction requires manual entry before it can be
confirmed.

**Yolo mode** (if opted in at step 1): clean extractions are accepted automatically.
Partial and failed extractions still require user input.

**Enrichment** is a single batch decision after candidates are confirmed. Ask once:

> "For these N books, want me to fetch public metadata (title, author, publisher,
> subjects, short description) from Open Library? Options: yes / no / choose per book."

- **Yes**: fetch for all confirmed books, present results, let the user accept-all or
  edit individual records.
- **No**: skip enrichment entirely. Nothing is sent externally.
- **Choose per book**: offer the choice per candidate.

Default is to ask (not to auto-enrich). Privacy-first users can answer "no" and nothing
goes to external services. Book content is never fetched — only bibliographic metadata
from open book databases.

### 4. Classify, create, record

For each confirmed (and possibly enriched) book:

**Propose a section**. Base the proposal on existing library sections, the book's
subject if known from enrichment, and recent placements of similar books. If the batch
came from a single shelf photo, propose one section as the shelf-level default and let
the user accept it or override per book. If the user wants a new section, create it.

**Generate a slug** from the title per the rules in docs/library/book-shape.md
(lowercase, non-alphanumeric to hyphens, truncate to ~50 chars). Check uniqueness
against existing slugs in the library; suffix with `-2`, `-3` if needed.

**Create the book directory** at `{library}/{section}/{slug}/`.

**Write the four files the universal book shape requires**:

- `metadata.yaml` — the catalog entry (template below)
- `README.md` — the book's spine (template below)
- `CLAUDE.md` — operational context for return sessions (template below)
- `photo.{ext}` — the source photo, preserved by default. If the user opted out of
  preservation, omit this file and remove the `photo:` field from metadata.yaml.

**Update `.library-index.yaml`** with the book's universal fields (one entry under its
section). For shelf batches, update once at the end rather than per book.

**Invoke /take-notes** once at the end of the invocation to log the acquisition batch
to `library-context.md`. Include: how many books were added, what workflow was used,
any notable user preferences observed (e.g., "user prefers no online enrichment").

## metadata.yaml template

```yaml
# Universal fields
slug: "{generated-slug}"
title: "{confirmed title}"
book_type: "physical"
section: "{selected section}"
description: "{generated from available fields — see below}"
date_added: "{today's date, YYYY-MM-DD}"
form: "physical"
media_type: "text:hardcover"          # or text:paperback, audio:vinyl, etc.
status: "active"

# Universal optional
author: "{author if known}"
provenance:
  source: "{e.g., 'Photographed from personal shelf, 2026-04-10'}"
  notes: "{user-provided context, or omit entirely}"

# Physical-specific (all optional; omit rather than include empty strings)
photo: "photo.jpg"
shelf_location: "{freeform, if user provided}"
isbn: "{if known}"
edition: "{if known}"
publisher: "{if known}"
publication_date: "{if known}"
```

**Description generation**: build a one-line description from available fields.
- Publisher + year: `"{title} by {author} ({publisher}, {year})"`
- Author only: `"{title} by {author}"`
- Year only: `"{title} ({year})"`
- Otherwise: `"Physical copy of {title}"`

## README.md template (the book's spine)

```markdown
# {title}

{if author:} *by {author}*

{description}

{if photo preserved:}
![{title}](photo.jpg)

{if enrichment summary accepted:}
## About

{short summary from Open Library, ≤500 words}

{if shelf_location:}
## Shelf location

{shelf_location}

## Catalog entry

- **Title**: {title}
- **Author**: {author or "—"}
- **Medium**: physical
- **Section**: {section}
- **Date added**: {date_added}
{include publisher, edition, ISBN, publication_date lines if known}

See `metadata.yaml` for the full catalog entry.
```

## CLAUDE.md template (operational context for return sessions)

```markdown
# {title}

A physical book record. The book itself is on a shelf; this directory is the library's
catalog entry for it.

## Details

- **Title**: {title}
- **Author**: {author or "—"}
- **Shelf location**: {shelf_location or "not recorded"}

## Files
- `metadata.yaml` — catalog entry
- `README.md` — the book's spine (what's displayed in views)
- `photo.jpg` — visual record (if present)
- `context.md` — interaction history (written by /take-notes on first use)

## Updating this record

- Edit `metadata.yaml` to change metadata fields
- Replace `photo.jpg` to update the visual record
- Use `/library` to move or re-classify

## Recent context

(updated automatically by /take-notes after significant work sessions)
```

## Adapting to the user

Use plain language. "Photograph" not "image capture." "Catalog entry" not "metadata
record." When extraction is uncertain, say so directly: "I couldn't read the bottom two
books clearly — can you tell me what they are?"

When first using vision AI, briefly explain: "I'll look at your photo and identify the
title and author for each book I can see. You'll review what I find before anything is
saved."

Respect privacy defaults. Never push online enrichment as the "better" option; present
it as one of several choices with the recommendation depending on the user's
preferences.

## Privacy and data handling

- **Photos go to the vision LLM only** (Claude by default; eventually a local vision
  model when that path is ready). Photos are never sent to book databases or third-party
  OCR services.
- **Enrichment fetches public bibliographic metadata only** — title, author, publisher,
  subjects, short description. Never book content.
- **Photos are preserved locally by default** in the book's directory. Users can opt
  out. They are never uploaded anywhere beyond the vision LLM call.

## What /new-physical does not do

- Does not digitize or copy book content
- Does not store more than a short description from online enrichment
- Does not send photos anywhere except the vision LLM that's extracting metadata
