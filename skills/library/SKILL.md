# /library

Create and manage a personal curated library — a collection of "books" organized by your needs.

A library is a directory on your machine containing books of different types. Each book is
a self-contained project (its own git repo) that conforms to the universal book shape
(see `docs/library/book-shape.md` in the alexandria repo). The library provides a
lightweight organizational layer: an index, sections, and a table of contents you can browse.

## Getting started

If no library exists yet, create one:

1. Ask the user what they'd like to call their library (default: "alexandria")
2. Ask where to create it (default: home directory, `~/alexandria`)
3. Create the directory and initialize `.library-index.yaml`:

```yaml
library_name: "alexandria"
created: "YYYY-MM-DD"
sections: {}
```

If a library already exists (detected by `.library-index.yaml` in the current directory or
a parent), work with that library.

## The universal book shape

Every book in the library, regardless of type, conforms to the universal book shape defined
in `docs/library/book-shape.md`. At minimum, every book directory contains:

- `README.md` — the book's spine, readable standalone
- `metadata.yaml` — the catalog entry with universal fields (slug, title, book_type,
  section, description, date_added, medium, status) plus any type-specific fields
- `CLAUDE.md` — operational context for Claude Code
- Optional `context.md` — interaction history (written by /take-notes on first use)

Book types provide their own content within this shape. When acquiring a book, ensure
the resulting directory satisfies the shape before considering the book added.

## Actions

### Add a book

Ask what the user needs. Based on their answer, determine the book type:

- **"I have a physical book (or shelf of books) I want to catalog"** → Physical
  A record of a physical book the user owns. Photo-based creation (single book or
  shelf) is the primary path; manual entry is supported. No content is copied — the
  book lives on a shelf, the catalog entry represents it. Available now — runs the
  /new-physical process.

- **"I want to add digital content I already have, or save a URL"** → Digital
  Local files (PDFs, HTML, markdown, text, images, audio, video), URLs to fetch and
  archive, or pasted text. Content is copied into the library and preserved in its
  original format. Available now — runs the /new-digital process.

- **"I need to understand and monitor a domain"** → Scout
  A curated, living knowledge base that monitors a topic for you. Researched, organized,
  critiqued, and kept current with automated discovery. Available now — runs the
  /new-scout process.

- **"I want to organize my own writing, notes, or projects"** → Author
  A container for content the user writes themselves. The skill creates the book's
  structure (universal files + a starter README suited to the purpose) and hands off
  to the user for writing. Supports projects, collections, journals, topical notes,
  and fully freeform writing. Available now — runs the /new-author process.

For a **physical book**:
Invoke /new-physical. That skill handles the full workflow: photo or manual input,
metadata extraction, confirmation, optional enrichment, classification, directory
creation, and library index update. See `skills/new-physical/SKILL.md`.

For a **digital book**:
Invoke /new-digital. That skill handles local files, URLs, and pasted text, with
metadata extraction, confirmation, optional enrichment, and the same classification
and index-update steps as /new-physical. See `skills/new-digital/SKILL.md`.

For an **author book**:
Invoke /new-author. That skill creates an empty book structure (universal files plus
a starter README based on the user's stated purpose — project, collection, journal,
notes, or freeform) and hands off to the user for writing. See
`skills/new-author/SKILL.md`.

For a **scout**:
1. Ask for a short name for the book (used to generate the slug — see slug generation in `docs/library/book-shape.md`)
2. Determine which section it belongs in. **Place into an existing section** — sections are soft-locked (see "Soft-locked section management" below). Propose the best-fit existing section; if no existing section is a clean match, use `unsorted` (create it if needed). If the library is brand-new and has no sections yet, ask the user what section to create for this first book.
3. Generate a slug from the title; check uniqueness against existing slugs and suffix with `-2`, `-3`, etc. if needed
4. Create the book directory at `{section}/{slug}/` within the library
5. `cd` into it and run the new-scout process (the full seven-phase process from the new-scout skill)
6. After building, ensure the book's `metadata.yaml` contains all required universal fields (the new-scout skill is responsible for creating this; verify it exists and is valid)
7. Update `.library-index.yaml` with the new book's universal fields (see cache format below)
8. **Check for review triggers** after adding. If the addition pushed a section past a diversity or size trigger, mention this to the user and offer to run `review-sections` now or defer.

### Browse

Two modes: quick (in terminal) and full (in browser).

**Quick browse** (default): Show the library's table of contents in the terminal:

```
Alexandria
├── Health
│   ├── Condition X Treatments (scout, created 2026-04-07)
│   └── Outbreak Monitoring (scout, created 2026-04-10)
└── Professional
    └── Causal Inference Methods (scout, created 2026-04-08)
```

**Full browse** (when the user wants to read): Regenerate the library's navigable views
and open in the browser. See "Viewing the library" below.

If the index is missing or stale, regenerate it by scanning the library tree for
`metadata.yaml` files and reading universal fields from each. See "Library index
cache format" below.

### Soft-locked section management

Sections are **soft-locked**: stable between organizational reviews, not frozen forever.
Between reviews, new books go into existing sections — Claude does not invent new
sections on the fly when adding a book. This keeps the library predictable: "I know
where my books live because the sections don't churn." When the structure genuinely
needs to change, Claude proposes a review and the user approves or defers.

Rationale: taxonomies that are made once and never updated become stale as the library
grows; taxonomies that churn constantly make nothing findable. The soft-lock middle
ground keeps things stable but responsive to growth.

#### Principles

- **New books go into existing sections.** If a user adds a book and no existing
  section is a clean fit, place it in the nearest section rather than creating a new
  one. If a book genuinely doesn't fit any existing section, note that during
  acquisition and flag it for the next section review — don't silently create a new
  section. The one exception: the first book in a brand-new library, when there are
  no sections yet.
- **Section reviews are occasional, not continuous.** Reviews happen when the current
  structure clearly isn't serving the library anymore. Between reviews, the user
  should be able to trust that the sections they see today are the sections they'll
  see tomorrow.
- **Reviews are proposals, not impositions.** Claude proposes; the user approves,
  edits, or defers. The user can also explicitly ask for a review at any time.
- **Reviews respect the user's taxonomy.** If the user's organizational logic is
  unusual (by mood, by project, by year, by provenance), Claude proposes within that
  logic rather than imposing a generic "by broad domain" scheme.

#### When to propose a review

Claude should notice these conditions during any /library action and mention them to
the user. Proposing a review is a prompt, not an obligation — the user may say "not
now" and Claude should drop it until the condition persists or worsens.

**Size triggers:**

- The library has 50+ books but only 2-3 sections (under-subdivided — hard to browse)
- A single section contains more than ~15 books (getting catch-all-y)
- A section contains fewer than 3 books and the library has 20+ books total (either
  needs more books or should be merged into a neighboring section)
- The library has more than ~12 sections at the top level (too many top-level
  sections — consider consolidating or introducing subsections)

**Diversity triggers** (judgment-based, not rule-based):

- A section's books cover visibly unrelated topics — "health" has books about
  treatments, kitchen equipment, and garden design. This is the "catch-all" failure
  mode: a section that was coherent at 5 books becomes a bucket for anything
  tangentially related at 15 books.
- A clear cluster within a section suggests a sub-topic worth its own section. E.g.,
  a "health" section that has 8 books about a specific condition alongside 4 general
  health books — the specific condition might deserve its own section.
- Books placed into "unsorted" (the fallback section for acquisitions that don't
  match any existing section) have accumulated. Unsorted is a signal that the
  current taxonomy has gaps.

**Time-based nudge** (light):

- No section review has happened in a long time and the library has grown meaningfully
  since the last one. Mention the option during a routine /library action; don't
  force it.

The thresholds above are calibration points, not rules. Claude uses judgment:
thresholds are triggers for *proposing* a review, not rules that force one.

#### The review workflow: `review-sections`

This action can be invoked explicitly (`/library` → review-sections) or offered
automatically when a trigger fires. The workflow:

1. **Read the current state.** Load `.library-index.yaml` and each book's
   `metadata.yaml`. Build an understanding of what's in each section: title,
   description, book type, and any other signals that help classify.
2. **Identify the specific problems.** What triggered the review? Catch-all sections,
   too many top-level sections, under-populated sections, "unsorted" accumulation?
   Name the problem(s) concretely.
3. **Propose a new structure.** Generate a proposed section taxonomy. This may
   involve:
   - **Renaming** a section ("health" → "health and wellness")
   - **Splitting** a section (one becomes two or more)
   - **Merging** sections (two become one)
   - **Creating** a new section (for a cluster that didn't fit before)
   - **Removing** an empty section (no books after other moves)
   - **Moving** books between sections to match the new structure

   Each change has a rationale tied to the triggering problem. "The 'health' section
   had 15 books spanning treatment research, nutrition, and fitness; split into
   'treatment research', 'nutrition', and 'fitness' so each stays focused."
4. **Present the proposal to the user.** Show:
   - The current sections with book counts
   - The proposed sections with the same book counts distributed per the new plan
   - A per-book diff: which books move from where to where, and which sections change
     name or disappear
   - The rationale for each non-trivial change
5. **Let the user decide.** Offer four options:
   - **Approve each change individually** — walk through the proposal one decision
     at a time
   - **Accept all** ("yolo") — apply the whole proposal without per-change confirmation
   - **Edit the proposal** — user changes specific moves before accepting
   - **Defer** — no changes now; the review is dropped until next time it's relevant
6. **Execute the approved changes.** Atomically (to the extent possible):
   - Create any new section directories
   - Move book directories to their new sections (filesystem mv)
   - Update each moved book's `metadata.yaml`: `section` field
   - Update `.library-index.yaml`: reflect all moves and section structure changes
   - Remove any emptied section directories
7. **Log the review.** Invoke `/take-notes` to write to `library-context.md`: what
   was reviewed, what triggered it, what changed, what the user's rationale was.
   Future reviews can look back at this to understand how the taxonomy has evolved.
8. **Regenerate the wiki** so the new section structure is reflected in all views.

#### What review-sections does NOT do

- **Does not restructure books' internal contents** — only their section placement.
  The book directories themselves (their metadata, README, content) are unchanged by
  a section review.
- **Does not change book slugs or titles** — only directory location.
- **Does not delete books** — removal is a separate action (`remove-book` or
  `delete-book`).
- **Does not run automatically without user approval** — reviews are always proposed,
  never executed unilaterally. Even "yolo" mode requires the user to explicitly
  request it.
- **Does not impose a universal taxonomy** — each library has its own organizational
  logic. Claude proposes within the user's existing scheme, extending or refining it
  rather than replacing it wholesale.

#### Unsorted: the fallback section

When a book is added and no existing section is a clean fit, place it in a section
called `unsorted` (creating it if needed). This is the one place where new sections
appear outside of a review. Unsorted is a signal: if books are accumulating there,
the current taxonomy has a gap, and the next review should address it.

An "unsorted" section with 5+ books is itself a trigger to propose a review.

### Remove a book (weeding)

Two removal modes. Default keeps a historical record; full deletion is opt-in.

Rationale: a real library's card catalog keeps records of withdrawn items. Knowing
"this was here once" is valuable — it prevents accidentally re-adding the same
content and preserves the record of past interests. Full deletion is available for
privacy concerns or when the user genuinely wants no record.

#### `remove-book` (default)

Marks a book as removed but keeps the catalog entry and the book's directory intact.

Steps:

1. Identify the book to remove (ask the user by title or slug; confirm the match
   before proceeding).
2. Ask the user for a removal reason (optional but encouraged — record empty string
   if the user declines).
3. Confirm the action clearly before making any changes.
4. Update the book's `metadata.yaml`:

   ```yaml
   status: removed
   removed_at: "YYYY-MM-DD"     # today's date
   removed_reason: "..."        # user's reason, or omit if empty
   ```

5. Update `.library-index.yaml` to reflect the same `status: removed`, `removed_at`,
   and `removed_reason` fields on the book's entry.
6. Leave the book's directory in place. The content files are preserved; only the
   catalog status changes. If the user explicitly wants the directory removed, use
   `delete-book` instead.
7. Invoke `/take-notes` to log the removal in `library-context.md` with details:
   which book, when, and the reason (if given).
8. Regenerate the wiki so removed books show with the "removed" marker on index
   pages and the removal notice on their individual pages.

Confirm before committing the changes. This is not a destructive action (the
directory stays), but the catalog state change should be deliberate.

#### `delete-book` (opt-in, destructive)

Fully removes the book's entry from `.library-index.yaml` and deletes the book's
directory from disk. No trace remains in the library except for the log entry in
`library-context.md`.

Steps:

1. Identify the book to delete. Confirm the match.
2. Warn the user clearly that this is destructive: the book's directory and all its
   files will be removed, and the catalog entry will be removed. The only record
   that will remain is the log entry in `library-context.md`.
3. Ask for a deletion reason (encouraged).
4. Require explicit confirmation ("yes, delete" — not a generic "ok").
5. Remove the book's entry from `.library-index.yaml`.
6. Delete the book's directory with `rm -rf` (or equivalent).
7. Invoke `/take-notes` to log the deletion in `library-context.md` with full details:
   book title, slug, path (for the record), date, and reason. This log entry is the
   only trace.
8. Regenerate the wiki so the book no longer appears anywhere in the views.

Use `delete-book` when the user has a real reason to eliminate the record (privacy,
cleanup of mistaken additions, or explicit intent to forget). Default to `remove-book`
otherwise.

### Settle a scout

Scouts are living books by default — discovery runs periodically, new entries get
added, the scout evolves. At some point the user may decide the scout has served its
purpose and should become a static reference. "Settling" a scout freezes it as a
static book in the library.

Steps:

1. Identify the scout to settle. Confirm the user means this scout and confirm that
   its `book_type` is indeed `scout`.
2. Ask the user for an optional note about why they're settling the scout (for the
   record).
3. Update the scout's `metadata.yaml`:

   ```yaml
   settled: true
   settled_at: "YYYY-MM-DD"     # today's date
   ```

4. Stop any discovery automation associated with the scout. If the scout has a
   scheduled discovery workflow (e.g., a GitHub Actions cron job running
   `scripts/discover.py`), disable or remove it. Claude Code should describe to the
   user what was running and what it's disabling so they have a clear picture.
5. The scout's content (data/entries.yaml, scripts/, docs/, README.md) is preserved
   as-is. Settling is a state change, not a content change.
6. Invoke `/take-notes` to log the settling in the scout's own `context.md` and in
   `library-context.md`. Record the settling rationale.
7. Regenerate the wiki. Settled scouts render differently from live scouts: the
   wiki page for a settled scout shows its README content inline (like other static
   book types — physical, digital, author) rather than linking out. This visibly
   marks the state change and makes the settled scout browseable like other static
   content. Live scouts continue to link out to their own presentation.

Settling is a one-way action in v1. If the user wants to "unsettle" a scout (resume
discovery, rebuild), they can edit `metadata.yaml` to set `settled: false` and
re-enable any discovery workflow. We don't expose this as an explicit action because
it's uncommon.

## Library index cache format

The `.library-index.yaml` at the library root is a regenerable cache of universal fields
from every book's `metadata.yaml`. Type-specific fields are not in the cache — views that
need them read the book's own `metadata.yaml` directly.

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
        form: "digital"
        media_type: "text:markdown"
        status: "active"
        author: null
        path: "health/condition-x-treatments"
```

### Updating the index

The index is updated whenever books are added, removed, weeded, or reorganized. On each
of these actions:
1. Update the corresponding book's `metadata.yaml` (source of truth)
2. Update `.library-index.yaml` to reflect the change

### Regenerating the index

If `.library-index.yaml` is missing, corrupted, or suspected stale, rebuild it:

1. Walk the library directory tree
2. For each `metadata.yaml` found, read the universal fields
3. Group books by their `section` field
4. Write the result to `.library-index.yaml`

The per-book `metadata.yaml` files are the source of truth. The index can always be
reconstructed from them. This means the user can delete `.library-index.yaml` without
losing any information.

## Wiki view

The library has a generated wiki — a browseable static HTML interface at
`{library}/wiki/index.html`. The wiki is the primary interface for non-CLI users and
works entirely offline (open `index.html` in any browser).

The wiki is generated by the alexandria tool `tools/generate_wiki.py`. Invoke it via:

```
uv run python /path/to/alexandria/tools/generate_wiki.py /path/to/library
```

Adjust the path to the alexandria repo as needed (if the user cloned to `~/alexandria`,
that's `~/alexandria/tools/generate_wiki.py`).

### regenerate-wiki action

Explicit action: `/library` → regenerate-wiki. Runs the generator against the current
library.

### Automatic regeneration after library changes

Invoke wiki regeneration automatically after any action that modifies library contents:
- Adding a book (any book type — /new-physical, /new-digital, /new-scout)
- Removing or deleting a book (weeding)
- Reorganizing (section changes)

The wiki regeneration is fast (seconds for small libraries) and ensures the browseable
view stays in sync with the catalog. For ad-hoc interactions that don't use these
actions (e.g., the user hand-edits a book's metadata.yaml), the user can explicitly
run regenerate-wiki when they want the wiki updated.

### Wiki output structure

```
{library}/wiki/
├── index.html              # homepage with summary and recent additions
├── _assets/style.css       # shared stylesheet
├── by-section/             # browse by section
├── by-date/                # browse chronologically (newest first)
├── by-type/                # browse by book_type (physical, digital, scout, ...)
├── by-form/                # browse by form (physical vs digital)
├── by-media-type/          # browse by media_type, grouped by content_type
├── by-topic/               # Pass 2 placeholder (not yet enabled)
└── books/                  # individual book pages
    └── {slug}.html
```

Individual book pages: scouts show a thin catalog entry with a link to the scout's own
README; physical, digital, and author books show the book's README content inline (up
to ~2000 words, with a "continued" link to the original for longer content). Removed
books show the "resource removed" marker and preserved metadata.

## Organizational principles

- **Directory structure IS the organization.** Sections are directories. The index is
  metadata, not the source of truth for structure.
- **The index is regenerable.** If `.library-index.yaml` is deleted, the skill can
  reconstruct it by scanning for git repos in the directory tree.
- **Light touch.** The library is an organizational layer, not a database. A user should
  be able to understand the structure by running `ls`.
- **User decides.** Propose groupings, don't impose them. Offer a reasonable default
  (by broad domain) but accept any structure the user prefers.

## Library-level context

Maintain an optional `library-context.md` at the library root with user-level patterns
that apply across books:
- Organizational preferences (how the user likes sections grouped)
- Technical comfort level (so vocabulary can be calibrated)
- Cross-book patterns observed

Generated lazily — created on the first significant `/library` interaction (not at library
creation), via the /take-notes skill. Read at the start of each `/library` invocation to
inform the agent's vocabulary and approach.

## Cross-book queries

When the user asks questions that span books ("what do my health books say about X?",
"which scouts mention treatment Y?"), read the relevant books' files directly. The
`.library-index.yaml` provides each book's path. Read each book's `context.md` for
decisions and history; read its `data/entries.yaml` or generated `README.md` for content.

No subagents or special access needed — Claude Code can read any file on the user's
machine. The `.library-index.yaml` is the routing table.

## Take-notes invocations

After meaningful `/library` actions, invoke /take-notes to log what was done:
- After adding a book (book-type skills handle their own logging; the library logs the
  organizational decision: which section, why)
- After reorganizing (which axes were chosen, what moved)
- After cross-book queries that revealed useful patterns (record the observed pattern as
  a user preference if the user confirms it)

The /take-notes skill detects the library context automatically and writes to
`library-context.md` at the library root.

## Viewing the library

The library is viewable at three layers. Markdown files are the truth; everything else
is a view on top.

### Layer 1: Claude Code (queries and navigation)

Most library interactions are queries that don't need rendering:
- "What's in my library?" → read index, show TOC
- "What's in my health section?" → list books in a section
- "Open my condition treatments scout" → run `open` on the right file
- "What's new since last week?" → scan git logs across book repos
- "What does my scout say about treatment X?" → read the YAML, answer directly

### Layer 2: Interlinked README.md files (the foundation)

The library is navigable via README.md files at every level:

```
~/alexandria/
├── README.md              ← library TOC: links to section READMEs
├── health/
│   ├── README.md          ← section TOC: links to book READMEs
│   └── condition-treatments/
│       └── README.md      ← book overview (generated by /new-scout)
```

These work in any markdown viewer (VS Code, Marked, Typora), on GitHub, and with any
tool that renders markdown. Relative links between README.md files enable click-through
navigation.

Auto-generate the library-level and section-level README.md files from `.library-index.yaml`
whenever the index changes (add book, reorganize). Book-level READMEs are generated by
the book-type skill (/new-scout).

### Layer 3: Pre-rendered HTML (browser viewing without a markdown app)

For users who want to read in a plain browser without installing a markdown viewer:

Generate an `index.html` alongside each README.md. The HTML is self-contained:
- Inline CSS (~40 lines: readable serif font, max-width, heading hierarchy, table styling)
- No JavaScript, no CDN, no external files
- Relative links between HTML files — works over `file://`
- No server needed

```
~/alexandria/
├── README.md
├── index.html             ← same content, rendered HTML with inline CSS
├── health/
│   ├── README.md
│   ├── index.html
│   └── condition-treatments/
│       ├── README.md
│       └── index.html
```

The user bookmarks `~/alexandria/index.html` and clicks through the library.

**When to generate HTML:**
- On "browse" (full mode): regenerate all library and section HTML, then `open index.html`
- On "add book": regenerate affected section and library HTML
- On "reorganize": regenerate all HTML
- Book-level HTML is generated during the book build process (Phase 4)

**HTML template for library/section index pages** (generated from `.library-index.yaml`,
no markdown parsing needed):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{library_name}</title>
<style>
  body { font-family: Georgia, 'Times New Roman', serif; max-width: 42em;
         margin: 2em auto; padding: 0 1em; line-height: 1.6; color: #222; }
  h1 { border-bottom: 1px solid #ddd; padding-bottom: 0.3em; }
  h2 { margin-top: 1.5em; color: #444; }
  a { color: #1a5276; }
  .book { margin: 0.5em 0; }
  .book .name { font-weight: bold; }
  .book .meta { color: #666; font-size: 0.9em; }
  .book .desc { margin-top: 0.2em; }
  nav { font-size: 0.9em; color: #666; margin-bottom: 2em; }
  nav a { color: #666; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th, td { text-align: left; padding: 0.4em 0.8em; border-bottom: 1px solid #ddd; }
  th { font-weight: bold; border-bottom: 2px solid #999; }
</style>
</head>
<body>
<nav>{breadcrumb}</nav>
<h1>{title}</h1>
{content}
</body>
</html>
```

Use this same template for all pages. Book-level HTML wraps the generated README content
in this same shell.

## Adapting to the user

Same principle as new-scout: gauge technical comfort, use plain language by default.
"Sections" not "taxonomy." "Organize" not "restructure." "Your library" not "the index."

For new users, explain what a library is in concrete terms: "This creates a folder on your
computer called 'alexandria' (or whatever you'd like to name it). Inside it, each topic you
track gets its own folder. I'll help you organize them and keep an index so you can find
things."
