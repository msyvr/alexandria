# /coll-physical

Create a catalog record for a physical item (or other physical item) the user owns. No
content is copied — the item lives on a shelf; this directory becomes its entry in the
library. Photo-based creation is the primary path; manual entry is supported as a
fallback or supplement.

Every item created by this skill conforms to the universal item shape (see
`docs/coll/book-shape.md` in the alexandria repo).

## Before starting

Detect the collection context by walking up from the current directory looking for
`.collection-index.yaml`. If not found, explain that /coll-physical must run inside an
alexandria collection and offer to help create one with /coll.

Read the collection index to understand existing sections; you'll need them for
classification.

## The workflow

Four things need to happen, in a conversational flow — not a rigid sequence:

1. **Gather intent and input** — what's being cataloged and how
2. **Extract candidates** — produce a list of draft item records
3. **Confirm, edit, optionally enrich** — user reviews each candidate
4. **Classify, create, record** — write the item directories and update the index

### 1. Gather intent and input

Ask the user what they're cataloging. The primary options:
- **A photo of one item** — fastest path for a single item
- **A photo of a shelf** — multiple items from one photo
- **Manual entry** — type in title and author by hand
- **Manual entry plus a photo** — preserve a visual record alongside hand-entered metadata

Photo and manual entry can coexist in a single invocation: a shelf photo might yield
three clean extractions, one that needs manual correction, and one that's unidentifiable
— all handled in one workflow.

If the user wants to skip per-item confirmation and accept all clean extractions as-is,
they can opt into **yolo mode** here. This is for batch-cataloging a large shelf when
the user trusts the extraction. Yolo still requires user input for partial or failed
extractions — it means "trust the clean ones," not "guess."

If a photo is involved, ask for the file path. Verify the file exists and the format is
supported (JPEG, PNG, HEIC, WebP). If the format isn't supported or the file is
unreadable, explain and ask for a different file or offer to switch to manual entry.

### 2. Extract candidates

The goal: produce a list of candidate items, each with draft metadata.

**From a photo**: use vision to identify visible items and extract what's legible —
title, author, publisher, ISBN, edition, publication date. A single-item photo usually
yields one candidate; a shelf photo yields one candidate per identifiable spine.

Candidates vary in confidence:
- **Clean**: title and author both clear
- **Partial**: one field clear, another missing or unclear
- **Failed**: an item is visible but nothing is legible (mark as "needs manual entry")

**From manual entry**: collect what the user provides. Both paths produce the same
candidate structure.

**Failure modes**:
- Photo contains no items (or is unrelated): report this, offer a different photo or
  manual entry. Don't silently fail.
- No items visible in a shelf photo: same handling.
- Extraction fails for specific items within a shelf: continue with the successful
  ones and flag the failures for manual entry.

### 3. Confirm, edit, optionally enrich

**Media type**: each item's metadata includes a `media_type` field. Default suggestions
are `text:hardcover` for photographed items, but common options include `text:paperback`,
`text:magazine`, `text:journal`, `audio:vinyl`, `audio:cd`, `video:dvd`, `video:blu-ray`,
`image:photograph`, `image:print`, or `other`.

- **Single-item photo**: ask the user once for the media_type with a default suggestion
- **Shelf photo**: ask once for a shelf-level default (applied to all candidates), with
  per-item override available during confirmation. Shelves are typically homogeneous —
  one question covers the batch. A mixed shelf is rare; override is there when needed.
- **Shortcut skills** (`/coll-hardcover`, `/coll-paperback`): media_type is pre-set by the
  shortcut; this question is skipped entirely.

**Default confirmation**: for each candidate, show the draft metadata (including
media_type) and ask the user to confirm, edit fields, or skip. A skipped candidate
doesn't become an item. A failed extraction requires manual entry before it can be
confirmed.

**Yolo mode** (if opted in at step 1): clean extractions are accepted automatically.
Partial and failed extractions still require user input.

**Enrichment** is a single batch decision after candidates are confirmed. Ask once:

> "For these N items, want me to fetch public metadata (title, author, publisher,
> subjects, short description) from Open Library? Options: yes / no / choose per book."

- **Yes**: fetch for all confirmed items, present results, let the user accept-all or
  edit individual records.
- **No**: skip enrichment entirely. Nothing is sent externally.
- **Choose per item**: offer the choice per candidate.

Default is to ask (not to auto-enrich). Privacy-first users can answer "no" and nothing
goes to external services. Item content is never fetched — only bibliographic metadata
from open book databases.

### 4. Classify, create, record

For each confirmed (and possibly enriched) item:

**Propose a major section and section**. Major section is the top-level grouping on
the By section wiki view (`Books`, `Research papers`, `Visual`, `Audio`, `Personal`,
`Etc` — user can supply a custom name). Section is the specific subsection (e.g.,
`fiction`, `photographs`). The same subsection name can live under different majors,
so both must be captured.

Base the proposals on existing collection sections, the item's subject if known from
enrichment, and recent placements of similar items. If the batch came from a single
shelf photo, propose one major + section as the shelf-level default and let the user
accept it or override per item. If the user wants a new section, create it.

**Generate a slug** from the title per the rules in docs/coll/book-shape.md
(lowercase, non-alphanumeric to hyphens, truncate to ~50 chars). Check uniqueness
against existing slugs in the collection; suffix with `-2`, `-3` if needed.

**Create the item directory** at `{library}/{section}/{slug}/`.

**Write the four files the universal item shape requires**:

- `metadata.yaml` — the catalog entry (template below)
- `README.md` — the item's spine (template below)
- `photo.{ext}` — the source photo, preserved by default. If the user opted out of
  preservation, omit this file and remove the `photo:` field from metadata.yaml.

No CLAUDE.md is generated for physical items. The metadata.yaml is self-documenting
and Claude can derive operational context from it directly.

**Update `.collection-index.yaml`** with the item's universal fields (one entry under its
section). For shelf batches, update once at the end rather than per item.

**Commit the item to the collection's git repo** (silent no-op if version control
isn't enabled). Once per invocation, after all item files and the index are written.
For a single item:

```
uv run python tools/commit_change.py {collection_path} \
  --message "Add physical item: {title}" \
  .collection-index.yaml \
  {section}/{slug}
```

For a shelf batch, use a single commit with a batch message like
`"Add {N} physical items from shelf photo"`.

**Invoke /coll-notes** once at the end of the invocation to log the acquisition batch
to `collection-context.md`. Include: how many items were added, what workflow was used,
any notable user preferences observed (e.g., "user prefers no online enrichment").

## metadata.yaml template

```yaml
# Universal fields
slug: "{generated-slug}"
title: "{confirmed title}"
book_type: "physical"
major_section: "{selected major section}"
section: "{selected section}"
description: "{generated from available fields — see below}"
date_added: "{today's date, YYYY-MM-DD}"
form: "physical"
media_type: "text:hardcover"          # or text:paperback, audio:vinyl, etc.
status: "active"

# Universal optional
author: "{author if known}"
acquired_at: "{YYYY-MM-DD, if the user knows when they got this item}"
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

## README.md template (the item's spine)

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

## Adapting to the user

Use plain language. "Photograph" not "image capture." "Catalog entry" not "metadata
record." When extraction is uncertain, say so directly: "I couldn't read the bottom two
items clearly — can you tell me what they are?"

When first using vision AI, briefly explain: "I'll look at your photo and identify the
title and author for each item I can see. You'll review what I find before anything is
saved."

Respect privacy defaults. Never push online enrichment as the "better" option; present
it as one of several choices with the recommendation depending on the user's
preferences.

## Privacy and data handling

- **Photos go to the vision LLM only** (Claude by default; eventually a local vision
  model when that path is ready). Photos are never sent to book databases or third-party
  OCR services.
- **Enrichment fetches public bibliographic metadata only** — title, author, publisher,
  subjects, short description. Never item content.
- **Photos are preserved locally by default** in the item's directory. Users can opt
  out. They are never uploaded anywhere beyond the vision LLM call.

## What /coll-physical does not do

- Does not digitize or copy item content
- Does not store more than a short description from online enrichment
- Does not send photos anywhere except the vision LLM that's extracting metadata
