# Manual testing checklist

The automated tests (`validate_repo.py`, `test_wiki_generation.py`) cover metadata validation, link integrity, Python syntax, and wiki generation. The skills themselves — the markdown instructions Claude Code reads and executes — can only be tested by running real Claude Code sessions.

This checklist defines what "done" looks like for skills-level testing. Run through it in a Claude Code session whenever the skills have been significantly updated.

## Setup

- [ ] Install the skills: `cp -r ~/alexandria/skills/* ~/.claude/skills/`
- [ ] Install dependencies: `cd ~/alexandria && uv sync`

## Library creation

- [ ] Start Claude Code and type `/library`
- [ ] Create a new library (accept default name or choose your own)
- [ ] Verify: library directory created with `.library-index.yaml`

## Physical book — single book

- [ ] `/new-physical` (or `/new-hardcover` for the shortcut)
- [ ] Provide a photo of a single book
- [ ] Verify: Claude extracts title and author from the photo
- [ ] Confirm the metadata (or edit fields)
- [ ] Verify: book directory created with `metadata.yaml`, `README.md`, `CLAUDE.md`, photo preserved
- [ ] Verify: `.library-index.yaml` updated with the new book entry

## Physical book — shelf photo

- [ ] `/new-physical` with a shelf photo (5+ books visible)
- [ ] Verify: Claude identifies multiple books from spines
- [ ] Confirm some, edit one, skip one
- [ ] Verify: correct number of books created (confirmed + edited, not skipped)

## Digital book — local file

- [ ] `/new-digital` with a local PDF file path
- [ ] Verify: pypdf extracts title/author from PDF metadata
- [ ] Verify: `original.pdf` preserved in the book's directory, no `content.md` (PDF policy)

## Digital book — URL

- [ ] `/new-digital` with a URL (a real article or web page)
- [ ] Verify: URL fetched, content archived as `original.html`, `content.md` extraction created
- [ ] Verify: provenance records `imported_from: url` and `fetched_at`

## Digital book — pasted text

- [ ] `/new-digital` and paste a block of text with a title
- [ ] Verify: `original.txt` stored, `media_type: text:plaintext`

## Author book

- [ ] `/new-author`
- [ ] Choose a purpose (e.g., "project")
- [ ] Verify: book directory created with starter README matching the chosen purpose
- [ ] Verify: no pre-created subdirectories (only universal files)

## Scout

- [ ] `/new-scout` with a small topic (e.g., "the top 5 programming languages")
- [ ] Verify: the seven-phase process runs through at least scope and research
- [ ] (Full scout testing takes longer; confirm at least the first 2-3 phases work)

## Browsing

- [ ] `/library` → browse (terminal view): verify the TOC lists all added books
- [ ] `/library` → regenerate-wiki
- [ ] Open `~/my-library/wiki/index.html` in a browser
- [ ] Verify: homepage shows correct book count and recent additions
- [ ] Click through: by-section, by-date, by-type, by-form, by-media-type indexes
- [ ] Verify: each index page lists the expected books
- [ ] Click a book: verify the book page shows metadata and content (or link-out for live scout)

## Weeding

- [ ] `/library` → remove-book: choose a book, give a reason
- [ ] Verify: book's metadata.yaml shows `status: removed`, `removed_at`, `removed_reason`
- [ ] Verify: wiki shows the book with "removed" marker on section page and removal notice on book page
- [ ] `/library` → delete-book: choose a different book, confirm destructive action
- [ ] Verify: book directory and catalog entry are both gone
- [ ] Verify: wiki no longer shows the deleted book anywhere

## Scout settling

- [ ] (If a scout was created above) `/library` → settle-scout
- [ ] Verify: metadata.yaml shows `settled: true` and `settled_at`
- [ ] Regenerate wiki
- [ ] Verify: settled scout's wiki page renders content inline (not link-out)

## Section management

- [ ] Add books until a section has 10+ items
- [ ] Verify: Claude mentions the possibility of a section review
- [ ] `/library` → review-sections
- [ ] Verify: Claude proposes a reorganization with rationale
- [ ] Accept or edit the proposal
- [ ] Verify: books moved to new sections, metadata.yaml `section` fields updated, wiki regenerated

## Persistent context

- [ ] `/take-notes` inside a book directory
- [ ] Verify: `context.md` created (or appended to) with a timestamped checkpoint
- [ ] Verify: `CLAUDE.md`'s "Recent context" section updated
- [ ] Start a new Claude Code session in the same book directory
- [ ] Ask Claude something that depends on prior context
- [ ] Verify: Claude reads `context.md` and has awareness of the prior session

## Cleanup

- [ ] Delete the test library when done
