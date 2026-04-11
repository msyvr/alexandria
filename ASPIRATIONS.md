# Project Aspirations

## The core idea

Alexandria is lightweight library infrastructure — a structure for organizing the digital content you want to own, keep, and reference. It borrows from the real-world library: a curated collection where things live in predictable places, findable by catalog or by browsing the stacks, with or without a librarian's help.

The library is a directory on your machine. Inside it, "books" are the things you hold — self-contained units with a consistent outer shape. Some books are content you've collected from elsewhere. Some are your own writing. A few may be dynamic — living resources that update themselves. The library's job is to hold them, organize them, and make them browseable. Your job is to decide what goes in.

Alexandria is AI-assisted, but not AI-dependent. A librarian (Claude Code today, a local open-source model eventually) helps with cataloging, search, and cross-book questions — but every feature of the library works without one. You can browse the catalog, walk the sections, and read any book without invoking any AI at all.

## Why not just a plain folder?

A folder with subfolders is fine at ten items. By the time you have a hundred, you can't find anything you didn't name carefully, you can't remember why half of it is there, and nothing ties related items together.

Alexandria adds the minimum structure that makes a collection browseable at scale:

| Concern | Plain folder | Alexandria |
|---|---|---|
| Finding an item without opening it | Filename only | Catalog with metadata |
| Consistent item shape | Whatever was dropped | Every book has known structure |
| Classification conventions | Arbitrary subdirectories | Sections with documented patterns |
| Browseable view | `ls` or Finder | Generated catalog, multiple axes |
| Context about why items are there | None | Per-book metadata and history |
| Works without AI assistance | No, at scale | Yes — that's the point |

The structure is deliberately lightweight. It's not a database. It's not an app. It's files on disk, organized in a way that scales past a few hundred items without requiring an AI to navigate.

## Who this is for

Anyone who would benefit from an organized, personal collection of digital content they want to own rather than depend on someone else's platform. No technical background is required. Some users will be software engineers who don't want to build the scaffolding from scratch. Some will have never opened a terminal. Both want the same thing: a library they own, understand, and can use.

The tool meets people where they are technically. For users new to working in a terminal, the process builds practical skills as a side effect. For technical users, it skips the hand-holding and gets to the result.

## Technical minimalism as a skill

For users who want it, alexandria doubles as a low-friction path to a disproportionately useful skill set: **technical minimalism**. Know what's absolutely necessary for security and essential capabilities, and know what isn't. Direct AI assistants effectively. Read structured data. Understand what "you own this data" means in practice.

This is a much smaller surface area than "learn to code" and a much more valuable one for a busy professional. Someone who can open a terminal, direct an AI assistant, and verify that the result does what it should can accomplish things that previously required hiring a developer — not because they learned to program, but because they learned what to ask for and what to check.

Alexandria is designed so this learning happens as a side effect of building something you actually need. If that's not your goal, fine — the library still works the same way. The upskilling is opt-in.

## Library invariants

These derive from the real-world library metaphor and are the acceptance criteria for alexandria's design. Every invariant must hold for the library to earn its place over a plain folder.

1. **Every book has a catalog entry.** Title, author/source, classification, description, date added, book type, medium (digital, physical, or both). You can find a book without opening it.
2. **Every book has a consistent outer shape.** Regardless of book type: a README (the spine), metadata (the catalog entry), and content files.
3. **The catalog is browseable by multiple axes.** Not just by directory structure — by section, by date added, by book type, by source. Views are generated from the catalog.
4. **Classification is convention-based and learnable.** Sections are directories. The user chooses their taxonomy; alexandria suggests starting patterns and documents them.
5. **Acquisition is a first-class process.** Adding a book requires determining type, populating the catalog, recording provenance.
6. **Weeding is a first-class process.** Books can be removed through a defined process. Default behavior keeps the catalog entry and marks the resource as removed (preserving the record that the book was once in the library); full deletion is available as an opt-in. Both log to `library-context.md`.
7. **Dynamic content is an exception, and can be settled.** Scouts are allowed but marked as dynamic. Users can freeze a scout into a static book at any time.
8. **The librarian is optional — and eventually local.** Every library feature is usable without AI. Claude accelerates it; a local open-source model will eventually be the default librarian.

9. **Books record their medium and link duplicates.** Every catalog entry includes a `medium` field: digital, physical, or both. When a user has both a digital and physical copy of the same book, the catalog links them as a single entry with both media flagged. The library detects likely duplicates during acquisition and asks the user to confirm the link.

## Book types

A book type defines how content of a particular kind gets created, organized, and maintained. All book types share the universal outer shape (README, metadata, classification, catalog entry) and the library's infrastructure. Beyond that, each type has its own creation process and conventions.

### Physical (planned, top priority)
A record of a physical book (or other physical item) you own. Unlike import, no content is copied — the book itself lives on your shelf. The catalog entry is the library's representation of the book. Creation is primarily photo-based: photograph a single book or a whole shelf, and the librarian extracts title, author, and other metadata from the image. Manual entry is supported as well, with or without a photo. An optional visual record (the photograph itself) is preserved.

For users who permit it, the librarian can also fetch publicly available metadata and summaries (from open book databases) to enrich the record — the book's content never leaves your shelf, but its title and author are public information. This is opt-in for privacy-first users who prefer fully offline operation.

**Physical is the top-priority book type.** The cataloging space has solid tools for standard use cases — LibraryThing, Libib, and CLZ Books handle barcode scanning, metadata retrieval, and cloud sync well. Where alexandria differentiates:

- **Shelf photo workflow with strong accuracy**: Photograph a whole shelf and get a draft catalog of every book visible. The one existing tool attempting this (Shelf Scan, launched 2024) has reportedly poor accuracy because it uses weaker vision models. Alexandria can meaningfully beat this by defaulting to best-available vision models.
- **Local-first, files you own**: Most existing tools are cloud-first. Alexandria's files live on your machine, browseable without the app, portable forever.
- **No subscription lock-in**: Free and unlimited.
- **Integration with other book types**: Alexandria holds physical books alongside digital imports, user-authored content, and scouts in a single library. No existing cataloging tool spans all these.

Leading with physical also signals what alexandria values: the considered, ownership-oriented approach to personal knowledge, where a book on your shelf is as first-class as a PDF on your drive.

Best-quality AI is the default for photo extraction (vision models benefit from stronger models), with a local-model option for privacy-first users.

### Import (planned, high priority)
Digital content you've gathered from elsewhere — papers, articles, web pages, downloaded files, screenshots, anything with provenance. The library copies the raw content and extracts metadata so you can find it later.

### Author (planned)
Content you produce yourself — notes, research, drafts, project plans, task lists, journal entries. Structured enough to be searchable, flexible enough for freeform writing.

### Scout (available, but not the focus)
A living knowledge base that monitors a domain. Unlike import and author, a scout is actively maintained by AI — researched, organized, critiqued, and kept current through automated discovery. Scouts are powerful but are the exception rather than the rule: most library holdings should be static, like most of a real library's holdings.

A scout can be **short-lived** (built for an immediate need, updated briefly, then settled into a static reference) or **long-lived** (kept updating indefinitely for an evolving domain). The user decides when to settle a scout — to freeze it as a static book in the library.

Because scout creation depends on capabilities that currently only the best models have (research, critique, editorial writing), scouts remain Claude-assisted even as the library librarian shifts to local models. This asymmetry is intentional: the library foundation should be maximally portable; the ambitious book-building work can reasonably require better models.

### Future types
The architecture accommodates book types not yet designed. The constraint is the shared infrastructure: a book type must produce a self-contained directory with the universal outer shape, fit into the library's classification, and integrate with the catalog. Beyond that, book types are free.

## Where this is headed

### Near-term
- Define and enforce the universal book shape across all book types
- Design import — a critical book type for the library metaphor to deliver on its promise
- Add multi-axis catalog views (by date, type, medium) alongside the section view
- Design weeding and scout settling as first-class library actions
- Build the **wiki view** — a browseable static-HTML interface generated from the library catalog, working offline over `file://`. This becomes the primary browsing interface for non-CLI users and makes the library genuinely usable without invoking Claude. Catalog layer first (mechanical generation); narrative layer (LLM-assisted topics and cross-references) scaffolded now, built later.
- Rebalance the repo — library-level reference docs to match the depth of scout-level docs

### Medium-term
- Implement import and physical book types
- Implement author book type
- Narrative layer for the wiki view (topics, cross-references, related-books). Default to Claude; local model support when there's a clear path and non-technical setup instructions.
- Technical onboarding guidance woven into the process: terminal basics, reading structured data, running scripts, version control — each introduced when needed
- Plugin packaging for streamlined installation

### Long-term
- Default librarian is a local, open-source model; Claude remains the default only for the most demanding tasks (scout creation, vision-based physical book cataloging, narrative layer wiki generation)
- Q&A as a first-class interaction with books and the library as a whole
- Compounding exploration: questions and answers can be filed back into the library
- **Soft-locked section management**: sections stay stable between organizational reviews but aren't frozen forever. Claude notices when diversity drops (a section has become a catch-all) or count drifts (too many sections, or too few), proposes a reorganization, and the user approves (or accepts all in "yolo" mode). Between reviews, sections are stable — new books go into existing sections, not new ones invented ad hoc. This addresses taxonomy drift: never-updated taxonomies go stale; constantly-churning ones make nothing findable.
- The technical minimalism path proven out: people building and maintaining sophisticated personal libraries regardless of starting technical level
