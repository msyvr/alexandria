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

- **"I need to understand and monitor a domain"** → Tracker
  A structured, living knowledge base on a topic. Researched, organized, critiqued, and
  kept current with automated discovery. Available now — runs the build-tracker process.

- **"I have papers, articles, or books to organize"** → Import (coming soon)
  Curated collection of external content. Organized, annotated, cross-referenced.
  Not yet available — let the user know this is planned.

- **"I want to organize my own writing, notes, or projects"** → Author (coming soon)
  The user's own creative and professional output. Structured, searchable, maintained.
  Not yet available — let the user know this is planned.

For a **tracker** book:
1. Ask for a short name for the book (this becomes the directory name)
2. Determine which section it belongs in (propose based on existing sections, or create new)
3. Create the book directory within the appropriate section
4. `cd` into it and run the build-tracker process (the full seven-phase process from
   the build-tracker skill)
5. After building, update `.library-index.yaml` with the new book

### Browse

Show the library's table of contents, organized by section:

```
Alexandria
├── Health
│   ├── Condition X Treatments (tracker, created 2026-04-07)
│   └── Outbreak Monitoring (tracker, created 2026-04-10)
└── Professional
    └── Causal Inference Methods (tracker, created 2026-04-08)
```

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

## Organizational principles

- **Directory structure IS the organization.** Sections are directories. The index is
  metadata, not the source of truth for structure.
- **The index is regenerable.** If `.library-index.yaml` is deleted, the skill can
  reconstruct it by scanning for git repos in the directory tree.
- **Light touch.** The library is an organizational layer, not a database. A user should
  be able to understand the structure by running `ls`.
- **User decides.** Propose groupings, don't impose them. Offer a reasonable default
  (by broad domain) but accept any structure the user prefers.

## Adapting to the user

Same principle as build-tracker: gauge technical comfort, use plain language by default.
"Sections" not "taxonomy." "Organize" not "restructure." "Your library" not "the index."

For new users, explain what a library is in concrete terms: "This creates a folder on your
computer called 'alexandria' (or whatever you'd like to name it). Inside it, each topic you
track gets its own folder. I'll help you organize them and keep an index so you can find
things."
