# TODO

## Library foundation (highest priority)

These items earn alexandria's place over a plain folder. See ASPIRATIONS.md for the library invariants that drive them.

- [x] **Universal book shape**: defined in `docs/library/book-shape.md`. Every book has README, metadata.yaml, CLAUDE.md; universal fields are slug, title, book_type, section, description, date_added, form (binary), media_type (hierarchical), status. /new-scout updated to conform.
- [x] **Form + media_type fields on every book**: schema uses `form` (binary: digital/physical) and `media_type` (hierarchical: content_type:format, e.g., text:hardcover, text:pdf, audio:vinyl). Generated views can filter by either axis.
- [ ] **Multi-axis catalog views**: generate library views by section (current), by date added, by book type, by form, by media_type (with content-type grouping via the `:` split). All generated from `.library-index.yaml`, all browseable without Claude.
- [ ] **Library-level reference docs** (`docs/library/`): catalog format specification, classification conventions, acquisition and weeding patterns. Rebalance the repo so library docs match the depth of scout docs.
- [ ] **Universal acquisition process**: `/library` → add a book must work for any book type, ending with a catalog entry. Currently only scout has a creation flow.
- [ ] **Deduplication and linking**: during acquisition, detect likely duplicates (same title/author) and offer to link physical and digital copies as a single catalog entry with both media flagged.
- [ ] **Weeding**: design and implement removal actions. Default (`remove-book`): mark the entry as `status: removed` in the catalog with `removed_at` and optional `removed_reason`, keep the catalog entry as a historical record. Opt-in full deletion (`delete-book`): remove the entry from `.library-index.yaml` and the book's directory entirely. Both log to `library-context.md`. Rationale: a real library's card catalog keeps records of withdrawn items; knowing "I once had this" prevents re-adding the same content and preserves past interests.
- [ ] **Classification guidance**: suggest a starting taxonomy (personal, professional, reference, projects, dynamic) when creating a library. Document the user's classification in the library's root README.

## Wiki view (Pass 1 after library foundation + universal book shape)

A browseable wiki-style interface generated from the library's catalog. Multi-axis index pages, individual book pages, works offline over `file://`. Gives non-CLI users a familiar interface for daily browsing. See plan file for full design.

**Prerequisite**: universal book shape must be defined first so the generator reads a consistent `metadata.yaml` from each book.

### Pass 1: Catalog-layer wiki (complete)

- [x] **Add `tools/generate_wiki.py`** — alexandria-level generator, invoked by /library
- [x] **Add `tools/_wiki_templates.py`** — HTML templates in pure Python
- [x] **Add `tools/_wiki_style.css`** — shared stylesheet with responsive layout and dark mode
- [x] **Generator output structure**: `wiki/` with homepage, by-section, by-date, by-type, by-form, by-media-type index pages, per-book pages under `books/`, and Pass 2 placeholder at by-topic. Dropped by-author (author semantics vary across book types).
- [x] **Scout handling**: wiki book page for scouts is a thin catalog entry linking to the scout's own README. Other book types render README content inline, truncated to ~2000 words with a "continued" link for longer content.
- [x] **Removed books**: index pages show removed books with a "removed" tag and dimmed styling; individual page shows removal metadata and "resource removed" notice in place of content.
- [x] **Update `/library` skill**: add `regenerate-wiki` action; documented automatic invocation after add, remove, delete, reorganize.
- [x] **Update `tests/validate_repo.py`**: Python syntax check via `ast.parse` for all .py files in the repo.

### Pass 2: Narrative-layer wiki scaffolding (complete)

- [x] **Scaffold item 1**: placeholder `wiki/by-topic/index.html` with a message explaining the narrative layer is not yet enabled. Linked from the homepage via the axes nav so it doesn't 404.
- [x] **Scaffold item 2**: `narrative_enrich(book_data)` stub function in `tools/generate_wiki.py` that returns `{"topics": [], "related_books": []}`. Pass 1 calls it for each book and ignores the empty result. Pass 2 replaces the body, not the call sites.

### Pass 2 full implementation (deferred)

- [ ] LLM-assisted topic extraction (3-5 topics/tags per book)
- [ ] Topic pages generated when a topic appears in 2+ books
- [ ] "Related books" sections on each book page (shared topics, cross-references)
- [ ] Incremental regeneration via content hashing (only re-process changed books)
- [ ] Default to Claude; local model support when local path is clear + non-technical setup instructions ready

## Physical book type (initial implementation complete)

A record of a physical book you own. No content is copied; the catalog entry is the library's representation. Physical leads the book-type priority because users with substantial physical libraries are poorly served by existing tools, while digital-first users have many alternatives (Zotero, Readwise, various reference managers). Leading with physical signals what alexandria values.

- [x] **Design the physical book metadata schema**: universal fields plus photo, shelf_location, isbn, edition, publisher, publication_date (all optional)
- [x] **Build the /new-physical skill**: photo-based creation as primary workflow (single book or shelf of books), with manual entry as fallback or supplement, mixed-mode within a single invocation
- [x] **Photo extraction**: use best-available AI (Claude vision) to extract metadata; per-book confirmation default, "yolo" mode opt-in
- [x] **Visual record**: photograph preserved by default in the book's directory; opt-out supported
- [x] **Manual entry support**: available as primary path or fallback for failed extractions
- [x] **Shelf-of-books workflow**: multi-book extraction from one photo, per-book confirmation
- [x] **Optional online enrichment**: one batch decision (yes/no/per-book), Open Library as the source, metadata only (never content)
- [x] **/library routing**: "I have a physical book I want to catalog" → /new-physical

Remaining for later passes:
- [ ] **Privacy-first local vision model** — deferred until there's a clear path and non-technical setup instructions; defaults to Claude for now
- [ ] **Barcode-scan workflow** as an alternative entry point (photo extraction reads ISBNs when visible; dedicated scanning can come later)
- [ ] **Batch import from LibraryThing/Libib/CLZ CSV exports** for users migrating from existing tools
- [ ] **Enrichment sources beyond Open Library** (Google Books, WorldCat) if the single source proves inadequate
- [ ] **End-to-end test** of the /new-physical workflow with real photos and a test library

## Digital book type (initial implementation complete)

Digital content the user wants to bring into their library — local files, URLs, pasted text. Named `/new-digital` (not `/new-import`) to parallel `/new-physical`.

- [x] **Define the digital book schema**: universal fields plus provenance (source, imported_from, fetched_at, original_path, extracted_path for HTML)
- [x] **Build the /new-digital skill**: local files, URLs, pasted text; mixed-source batching in one invocation
- [x] **Format handling**: PDF (metadata extraction via pypdf), HTML (parsed with beautifulsoup4, rendered to content.md with html2text), markdown, plain text, images, audio, video files
- [x] **Original preservation**: content copied exactly as `original.{ext}`; never modified
- [x] **Enrichment batch decision**: yes-all / no / per-item from Open Library and Semantic Scholar; metadata only, never content
- [x] **/library routing**: "I want to add digital content I already have, or save a URL" → /new-digital

Remaining for later passes:
- [ ] **Full-text PDF extraction** — deferred; revisit when wiki Pass 2 narrative layer needs searchable text
- [ ] **OCR for scanned PDFs** — future consideration
- [ ] **Reference manager bulk import** (Zotero, Mendeley exports) — separate pass
- [ ] **More enrichment sources** — currently Open Library and Semantic Scholar

## Author book type (initial implementation complete)

A container for content the user writes themselves.

- [x] **Define scope**: notes, research, drafts, project plans, journal entries, essays — any personal writing
- [x] **Design the structure**: five purposes (project, collection, journal, notes, freeform), each with a short starter README template. No pre-created subdirectories; user creates content files as they need them.
- [x] **Build the /new-author skill**: three-step conversational flow (intent → classify → create and hand off); no extraction, no confirmation, no enrichment since the content is user-produced
- [x] **/library routing**: "I want to organize my own writing" → /new-author

Remaining for later passes:
- [ ] Help-the-user commands: drafting, reviewing, organizing assistance (currently handled ad-hoc through Claude Code reading the book's files)
- [ ] Version history integration for books with frequent edits (if git per-book proves insufficient)
- [ ] Purpose-specific skills (e.g., /new-journal, /new-project) if the usage pattern warrants shortcut skills similar to /new-hardcover

## Scout book type

- [ ] **Scout settling**: first-class action to freeze a scout into a static book (set `settled: true` in metadata.yaml, stop discovery automation, treat as a static import from that point). Support the short-lived use case explicitly.
- [x] **Make scout conform to universal book shape**: new-scout's Phase 4 now generates metadata.yaml with universal fields and `settled: false`.
- [ ] Personalization: "my context" mechanism for relating entries to user's specific situation
- [ ] Schema pattern for personalized fields
- [ ] Reduce redundancy across reference docs
- [ ] Test process end-to-end on a non-technical domain and document what breaks

## Library-level operations

- [ ] Test /library end-to-end: create library, add a book, browse, verify index
- [ ] Reorganization logic: detect when sections need subdivision, propose axes
- [ ] Index regeneration: scan library tree for metadata.yaml files and rebuild .library-index.yaml when missing or stale
- [ ] **Soft-locked section management**: sections stay stable between organizational reviews. Claude notices when a section has become a catch-all (diversity drop) or when section count has drifted (too many or too few for library size), proposes a reorganization, and the user approves per-change or accepts all ("yolo" mode). New books go into existing sections between reviews, not new ones invented ad hoc. See ASPIRATIONS.md long-term vision.

## Local librarian (long-term direction)

- [ ] Investigate which local open-source models could serve as the default librarian for library-level tasks (browsing, catalog search, cross-book Q&A)
- [ ] Design a model-abstraction layer so library-level skills can use Claude or a local model interchangeably
- [ ] Scout creation continues to default to Claude due to capability requirements; document the asymmetry clearly

## Technical onboarding guidance

- [ ] Terminal basics guide
- [ ] Claude Code onboarding: installation walkthrough, first session, what to expect
- [ ] YAML literacy: how to read and edit structured data
- [ ] Running scripts: what the scripts do, how to read output, what to do on failure
- [ ] Git basics and GitHub basics
- [ ] Order guides so each builds on the last

## Delivery

- [x] Claude Code skill as primary delivery mechanism
- [ ] Package as Claude Code plugin for streamlined installation
- [ ] Guided interactive mode for first-time users
