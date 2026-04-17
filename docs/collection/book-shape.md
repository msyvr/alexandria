# Universal item shape

Every item in an alexandria collection follows the same outer shape, regardless of item type. This contract makes items interchangeable at the collection level: the catalog can iterate over them, views can render them, skills can operate on them, and new item types can plug into the existing infrastructure without redesigning the foundation.

This document specifies the shape. Item types define their own content within it.

## Design principles

- **Minimum mandatory, nothing speculative.** Every required field has a defined consumer today.
- **metadata.yaml is the source of truth.** The collection-level `.collection-index.yaml` is a regenerable cache derived from every item's `metadata.yaml`.
- **Filesystem structure is not duplicated in metadata.** If the information is in the directory path, it doesn't also live in a field. (One exception: `section` is kept in metadata so the index cache doesn't require filesystem walks.)
- **Hand-editable.** A user should be able to open `metadata.yaml` in a text editor, change a field, and have the collection pick up the change.

## Item directory shape

Every item directory contains these files at acquisition time:

```
{item-slug}/
├── README.md           # the spine: what this item is, readable standalone
├── metadata.yaml       # the catalog entry (universal + type-specific fields)
└── ... type-specific content files ...
```

Files created on first use or only for certain item types:

```
{item-slug}/
├── CLAUDE.md           # operational context (scouts only — see below)
└── context.md          # interaction history, written by /coll-notes
```

**README.md** (required): the item's spine. A reader should be able to open it and understand what this item is, what's in it, and how to navigate its contents, without any other context. Each item type provides its own README template; scouts generate a rich overview, physical items show metadata and (if present) a photo, digital items show provenance and content.

**metadata.yaml** (required): the catalog entry (see schema below).

**CLAUDE.md** (optional — required for scouts, omitted for simple items): operational context for Claude Code when the user returns to the item in a future session. Scouts need this because they have complex operational context (schema, scripts, update commands, lens definitions). Physical and digital items don't need it — their metadata.yaml is self-documenting and Claude can derive everything it needs from there. See `.claude/skills/coll-new-scout/SKILL.md` for the scout CLAUDE.md template.

**context.md** (optional): interaction history written by `/coll-notes`. Created on first invocation. Contains decisions, user preferences, session log, open questions, and useful Q&A. Universal format across all item types.

**Type-specific content files**: whatever the item type needs. Scouts have `data/entries.yaml`, `scripts/`, `docs/`, and a generated `README.md`. Physical items might have a `photo.jpg`. Digital items might have an `original.pdf` plus a markdown extraction.

## metadata.yaml universal schema

### Required fields

```yaml
slug: "condition-x-treatments"        # unique within library; matches directory name
title: "Condition X Treatments"       # display name, any characters
book_type: "scout"                    # physical, digital, or scout
major_section: "Research papers"      # top-level grouping (user-customizable)
section: "ai safety"                  # specific subsection within the major
description: "Living knowledge base tracking treatment options."  # one line
date_added: "2026-04-10"              # ISO 8601 date
form: "digital"                       # digital or physical
media_type: "text:markdown"           # hierarchical format: {content_type}:{format}
status: "active"                      # active or removed
```

### Optional fields

```yaml
author: "Ursula Le Guin"              # semantics vary by item type (see below)
user_notes: "Essential reference."     # freeform personal notes about this item
provenance:
  source: "Personal collection"       # freeform string — where this came from
  notes: "Inherited from family"      # freeform string — any acquisition context
removed_at: "2026-05-01"              # ISO date; only if status == removed
removed_reason: "Superseded"          # freeform; only if status == removed
```

### Type-specific fields

Item types define their own fields at the top level of the same file, after the universal fields. No nesting ceremony. Example for scout:

```yaml
# ... universal fields above ...
settled: false                        # true if the scout has been frozen as static
settled_at: "2026-05-15"              # ISO date; only present if settled == true
```

For scouts, the `settled` field captures whether the scout is live (updating via discovery) or frozen as a static reference. Settling is a first-class action in the /coll skill — see `.claude/skills/coll/SKILL.md`. The wiki renders settled scouts inline like other static item types, while live scouts link out to their own presentation.

## Field semantics

### `slug` (required, string)

URL-and-filename-safe identifier for the item. Generated from the title:
- Lowercase
- Non-alphanumeric characters replaced with hyphens
- Multiple consecutive hyphens collapsed
- Leading/trailing hyphens removed
- Truncated to ~50 characters if needed

Must be **unique within the collection**. The `/coll` acquisition process checks existing slugs and appends a numeric suffix if needed (`-2`, `-3`, etc.). The item's directory name matches its slug.

### `title` (required, string)

Display name. Any characters allowed. Shown in catalog views and used as the `<title>` in generated HTML.

### `book_type` (required, enum)

One of:
- `physical` — a record of a physical item the user owns (no content files; the item lives on a shelf)
- `digital` — digital content the user has brought into the collection (local files, URLs, pasted text, including the user's own work)
- `scout` — a living, AI-maintained knowledge base

This determines which creation skill was used and what type-specific fields to expect.

### `major_section` (required, string)

The top-level grouping this item belongs to. Used on the By section wiki view to organize sections into broader categories.

**Default set** (user-customizable):
- `Books` — fiction, nonfiction, poetry, reference, technical, textbooks, essays, magazines
- `Research papers` — peer-reviewed and preprint academic work, theses
- `Visual` — photographs, images, art, illustrations, drawings, video, films, dvds, blu-ray
- `Audio` — music, podcasts, recordings, cds, vinyl, tapes
- `Personal` — journals, diaries, letters, correspondence, travel, notes
- `Etc` — anything that doesn't fit the above

The user can pick from this set or supply a custom name. Skills offer the default options at acquisition time but accept any string. The wiki generator renders known majors in the default order above, then any custom majors alphabetically.

Note: `major_section` is stored on the item because the same topic name (e.g., "ai safety") can live under multiple majors (`Books / ai safety` vs. `Research papers / ai safety`). Storing the major explicitly removes the ambiguity.

### `section` (required, string)

The specific subsection within the major. Matches a directory at the collection root (e.g., `fiction`, `ai safety`, `photographs`). Required.

If the acquisition process can't determine a section, it defaults to `"unsorted"` and the user can move it later.

Note: `section` duplicates information from the directory path. It's kept in metadata so the `.collection-index.yaml` cache doesn't require walking the filesystem on every read. This is a deliberate exception to the "don't duplicate filesystem structure" principle.

### `description` (required, string)

One-line summary. Target ~150 characters, maximum ~300. Shown in catalog and index views without opening the item. Should convey what the item is and why the user has it.

### `date_added` (required, ISO 8601 date)

The date the item was added to the collection. Format: `YYYY-MM-DD`. Set automatically on acquisition; never changed by normal operations.

### `form` (required, enum)

One of:
- `digital` — content exists as files in the item directory
- `physical` — content exists in the physical world; the catalog entry is a record

Binary. There is no `both` value for v1. If a user has the same work in both forms, they create two entries with no cross-reference. Linking is a deferred feature.

### `media_type` (required, hierarchical string)

Describes what the object structurally IS — its format. Not its purpose or content. Format: `{content_type}:{format}`, parseable on the colon.

**Content types**: `text`, `audio`, `video`, `image`.

**V1 vocabulary** (illustrative, extensible):

Text formats:
- `text:hardcover` (hardbound item)
- `text:paperback` (softcover item)
- `text:magazine`
- `text:journal` (academic or scientific)
- `text:manuscript` (bound writing)
- `text:unbound` (loose pages, folio, fragments)
- `text:pdf`
- `text:epub`
- `text:html` (saved web page)
- `text:markdown`
- `text:plaintext`

Audio formats:
- `audio:vinyl`
- `audio:cassette`
- `audio:cd`
- `audio:digital` (mp3, flac, etc.)

Video formats:
- `video:vhs`
- `video:dvd`
- `video:blu-ray`
- `video:digital`

Image formats:
- `image:photograph` (physical print)
- `image:print` (artwork, poster, physical image)
- `image:digital`

**Browsing uses**: exact match for specific filters ("my vinyl" → `audio:vinyl`); prefix match on content type for broad filters ("all my audio" → `audio:*`).

**media_type is about structural format, not purpose**. A PDF encyclopedia has `media_type: text:pdf` (it's a PDF). A hardcover encyclopedia has `media_type: text:hardcover` (it's a hardcover). The "encyclopedia" nature is about content — captured in title, description, or user tags — not in the format field.

**Defaults by item type**:
- `physical`: asked during acquisition (common options: hardcover, paperback, magazine, vinyl, cd, dvd, other)
- `digital`: inferred from file extension (`.pdf` → `text:pdf`, `.mp3` → `audio:digital`, etc.)
- `scout`: `text:markdown` (scouts are structurally markdown files)

### `status` (required, enum)

One of:
- `active` — the item is part of the live library (default)
- `removed` — the resource has been weeded; the catalog entry persists as a historical record

There is no `archived` status. Archiving is accomplished by moving an item to an `_archive/` section, not by changing status. Removal (via weeding) sets `status: removed` — see `/coll` weeding actions.

### `author` (optional, string)

Semantics vary by item type:
- **physical**: the literal author of the physical item (e.g., "Ursula K. Le Guin")
- **digital**: the author(s) of the digital source; for papers with many authors, use "First Author et al."
- **scout**: typically omitted; scouts are aggregated rather than authored

For the user's own work (imported via `/coll-digital`), set author to the user's name or leave it null — the provenance notes can capture that the user created it.

When null or omitted, catalog views display "—" or skip the author display.

### `user_notes` (optional, string)

Freeform personal notes about this item — why the user has it, what it's useful for, anything the user wants to record for their own reference. Unlike `description` (which is a one-line summary for catalog views), `user_notes` can be any length and is for the user's own use.

Examples:
- "Essential reference for the first six months of treatment decisions"
- "Borrowed from Maya — return by June"
- "Chapters 3 and 7 are the most relevant to my project"
- "Companion to the hardcover on the top shelf"

Shown on the item's wiki page when present. Not shown in index/catalog card views (those use `description`). The user can add or edit this at any time by editing `metadata.yaml`.

### `provenance` (optional, object)

Acquisition context. Minimum structure is two freeform string fields:

```yaml
provenance:
  source: "..."       # where this came from
  notes: "..."        # any additional acquisition context
```

Item types may add their own fields below these. For example, digital items might add:

```yaml
provenance:
  source: "https://example.com/article"
  notes: "Saved for the regulatory framework section"
  source_url: "https://example.com/article"
  fetched_at: "2026-04-10T14:23:00Z"
  original_format: "html"
```

The minimum structure guarantees that cross-item-type queries like "where did this come from?" work without having to know the specific item type's extended schema.

### `removed_at` (optional, ISO 8601 date)

Only present when `status == removed`. The date the item was weeded.

### `removed_reason` (optional, string)

Only present when `status == removed`. Freeform explanation of why the item was removed. Recommended but not required — helps future browsing make sense of the historical record.

## .collection-index.yaml cache format

The collection-level index is a regenerable cache of universal fields from every item's `metadata.yaml`. Type-specific fields are not in the cache — views that need them read the item's own `metadata.yaml` directly.

```yaml
collection_name: "alexandria"
created: "2026-04-07"
sections:
  ai safety:
    items:
      - slug: "condition-x-treatments"
        title: "Condition X Treatments"
        book_type: "scout"
        major_section: "Research papers"
        description: "Living knowledge base tracking treatment options."
        date_added: "2026-04-10"
        form: "digital"
        media_type: "text:markdown"
        status: "active"
        author: null
        path: "ai safety/condition-x-treatments"
  causal inference:
    items:
      - slug: "causal-inference-methods"
        title: "Causal Inference Methods"
        book_type: "scout"
        major_section: "Research papers"
        description: "Methods for policy evaluation, with applicability notes."
        date_added: "2026-04-08"
        form: "digital"
        media_type: "text:markdown"
        status: "active"
        author: null
        path: "causal inference/causal-inference-methods"
```

### Regeneration

If `.collection-index.yaml` is missing or stale, the `/coll` skill rebuilds it by:

1. Walking the collection directory tree
2. For each `metadata.yaml` found, reading its universal fields
3. Grouping items by `section`
4. Writing the result to `.collection-index.yaml`

This means the user can delete `.collection-index.yaml` at any time without data loss. The source of truth is the per-item `metadata.yaml` files.

## How item types extend the shape

Each item type:

1. **Produces all required universal fields** in its acquired `metadata.yaml`
2. **Uses optional universal fields appropriately** (`author` where it makes sense; `provenance` always recommended)
3. **Adds type-specific fields** at the top level of the same file, after the universal fields
4. **Documents its type-specific schema** in its skill file (`.claude/skills/coll-{type}/SKILL.md`) or adjacent reference docs

The item type is free to define its own content shape beyond metadata — README structure, additional files, subdirectories, scripts. The only constraints are:

- The mandatory three files (`README.md`, `metadata.yaml`, `CLAUDE.md`) exist at acquisition time
- The `metadata.yaml` universal fields are all present and valid
- The directory is self-contained (content lives under the item's directory, not elsewhere)

## Slug generation reference

Given a title, generate a slug:

1. Lowercase the title
2. Replace each non-alphanumeric character with a hyphen
3. Collapse consecutive hyphens to a single hyphen
4. Remove leading and trailing hyphens
5. Truncate to 50 characters, removing a trailing hyphen if present
6. If the result is empty, fall back to a timestamp-based slug

Examples:
- "The Dispossessed" → `the-dispossessed`
- "LLMs: A Survey (2025)" → `llms-a-survey-2025`
- "Condition X: Treatment Options & Evidence" → `condition-x-treatment-options-evidence`

Uniqueness check: if the generated slug collides with an existing item in the collection, append `-2`, `-3`, etc. until a unique slug is found.

## Validation

There is no automated validation tool in v1. The `/coll` skill ensures valid metadata at acquisition time by construction. Users who hand-edit `metadata.yaml` are trusted to preserve the schema; the regeneration process tolerates missing optional fields but will fail loudly on missing required fields.

Validation tooling may be added later if drift becomes a problem in practice.
