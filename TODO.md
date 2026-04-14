# TODO

## Collection foundation (highest priority)

These items earn alexandria's place over a plain folder. See ASPIRATIONS.md for the collection invariants that drive them.

- [x] **Universal book shape**: defined in `docs/coll/book-shape.md`. Every book has README, metadata.yaml, CLAUDE.md; universal fields are slug, title, book_type, section, description, date_added, form (binary), media_type (hierarchical), status. /coll-scout updated to conform.
- [x] **Form + media_type fields on every book**: schema uses `form` (binary: digital/physical) and `media_type` (hierarchical: content_type:format, e.g., text:hardcover, text:pdf, audio:vinyl). Generated views can filter by either axis.
- [ ] **Multi-axis catalog views**: generate library views by section (current), by date added, by book type, by form, by media_type (with content-type grouping via the `:` split). All generated from `.collection-index.yaml`, all browseable without Claude.
- [ ] **Library-level reference docs** (`docs/coll/`): catalog format specification, classification conventions, acquisition and weeding patterns. Rebalance the repo so library docs match the depth of scout docs.
- [ ] **Universal acquisition process**: `/coll` → add a book must work for any book type, ending with a catalog entry. Currently only scout has a creation flow.
- [ ] **Deduplication and linking**: during acquisition, detect likely duplicates (same title/author) and offer to link physical and digital copies as a single catalog entry with both media flagged.
- [ ] **Weeding**: design and implement removal actions. Default (`remove-book`): mark the entry as `status: removed` in the catalog with `removed_at` and optional `removed_reason`, keep the catalog entry as a historical record. Opt-in full deletion (`delete-book`): remove the entry from `.collection-index.yaml` and the book's directory entirely. Both log to `collection-context.md`. Rationale: a real library's card catalog keeps records of withdrawn items; knowing "I once had this" prevents re-adding the same content and preserves past interests.
- [ ] **Classification guidance**: suggest a starting taxonomy (personal, professional, reference, projects, dynamic) when creating a collection. Document the user's classification in the collection's root README.

## Wiki view (Pass 1 after collection foundation + universal book shape)

A browseable wiki-style interface generated from the collection's catalog. Multi-axis index pages, individual book pages, works offline over `file://`. Gives non-CLI users a familiar interface for daily browsing. See plan file for full design.

**Prerequisite**: universal book shape must be defined first so the generator reads a consistent `metadata.yaml` from each book.

### Pass 1: Catalog-layer wiki (complete)

- [x] **Add `tools/generate_wiki.py`** — alexandria-level generator, invoked by /coll
- [x] **Add `tools/_wiki_templates.py`** — HTML templates in pure Python
- [x] **Add `tools/_wiki_style.css`** — shared stylesheet with responsive layout and dark mode
- [x] **Generator output structure**: `wiki/` with homepage, by-section, by-date, by-type, by-form, by-media-type index pages, per-book pages under `books/`, and Pass 2 placeholder at by-topic. Dropped by-author (author semantics vary across book types).
- [x] **Scout handling**: wiki book page for scouts is a thin catalog entry linking to the scout's own README. Other book types render README content inline, truncated to ~2000 words with a "continued" link for longer content.
- [x] **Removed books**: index pages show removed books with a "removed" tag and dimmed styling; individual page shows removal metadata and "resource removed" notice in place of content.
- [x] **Update `/coll` skill**: add `regenerate-wiki` action; documented automatic invocation after add, remove, delete, reorganize.
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

A record of a physical book you own. No content is copied; the catalog entry is the collection's representation. Physical leads the book-type priority because users with substantial physical libraries are poorly served by existing tools, while digital-first users have many alternatives (Zotero, Readwise, various reference managers). Leading with physical signals what alexandria values.

- [x] **Design the physical book metadata schema**: universal fields plus photo, shelf_location, isbn, edition, publisher, publication_date (all optional)
- [x] **Build the /coll-physical skill**: photo-based creation as primary workflow (single book or shelf of books), with manual entry as fallback or supplement, mixed-mode within a single invocation
- [x] **Photo extraction**: use best-available AI (Claude vision) to extract metadata; per-book confirmation default, "yolo" mode opt-in
- [x] **Visual record**: photograph preserved by default in the book's directory; opt-out supported
- [x] **Manual entry support**: available as primary path or fallback for failed extractions
- [x] **Shelf-of-books workflow**: multi-book extraction from one photo, per-book confirmation
- [x] **Optional online enrichment**: one batch decision (yes/no/per-book), Open Library as the source, metadata only (never content)
- [x] **/coll routing**: "I have a physical book I want to catalog" → /coll-physical

Remaining for later passes:
- [ ] **Privacy-first local vision model** — deferred until there's a clear path and non-technical setup instructions; defaults to Claude for now
- [ ] **Barcode-scan workflow** as an alternative entry point (photo extraction reads ISBNs when visible; dedicated scanning can come later)
- [ ] **Batch import from LibraryThing/Libib/CLZ CSV exports** for users migrating from existing tools
- [ ] **Enrichment sources beyond Open Library** (Google Books, WorldCat) if the single source proves inadequate
- [ ] **End-to-end test** of the /coll-physical workflow with real photos and a test library

## Digital book type (initial implementation complete)

Digital content the user wants to bring into their library — local files, URLs, pasted text. Named `/coll-digital` (not `/new-import`) to parallel `/coll-physical`.

- [x] **Define the digital book schema**: universal fields plus provenance (source, imported_from, fetched_at, original_path, extracted_path for HTML)
- [x] **Build the /coll-digital skill**: local files, URLs, pasted text; mixed-source batching in one invocation
- [x] **Format handling**: PDF (metadata extraction via pypdf), HTML (parsed with beautifulsoup4, rendered to content.md with html2text), markdown, plain text, images, audio, video files
- [x] **Original preservation**: content copied exactly as `original.{ext}`; never modified
- [x] **Enrichment batch decision**: yes-all / no / per-item from Open Library and Semantic Scholar; metadata only, never content
- [x] **/coll routing**: "I want to add digital content I already have, or save a URL" → /coll-digital

Remaining for later passes:
- [ ] **Full-text PDF extraction** — deferred; revisit when wiki Pass 2 narrative layer needs searchable text
- [ ] **OCR for scanned PDFs** — future consideration
- [ ] **Reference manager bulk import** (Zotero, Mendeley exports) — separate pass
- [ ] **More enrichment sources** — currently Open Library and Semantic Scholar

## Author book type (removed)

The Author book type was removed. User-created content (notes, drafts, art, writing) is handled by `/coll-digital` (for digital files) or `/coll-physical` (for physical creations). There's no need for a separate book type when the existing types cover the use case — the `author` metadata field captures who created the content.

## Scout book type

- [x] **Scout settling**: first-class /coll action (`settle-scout`) freezes a live scout into a static book. Sets `settled: true` and `settled_at` in metadata.yaml, stops discovery automation, and the wiki generator renders settled scouts inline like other static book types (live scouts still link out). One-way action in v1; users can manually edit metadata to unsettle if needed.
- [x] **Make scout conform to universal book shape**: new-scout's Phase 4 now generates metadata.yaml with universal fields and `settled: false`.
- [ ] Personalization: "my context" mechanism for relating entries to user's specific situation
- [ ] Schema pattern for personalized fields
- [ ] Reduce redundancy across reference docs
- [ ] Test process end-to-end on a non-technical domain and document what breaks

## Library-level operations

- [x] **Weeding**: `remove-book` (default) marks a book as removed in metadata.yaml and .collection-index.yaml with `status`, `removed_at`, and `removed_reason` fields; the book's directory stays in place as a historical record. `delete-book` (opt-in, destructive) removes both the catalog entry and the book's directory entirely. Both log to `collection-context.md` via /coll-notes and trigger wiki regeneration. Section pages include removed books with a removed marker; individual book pages show the removal notice.
- [x] **Soft-locked section management**: sections are stable between organizational reviews. New books go into existing sections; `unsorted` is the fallback when no section fits. Claude notices catch-all, over-count, under-population, and "unsorted accumulation" conditions and proposes a review. The `review-sections` action in /coll walks the user through a proposal (current → proposed, per-book diff, rationale per change) and applies approved changes atomically (directory moves, metadata updates, index rebuild, wiki regen). Options: approve each individually / accept all / edit / defer. Captured in `.claude/skills/coll/SKILL.md`.
- [x] **Automated wiki generation test** (`tests/test_wiki_generation.py`): creates a synthetic 6-book library (all four types + settled scout + removed book), validates metadata against the universal shape spec, runs the wiki generator, verifies 135 checks including file existence, content rendering, settled vs live scout behavior, removed-book handling, user_notes display, and regression checks (absence of content where it shouldn't appear). Run with `uv run python tests/test_wiki_generation.py`.
- [x] **Manual testing checklist** (`tests/MANUAL_TESTING.md`): step-by-step checklist for skills-level testing in a real Claude Code session. Covers all book types, browsing, weeding, scout settling, section management, and persistent context. Not automated — requires a human.
- [ ] **Run the manual testing checklist**: actually execute the checklist in a Claude Code session and document what works and what breaks
- [ ] Index regeneration: scan collection tree for metadata.yaml files and rebuild .collection-index.yaml when missing or stale

## Local librarian (long-term direction)

- [ ] Investigate which local open-source models could serve as the default librarian for collection-level tasks (browsing, catalog search, cross-book Q&A)
- [ ] Design a model-abstraction layer so collection-level skills can use Claude or a local model interchangeably
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
