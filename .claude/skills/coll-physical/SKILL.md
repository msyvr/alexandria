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

### 3.5. Ask for optional personal notes

Before writing the item, offer the user an optional personal-notes slot:

> Any personal notes you'd like to attach to this item? A reaction,
> why you have it, what you think of it, what to remember — anything
> you'd want to see again when you revisit the item. Press Enter to
> skip, or type/paste your notes (multi-line is fine).

If the user provides anything, record it verbatim as the `user_notes`
field in `metadata.yaml` and as a **## Personal notes** section in the
item's README. See the README template below. If the user skips, omit
both.

For shelf batches, ask once at the start whether per-item personal
notes should be prompted or skipped for the batch, then act accordingly.

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
author: "{canonical name only — e.g., 'Lawrence Kasdan', not 'Directed by Lawrence Kasdan'}"
author_role: "{role as it would be phrased before the name — Director, Author, Writer, Artist, Performer, Composer, Photographer, Producer, Illustrator, Translator, Editor, Narrator, Curator. Infer from media_type when possible: video:* → Director, audio:* (music) → Artist, image:* → Photographer, text:* → Author. Ask the user if ambiguous.}"
date_created: "{the date the work itself was made — publication date for books, release year for films, date taken for photos, etc.; ISO date, year+month, or just year}"
acquired_at: "{YYYY-MM-DD, if the user knows when they got this item}"
user_notes: |
  {optional — freeform personal notes the user provided (see step 3.5 below).
  Can be multi-line; use a YAML block scalar if so. Stored verbatim.}
provenance:
  source: "{e.g., 'Photographed from personal shelf, 2026-04-10'}"
  notes: "{user-provided context, or omit entirely}"

# Physical-specific (all optional; omit rather than include empty strings)
photo: "photo.jpg"
shelf_location: "{freeform, if user provided}"
isbn: "{if known}"
edition: "{if known}"
publisher: "{if known}"
publication_date: "{if known — same as date_created for books; keep both if the semantics feel distinct, otherwise use date_created alone}"
```

**Description generation**: compose a short natural-prose description (1–3
sentences) that reads on its own. The grid already shows title, author,
role, date, format, section, and shelf; so the description focuses on
**subject, premise, and notable context** — what the item is *about*, not
the catalog attributes.

Template: `{subject/genre phrase}{, optional one-sentence premise}{, optional tail of notable secondary credits or context}`

Loose scope: light repetition with grid fields is fine when the grammar
wants it. The rule is "read naturally," not "zero overlap."

Per-type guidance:

- **Book (fiction)**: genre + plot premise + (optional) notable edition/translator/series
  - e.g. *"Anarchist utopia novel set between twin worlds. Core of Le Guin's Hainish Cycle; this 2003 Eos edition includes the author's 1975 afterword."*
- **Book (non-fiction)**: subject area + thesis or approach + (optional) notable context
  - e.g. *"Biography of Alan Turing, tracing his cryptanalytic work at Bletchley Park through his death. Draws on Hodges's decade of archive research; includes the 2014 afterword on post-conviction reappraisals."*
- **Film / DVD / Blu-ray**: genre + plot hook + (optional) notable cast, cinematographer, production context
  - e.g. *"Romantic comedy: a woman chases her straying fiancé across Paris and gets tangled with a charming thief. Meg Ryan, Kevin Kline, Timothy Hutton, Jean Reno; cinematography by Owen Roizman."*
- **Music (vinyl, CD, tape)**: genre + concept or era + (optional) featured players, producers
  - e.g. *"Folk-rock concept album woven around the Port of Seattle shipyard strike of 1919. Produced by Joe Henry; Rosanne Cash features on two tracks."*
- **Other physical objects (art prints, ephemera)**: kind + subject + (optional) provenance/context
  - e.g. *"Letterpress poster commemorating the 1968 Olympia type foundry. One of 250; signed by the designer."*

Fallback when little is known: empty description (the item page simply
won't render a description line).

## README.md template (the item's spine)

The README is both the wiki's content source and a standalone readable
document on disk (for browsing an item's directory in a markdown reader
without alexandria). The layout follows the catalog-style convention:
identification → reference card → body. The two `<!-- alexandria:metadata-*
-->` HTML comments are invisible in rendered markdown but act as
deterministic delimiters for the wiki generator's stripper — everything
between them is dropped from the wiki item page because the page already
renders those fields as a structured grid.

Byline wording is role-aware: use the `author_role` to phrase it
(`*Directed by Lawrence Kasdan*`, `*Photographed by Ansel Adams*`,
`*by Ursula Le Guin*` for default Author). If role is absent or equals
`Author`, use `*by {author}*`; otherwise use `*{role}ed by {author}*`
(Director → "Directed by", Producer → "Produced by", etc. — the skill
knows the conjugation for the recommended role vocabulary).

```markdown
# {title}

{if author:} *{role-aware byline}*

{description}

{if photo preserved:}
![{title}](photo.jpg)

<!-- alexandria:metadata-start -->

## Catalog entry

- **Title**: {title}
- **{role-aware author label}**: {author}
- **Created**: {date_created if known}
- **Acquired**: {acquired_at if known}
- **Added**: {date_added}
- **Section**: {major_section} / {section}
- **Format**: {media_type} ({form})
- **Publisher**: {publisher if known}
- **ISBN**: {isbn if known}
- **Edition**: {edition if known}
- (any other type-specific fields that make sense as a labelled list entry)

{if shelf_location:}
## Shelf location

{shelf_location}

<!-- alexandria:metadata-end -->

{if editorial body appropriate:}
## About

{body — subject summary, plot discussion, notable context, etc. Keep to
the informational/editorial register; no catalog repetition.}

{if user_notes:}
## Personal notes

{user_notes, verbatim — whatever the user provided in step 3.5, preserving
line breaks. No editing, no summarizing.}

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
