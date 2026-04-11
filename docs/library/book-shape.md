# Universal book shape

Every book in an alexandria library follows the same outer shape, regardless of book type. This contract makes books interchangeable at the library level: the catalog can iterate over them, views can render them, skills can operate on them, and new book types can plug into the existing infrastructure without redesigning the foundation.

This document specifies the shape. Book types define their own content within it.

## Design principles

- **Minimum mandatory, nothing speculative.** Every required field has a defined consumer today.
- **metadata.yaml is the source of truth.** The library-level `.library-index.yaml` is a regenerable cache derived from every book's `metadata.yaml`.
- **Filesystem structure is not duplicated in metadata.** If the information is in the directory path, it doesn't also live in a field. (One exception: `section` is kept in metadata so the index cache doesn't require filesystem walks.)
- **Hand-editable.** A user should be able to open `metadata.yaml` in a text editor, change a field, and have the library pick up the change.

## Book directory shape

Every book directory contains these files at acquisition time:

```
{book-slug}/
├── README.md           # the spine: what this book is, readable standalone
├── metadata.yaml       # the catalog entry (universal + type-specific fields)
├── CLAUDE.md           # operational context for Claude Code (book-type-specific)
└── ... type-specific content files ...
```

One more file is created on first use but isn't required at acquisition:

```
{book-slug}/
└── context.md          # interaction history, written by /take-notes
```

**README.md**: the book's spine. A reader should be able to open it and understand what this book is, what's in it, and how to navigate its contents, without any other context. Each book type provides its own README template; scouts generate a rich overview, physical books show metadata and (if present) a photo, imports show provenance and content, author books show the user's writing.

**metadata.yaml**: the catalog entry (see schema below).

**CLAUDE.md**: operational context for Claude Code when the user returns to the book in a future session. Book-type-specific content: scouts describe their schema and update commands, physical books describe their source and any online enrichment policy, etc. Kept lean (~40-60 lines). See `skills/new-scout/SKILL.md` for the scout template.

**context.md**: interaction history written by `/take-notes`. Created on first invocation. Contains decisions, user preferences, session log, open questions, and useful Q&A. Universal format across all book types.

**Type-specific content files**: whatever the book type needs. Scouts have `data/entries.yaml`, `scripts/`, `docs/`, and a generated `README.md`. Physical books might have a `photo.jpg`. Imports might have an `original.pdf` plus a markdown extraction. Author books might have multiple markdown files for different sections of the user's writing.

## metadata.yaml universal schema

### Required fields

```yaml
slug: "condition-x-treatments"        # unique within library; matches directory name
title: "Condition X Treatments"       # display name, any characters
book_type: "scout"                    # physical, import, author, or scout
section: "health"                     # top-level library section
description: "Living knowledge base tracking treatment options."  # one line
date_added: "2026-04-10"              # ISO 8601 date
medium: "digital"                     # digital or physical
status: "active"                      # active or removed
```

### Optional fields

```yaml
author: "Ursula Le Guin"              # semantics vary by book type (see below)
provenance:
  source: "Personal collection"       # freeform string — where this came from
  notes: "Inherited from family"      # freeform string — any acquisition context
removed_at: "2026-05-01"              # ISO date; only if status == removed
removed_reason: "Superseded"          # freeform; only if status == removed
```

### Type-specific fields

Book types define their own fields at the top level of the same file, after the universal fields. No nesting ceremony. Example for scout:

```yaml
# ... universal fields above ...
settled: false                        # true if the scout has been frozen as static
```

## Field semantics

### `slug` (required, string)

URL-and-filename-safe identifier for the book. Generated from the title:
- Lowercase
- Non-alphanumeric characters replaced with hyphens
- Multiple consecutive hyphens collapsed
- Leading/trailing hyphens removed
- Truncated to ~50 characters if needed

Must be **unique within the library**. The `/library` acquisition process checks existing slugs and appends a numeric suffix if needed (`-2`, `-3`, etc.). The book's directory name matches its slug.

### `title` (required, string)

Display name. Any characters allowed. Shown in catalog views and used as the `<title>` in generated HTML.

### `book_type` (required, enum)

One of:
- `physical` — a record of a physical book the user owns (no content files)
- `import` — content imported from elsewhere with provenance
- `author` — content the user wrote themselves
- `scout` — a living, AI-maintained knowledge base

This determines which creation skill was used and what type-specific fields to expect.

### `section` (required, string)

The top-level library section where this book lives. Matches a directory at the library root (e.g., `health`, `professional`, `reference`). Required.

If the acquisition process can't determine a section, it defaults to `"unsorted"` and the user can move it later.

Note: `section` duplicates information from the directory path. It's kept in metadata so the `.library-index.yaml` cache doesn't require walking the filesystem on every read. This is a deliberate exception to the "don't duplicate filesystem structure" principle.

### `description` (required, string)

One-line summary. Target ~150 characters, maximum ~300. Shown in catalog and index views without opening the book. Should convey what the book is and why the user has it.

### `date_added` (required, ISO 8601 date)

The date the book was added to the library. Format: `YYYY-MM-DD`. Set automatically on acquisition; never changed by normal operations.

### `medium` (required, enum)

One of:
- `digital` — content exists as files in the book directory
- `physical` — content exists in the physical world; the catalog entry is a record

Binary. There is no `both` value for v1. If a user has the same work in both forms, they create two entries with no cross-reference. Linking is a deferred feature.

### `status` (required, enum)

One of:
- `active` — the book is part of the live library (default)
- `removed` — the resource has been weeded; the catalog entry persists as a historical record

There is no `archived` status. Archiving is accomplished by moving a book to an `_archive/` section, not by changing status. Removal (via weeding) sets `status: removed` — see `/library` weeding actions.

### `author` (optional, string)

Semantics vary by book type:
- **physical**: the literal author of the physical book (e.g., "Ursula K. Le Guin")
- **import**: the author(s) of the imported source; for papers with many authors, use "First Author et al."
- **author**: typically omitted; this is content the user wrote
- **scout**: typically omitted; scouts are aggregated rather than authored

When null or omitted, catalog views display "—" or skip the author display.

### `provenance` (optional, object)

Acquisition context. Minimum structure is two freeform string fields:

```yaml
provenance:
  source: "..."       # where this came from
  notes: "..."        # any additional acquisition context
```

Book types may add their own fields below these. For example, imports might add:

```yaml
provenance:
  source: "https://example.com/article"
  notes: "Saved for the regulatory framework section"
  source_url: "https://example.com/article"
  fetched_at: "2026-04-10T14:23:00Z"
  original_format: "html"
```

The minimum structure guarantees that cross-book-type queries like "where did this come from?" work without having to know the specific book type's extended schema.

### `removed_at` (optional, ISO 8601 date)

Only present when `status == removed`. The date the book was weeded.

### `removed_reason` (optional, string)

Only present when `status == removed`. Freeform explanation of why the book was removed. Recommended but not required — helps future browsing make sense of the historical record.

## .library-index.yaml cache format

The library-level index is a regenerable cache of universal fields from every book's `metadata.yaml`. Type-specific fields are not in the cache — views that need them read the book's own `metadata.yaml` directly.

```yaml
library_name: "alexandria"
created: "2026-04-07"
sections:
  health:
    books:
      - slug: "condition-x-treatments"
        title: "Condition X Treatments"
        book_type: "scout"
        description: "Living knowledge base tracking treatment options."
        date_added: "2026-04-10"
        medium: "digital"
        status: "active"
        author: null
        path: "health/condition-x-treatments"
  professional:
    books:
      - slug: "causal-inference-methods"
        title: "Causal Inference Methods"
        book_type: "scout"
        description: "Methods for policy evaluation, with applicability notes."
        date_added: "2026-04-08"
        medium: "digital"
        status: "active"
        author: null
        path: "professional/causal-inference-methods"
```

### Regeneration

If `.library-index.yaml` is missing or stale, the `/library` skill rebuilds it by:

1. Walking the library directory tree
2. For each `metadata.yaml` found, reading its universal fields
3. Grouping books by `section`
4. Writing the result to `.library-index.yaml`

This means the user can delete `.library-index.yaml` at any time without data loss. The source of truth is the per-book `metadata.yaml` files.

## How book types extend the shape

Each book type:

1. **Produces all required universal fields** in its acquired `metadata.yaml`
2. **Uses optional universal fields appropriately** (`author` where it makes sense; `provenance` always recommended)
3. **Adds type-specific fields** at the top level of the same file, after the universal fields
4. **Documents its type-specific schema** in its skill file (`skills/{book-type}/SKILL.md`) or adjacent reference docs

The book type is free to define its own content shape beyond metadata — README structure, additional files, subdirectories, scripts. The only constraints are:

- The mandatory three files (`README.md`, `metadata.yaml`, `CLAUDE.md`) exist at acquisition time
- The `metadata.yaml` universal fields are all present and valid
- The directory is self-contained (content lives under the book's directory, not elsewhere)

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

Uniqueness check: if the generated slug collides with an existing book in the library, append `-2`, `-3`, etc. until a unique slug is found.

## Validation

There is no automated validation tool in v1. The `/library` skill ensures valid metadata at acquisition time by construction. Users who hand-edit `metadata.yaml` are trusted to preserve the schema; the regeneration process tolerates missing optional fields but will fail loudly on missing required fields.

Validation tooling may be added later if drift becomes a problem in practice.
