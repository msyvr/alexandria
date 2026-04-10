# TODO

## Library foundation (highest priority)

These items earn alexandria's place over a plain folder. See ASPIRATIONS.md for the library invariants that drive them.

- [ ] **Universal book shape**: define what every book directory must contain (README, metadata, classification) regardless of type. Document in library-level reference docs. Update /new-scout to conform.
- [ ] **Medium field on every book**: catalog entries include `medium` (digital, physical, both). Generated views can filter/group by medium.
- [ ] **Multi-axis catalog views**: generate library views by section (current), by date added, by book type, by source, by medium. All generated from `.library-index.yaml`, all browseable without Claude.
- [ ] **Library-level reference docs** (`docs/library/`): catalog format specification, classification conventions, acquisition and weeding patterns. Rebalance the repo so library docs match the depth of scout docs.
- [ ] **Universal acquisition process**: `/library` → add a book must work for any book type, ending with a catalog entry. Currently only scout has a creation flow.
- [ ] **Deduplication and linking**: during acquisition, detect likely duplicates (same title/author) and offer to link physical and digital copies as a single catalog entry with both media flagged.
- [ ] **Weeding**: design and implement archive and delete actions. Archiving moves a book to an archived section and keeps the catalog entry. Deleting removes both. Both log to `library-context.md`.
- [ ] **Classification guidance**: suggest a starting taxonomy (personal, professional, reference, projects, dynamic) when creating a library. Document the user's classification in the library's root README.

## Import book type (top priority after library foundation)

Import is the most important book type for the library metaphor. Design pass needed:

- [ ] **Define import concretely**: copy vs reference (recommend copy), raw vs processed (recommend both), unit of import (flexible: single document or collection), provenance metadata (mandatory: source, date, user's reason)
- [ ] **Design the import schema**: what metadata fields are required, what are optional
- [ ] **Build the /new-import skill** (following the /new-scout pattern, adapted to the library metaphor — less AI-heavy creation process)
- [ ] **Support common source types**: PDFs, web pages (with archival snapshot), downloaded files, plain notes

## Physical book type (high priority — may be primary use for some users)

A record of a physical book you own. No content is copied; the catalog entry is the library's representation.

- [ ] **Design the physical book metadata schema**: title, author, medium (set to physical), optional photo, optional online summary, provenance (when/where acquired), classification, shelf location
- [ ] **Build the /new-physical skill**: photo-based creation as primary workflow (single book or shelf of books), with manual entry as fallback or supplement
- [ ] **Photo extraction**: use best-available AI (vision model) to extract title, author, and other visible metadata from the photo. Default to user confirmation per book; support a "yolo" mode that accepts extracted metadata without per-book confirmation (opt-in)
- [ ] **Privacy-first mode**: support local vision model alternative for users who don't want photos processed remotely
- [ ] **Optional online enrichment**: with user permission, fetch public metadata and summaries from open book databases (Open Library, Google Books, etc.). Clearly opt-in; default off for privacy-first users. Book content never leaves the user's shelf; only public bibliographic data is fetched.
- [ ] **Visual record**: preserve the photograph as part of the book's content for users who want it (useful for reference and for offline users to see their own shelves)
- [ ] **Manual entry support**: users who can't or don't want to photograph should be able to populate records by hand
- [ ] **Shelf-of-books workflow**: from a single shelf photo, create multiple book entries (one per book visible), each with its own catalog entry

## Author book type

- [ ] Define scope: notes, research, drafts, project plans, task lists, journal entries
- [ ] Design the structure: templates for common uses vs fully freeform
- [ ] Build the /new-author skill

## Scout book type

- [ ] **Scout settling**: first-class action to freeze a scout into a static book (mark as settled, stop discovery automation, treat as a static import from that point). Support the short-lived use case explicitly.
- [ ] **Make scout conform to universal book shape** (once defined)
- [ ] Personalization: "my context" mechanism for relating entries to user's specific situation
- [ ] Schema pattern for personalized fields
- [ ] Reduce redundancy across reference docs
- [ ] Test process end-to-end on a non-technical domain and document what breaks

## Library-level operations

- [ ] Test /library end-to-end: create library, add a book, browse, verify index
- [ ] Reorganization logic: detect when sections need subdivision, propose axes
- [ ] Index regeneration: scan directory for git repos when index is missing/stale

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
