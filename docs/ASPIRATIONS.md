## Project Aspirations

### The thesis

As AI takes on more of the work of making, editing, and organizing digital material, retaining control of one's own work has begun to depend on a small, practical fluency. Not programming — a narrower set: terminal use, structured text, directing an AI assistant, a sense of what a file is and whether you own it, and light version control as insurance. A person who is comfortable with those few things can remain in control of their own work as AI continues to advance. A person who is not is increasingly renting the capability from whoever made the nearest app.

Alexandria is for people who would like that fluency but have not yet built it. The collection — a private library of books, papers, notes, research, whatever else is worth holding onto — is the vehicle for developing it. Each skill comes up in the course of the work, when there is something concrete to apply it to. The finished collection is entirely the user's, and continues to work whether or not any AI is running.

### What you are learning

Five skills, picked for leverage rather than breadth:

1. Working in a terminal — enough to navigate, start tools, and recover from small mistakes.
2. Reading structured data — YAML and markdown with frontmatter, as a shape rather than as a language.
3. Directing an AI assistant — prompting, reviewing, pushing back, verifying.
4. File ownership in practice — what a local file is, what a format is, whether the data is yours.
5. Version control as insurance — git, used lightly, against mistakes on files you care about.

The set is smaller than "learn to code" and considerably more leveraged for a person whose work is not programming. Someone who can direct AI and verify the result can accomplish a great deal without becoming a developer — not by learning to program, but by learning what to ask for and what to check.

The curriculum is built into the workflow. The five skills are not studied in isolation; they surface when the work calls for them, and Claude is there to explain each one as it appears.

### The collection itself

Alexandria borrows from the real-world library: a curated collection where things live in predictable places, findable by catalog or by browsing the stacks, with or without a librarian's help. This is not a product claim but a pedagogical choice — the library metaphor gives the reader something concrete and spatial to reason about while the underlying files teach what they are.

The collection is a directory on your machine. Inside it, "items" are the things you hold — self-contained units with a consistent outer shape. Some items are content you have collected from elsewhere. Some are your own writing. A few are dynamic — living resources that update themselves, called **scouts**, which can be "settled" into static items when they are done. The collection's job is to hold them, organize them, and make them browseable. Your job is to decide what goes in.

Alexandria is AI-assisted, but not AI-dependent. A librarian (Claude Code today, a local open-source model eventually) helps with cataloging, search, and cross-item questions — but every feature of the collection works without one. You can browse the catalog, walk the sections, and read any item without invoking any AI at all.

### Why not just a plain folder?

A folder with subfolders is fine at ten items. By the time you have a hundred, you can't find anything you didn't name carefully, you can't remember why half of it is there, and nothing ties related items together.

Alexandria adds the minimum structure that makes a collection browseable at scale:

| Concern                            | Plain folder             | Alexandria                        |
| ---------------------------------- | ------------------------ | --------------------------------- |
| Finding an item without opening it | Filename only            | Catalog with metadata             |
| Consistent item shape              | Whatever was dropped     | Every item has known structure    |
| Classification conventions         | Arbitrary subdirectories | Sections with documented patterns |
| Browseable view                    | `ls` or Finder           | Generated catalog, multiple axes  |
| Context about why items are there  | None                     | Per-item metadata and history     |
| Works without AI assistance        | No, at scale             | Yes — that's the point            |

The structure is deliberately lightweight. It's not a database. It's not an app. It's files on disk, organized in a way that scales past a few hundred items without requiring an AI to navigate.

### Who this is for

People who would like a working fluency with their own digital material in the presence of AI, and are open to developing it as they go. No prior technical background is expected — the process introduces what is needed when it is needed. Software engineers who would rather not build the scaffolding from scratch are equally welcome.

The tool meets people where they are technically. For readers new to a terminal, the setup is the first occasion to use most of the skills above. For technical readers, it skips the hand-holding and gets to the result.

### Why these five, specifically

The five skills above are chosen deliberately. Adjacent skills — writing full applications, understanding networking, configuring CI — are valuable but not minimum. The test is: what is the smallest set such that a person whose work is not programming can still exercise meaningful control over their own digital material as AI proliferates?

The defense for this specific set:

- Terminal and structured data are the substrate. Most useful digital artifacts are structured files that can be read and run from a terminal. A person who cannot see past the app layer loses visibility into what they own.
- Directing an AI assistant is the leverage. With it, the other four skills are recoverable — one can ask Claude to explain the YAML, teach git when it is needed, diagnose a terminal error. Without it, each small friction becomes a dead end.
- File ownership and version control are the insurance. AI is going to touch one's files; some of those touches will be wrong. If the earlier version cannot be recovered, or if the data cannot be read without the app that wrote it, "you own this" is not literally true.

This is the literacy floor, not a programming curriculum.

### Collection invariants

These derive from the real-world collection metaphor and are the acceptance criteria for alexandria's design. Every invariant must hold for the collection to earn its place over a plain folder.

1. **Every item has a catalog entry.** Title, author/source, major_section (top-level grouping), section (specific subsection), description, date added, item type, form (digital or physical), media_type (hierarchical: content_type:format, e.g., text:hardcover, text:pdf, audio:vinyl). You can find an item without opening it.
2. **Every item has a consistent outer shape.** Regardless of item type: a README (the spine), metadata (the catalog entry), and content files.
3. **The catalog is browseable by multiple axes.** Not just by directory structure — the full catalog (All, sortable by date added, date acquired, author/artist, title), By section (grouped by major section), By author/artist, By medium & format. Views are generated from the catalog and rendered as static HTML in the wiki.
4. **Classification is convention-based and learnable.** Sections are directories. The user chooses their taxonomy; alexandria suggests starting patterns and documents them.
5. **Acquisition is a first-class process.** Adding an item requires determining type, populating the catalog, recording provenance.
6. **Weeding is a first-class process.** Items can be removed through a defined process. Default behavior keeps the catalog entry and marks the resource as removed (preserving the record that the item was once in the collection); full deletion is available as an opt-in. Both log to `collection-context.md`.
7. **Dynamic content is an exception, and can be settled.** Scouts are allowed but marked as dynamic. Users can freeze a scout into a static item at any time.
8. **The librarian is optional — and eventually local.** Every library feature is usable without AI. Claude accelerates it; a local open-source model will eventually be the default librarian.

9. **Items record their form and media_type.** Every catalog entry includes a `form` field (binary: digital or physical — where does this live?) and a `media_type` field (hierarchical: content_type:format — what specifically is this? e.g., `text:hardcover`, `text:pdf`, `audio:vinyl`). The two axes let users browse by both dimensions: "show me my physical items" (form) or "show me my vinyl collection" (media_type). Linking duplicates across form (same work in physical and digital) is deferred — for v1, duplicates are separate entries.

### Item types

An item type defines how content of a particular kind gets created, organized, and maintained. All item types share the universal outer shape (README, metadata, classification, catalog entry) and the collection's infrastructure. Beyond that, each type has its own creation process and conventions.

#### Physical (planned, top priority)

A record of a physical item (or other physical item) you own. Unlike import, no content is copied — the item itself lives on your shelf. The catalog entry is the collection's representation of the item. Creation is primarily photo-based: photograph a single item or a whole shelf, and the librarian extracts title, author, and other metadata from the image. Manual entry is supported as well, with or without a photo. An optional visual record (the photograph itself) is preserved.

For users who permit it, the librarian can also fetch publicly available metadata and summaries (from open book databases) to enrich the record — the book's content never leaves your shelf, but its title and author are public information. This is opt-in for privacy-first users who prefer fully offline operation.

**Physical is the top-priority item type.** The cataloging space has solid tools for standard use cases — LibraryThing, Libib, and CLZ Books handle barcode scanning, metadata retrieval, and cloud sync well. Where alexandria differentiates:

- **Shelf photo workflow with strong accuracy**: Photograph a whole shelf and get a draft catalog of every item visible. The one existing tool attempting this (Shelf Scan, launched 2024) has reportedly poor accuracy because it uses weaker vision models. Alexandria can meaningfully beat this by defaulting to best-available vision models.
- **Local-first, files you own**: Most existing tools are cloud-first. Alexandria's files live on your machine, browseable without the app, portable forever.
- **No subscription lock-in**: Free and unlimited.
- **Integration with other item types**: Alexandria holds physical items alongside digital imports, user-authored content, and scouts in a single library. No existing cataloging tool spans all these.

Leading with physical also signals what alexandria values: the considered, ownership-oriented approach to personal knowledge, where an item on your shelf is as first-class as a PDF on your drive.

Best-quality AI is the default for photo extraction (vision models benefit from stronger models), with a local-model option for privacy-first users.

#### Digital (available now)

Digital content the user wants to bring into their collection — local files (PDFs, HTML, markdown, text, images, audio, video), URLs to fetch and archive, or pasted text. This includes the user's own work (notes, drafts, creative output) as well as content from other sources. Content is copied into the collection, preserved exactly in its original format, and cataloged with extracted metadata. Runs through `/coll-digital`.

#### Scout (available now)

A knowledge base on a topic, actively maintained by AI — researched, organized, critiqued, and kept current through discovery scripts. A scout is the fullest expression of what this collection makes possible: a resource on a subject the user cares about, built and owned by them, rather than a subscription to a generic version of it.

A scout can be **short-lived** (built for an immediate need, updated briefly, then settled into a static reference) or **long-lived** (kept updating indefinitely for an evolving domain). The user decides when to settle a scout — to freeze it as a static item in the collection. Most items in a mature collection are static, as most holdings in a library are; scouts are the ones that keep moving until the user decides otherwise.

Because scout creation depends on capabilities that currently only the best models have (research, critique, editorial writing), scouts remain Claude-assisted even as the collection librarian shifts to local models. This asymmetry is intentional: the collection foundation should be maximally portable; the ambitious item-building work can reasonably require better models.

#### Future types

The architecture accommodates item types not yet designed. The constraint is the shared infrastructure: an item type must produce a self-contained directory with the universal outer shape, fit into the collection's classification, and integrate with the catalog. Beyond that, item types are free.

### Where this is headed

#### Near-term (largely complete)

- ✅ Universal item shape defined and enforced across all three item types
- ✅ Physical, digital, and scout item types all implemented
- ✅ Multi-axis catalog views generated by the wiki (All with client-side sort by date added / date acquired / author / title, By section grouped by major section, By author/artist, By medium & format)
- ✅ Weeding (`remove-item` non-destructive default, `delete-item` opt-in) and scout settling implemented as first-class `/coll` actions
- ✅ **Wiki view** (catalog layer) — browseable static HTML generated from the collection catalog, working offline over `file://`. Homepage with summary and recent additions; multi-axis index pages; individual item pages rendered inline for static item types (including settled scouts) and link-out for live scouts. This is the primary browsing interface for non-CLI users and makes the collection genuinely usable without invoking Claude. The narrative layer (LLM-assisted topics and cross-references) is scaffolded but not yet built.
- ✅ **Soft-locked section management** — sections are stable between organizational reviews. New items go into existing sections; `unsorted` is the fallback. Claude notices catch-all, size-drift, and unsorted-accumulation conditions and proposes a review via `/coll` → review-sections. Addresses the classification drift problem: never-updated taxonomies go stale; constantly-churning ones make nothing findable.
- Library-level reference docs to rebalance against the depth of scout-level docs (partial — `docs/collection/book-shape.md` exists)

#### Medium-term

- Narrative layer for the wiki view (topics, cross-references, related-items). Default to Claude; local model support when there's a clear path and non-technical setup instructions.
- Technical onboarding guidance woven into the process: terminal basics, reading structured data, running scripts, version control — each introduced when needed
- Plugin packaging for streamlined installation
- End-to-end user testing across all three item types and collection operations

#### Long-term

- Default librarian is a local, open-source model; Claude remains the default only for the most demanding tasks (scout creation, vision-based physical item cataloging, narrative layer wiki generation)
- Q&A as a first-class interaction with items and the collection as a whole
- Compounding exploration: questions and answers can be filed back into the collection
- The technical minimalism path proven out: people building and maintaining sophisticated personal libraries regardless of starting technical level
