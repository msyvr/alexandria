# /library

Create and manage a personal curated library — a collection of "books" organized by your needs.

A library is a directory on your machine containing books of different types. Each book is
a self-contained project (its own git repo). The library provides a lightweight organizational
layer: an index, sections, and a table of contents you can browse.

## Getting started

If no library exists yet, create one:

1. Ask the user what they'd like to call their library (default: "alexandria")
2. Ask where to create it (default: home directory, `~/alexandria`)
3. Create the directory and initialize `.library-index.yaml`:

```yaml
name: "alexandria"
created: YYYY-MM-DD
sections: {}
```

If a library already exists (detected by `.library-index.yaml` in the current directory or
a parent), work with that library.

## Actions

### Add a book

Ask what the user needs. Based on their answer, determine the book type:

- **"I need to understand and monitor a domain"** → Scout
  A curated, living knowledge base that monitors a topic for you. Researched, organized,
  critiqued, and kept current with automated discovery. Available now — runs the
  /new-scout process.

- **"I have papers, articles, or books to organize"** → Import (coming soon)
  Curated collection of external content. Organized, annotated, cross-referenced.
  Not yet available — let the user know this is planned.

- **"I want to organize my own writing, notes, or projects"** → Author (coming soon)
  The user's own creative and professional output. Structured, searchable, maintained.
  Not yet available — let the user know this is planned.

For a **scout**:
1. Ask for a short name for the book (this becomes the directory name)
2. Determine which section it belongs in (propose based on existing sections, or create new)
3. Create the book directory within the appropriate section
4. `cd` into it and run the new-scout process (the full seven-phase process from
   the new-scout skill)
5. After building, update `.library-index.yaml` with the new book

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

If the index is missing or stale, regenerate it by scanning the directory structure
(each subdirectory with a `.git/` is a book).

### Reorganize

When sections grow or the user's needs shift, propose reorganization:

- **Subdivision**: When a section holds more than ~7 books, propose splitting it into
  subsections. Ask the user what axes make sense.
- **Regrouping**: If books have been added ad hoc and the organization no longer reflects
  how the user thinks about them, propose a new grouping. Show the proposed structure,
  let the user adjust.
- **Axes**: Propose organizational groupings based on the books that exist. Default is
  by broad domain (health, professional, personal, etc.). The user can override with
  any grouping that makes sense to them.

Reorganization means moving directories and updating the index. Always confirm before
moving anything.

### Remove a book (weeding)

Two removal modes. Default keeps a historical record; full deletion is opt-in.

**Default: `remove-book`** — the book's catalog entry stays in `.library-index.yaml`
but is marked as removed:

```yaml
- name: "Example Book"
  status: removed
  removed_at: "2026-04-10"
  removed_reason: "No longer relevant to current interests"
  # ... rest of entry preserved
```

The book's directory may be archived (moved to an `_archived/` subsection) or deleted.
The catalog entry persists as a historical record: "I once had this book in my library."
This prevents accidentally re-adding the same content later and preserves the record of
past interests. Log the removal in `library-context.md`.

**Opt-in: `delete-book`** — fully remove the entry from `.library-index.yaml` AND delete
the book's directory. No trace remains in the library. Log the full deletion event with
reason in `library-context.md`. Use this for privacy concerns or when the user genuinely
wants no record.

Always confirm before removing or deleting. Ask the user for a reason (optional but
encouraged — it helps future browsing make sense of the historical record).

Rationale: a real library's card catalog keeps records of withdrawn items. Knowing
"this was here once" is valuable. Full deletion is available when the user chooses it,
not as the default.

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
