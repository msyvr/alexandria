# Manual testing checklist

The automated tests (`validate_repo.py`, `test_wiki_generation.py`) cover metadata validation, link integrity, Python syntax, and wiki generation. The skills themselves — the markdown instructions Claude Code reads and executes — can only be tested by running real Claude Code sessions.

This checklist defines what "done" looks like for skills-level testing. Run through it in a Claude Code session whenever the skills have been significantly updated.

## Setup

- [ ] Install the skills: `cp -r ~/alexandria/skills/* ~/.claude/skills/`
- [ ] Install dependencies: `cd ~/alexandria && uv sync`

## Collection creation

- [ ] Start Claude Code from the alexandria repo directory and type `/coll-build-new-collection`
- [ ] Create a new collection (accept default name or choose your own)
- [ ] Verify: collection directory created with `.collection-index.yaml` and `.claude/skills/` populated

## Physical item — single item

- [ ] `/coll-physical` (or `/coll-hardcover` for the shortcut)
- [ ] Provide a photo of a single item
- [ ] Verify: Claude extracts title and author from the photo
- [ ] Confirm the metadata (or edit fields)
- [ ] Verify: item directory created with `metadata.yaml`, `README.md`, `CLAUDE.md`, photo preserved
- [ ] Verify: `.collection-index.yaml` updated with the new item entry

## Physical item — shelf photo

- [ ] `/coll-physical` with a shelf photo (5+ items visible)
- [ ] Verify: Claude identifies multiple items from spines
- [ ] Confirm some, edit one, skip one
- [ ] Verify: correct number of items created (confirmed + edited, not skipped)

## Digital item — local file

- [ ] `/coll-digital` with a local PDF file path
- [ ] Verify: pypdf extracts title/author from PDF metadata
- [ ] Verify: `original.pdf` preserved in the item's directory, no `content.md` (PDF policy)

## Digital item — URL

- [ ] `/coll-digital` with a URL (a real article or web page)
- [ ] Verify: URL fetched, content archived as `original.html`, `content.md` extraction created
- [ ] Verify: provenance records `imported_from: url` and `fetched_at`

## Digital item — pasted text

- [ ] `/coll-digital` and paste a block of text with a title
- [ ] Verify: `original.txt` stored, `media_type: text:plaintext`

## User-created content (via /coll-digital)

- [ ] `/coll-digital` with a markdown file you've written
- [ ] Verify: file imported, metadata populated, `book_type: digital`
- [ ] Verify: the `author` field can be set to your name if desired

## Scout — create new

- [ ] `/coll-new-scout` with a small topic (e.g., "the top 5 programming languages")
- [ ] Verify: the seven-phase process runs through at least scope and research
- [ ] (Full scout testing takes longer; confirm at least the first 2-3 phases work)

## Scout — import existing

- [ ] Build a scout independently first (outside the collection), or have one from a previous session
- [ ] `/coll-scout` and provide the path to the existing scout directory
- [ ] Verify: scout directory moved/copied into the collection under the right section
- [ ] Verify: metadata.yaml present with universal fields + `book_type: scout`
- [ ] Verify: `.collection-index.yaml` updated

## Browsing

- [ ] `/coll` → browse (terminal view): verify the TOC lists all added items
- [ ] `/coll` → regenerate-wiki
- [ ] Open `~/my-collection/wiki/index.html` in a browser
- [ ] Verify: homepage shows correct item count and recent additions
- [ ] Click through: by-section, by-date, by-type, by-form, by-media-type indexes
- [ ] Verify: each index page lists the expected items
- [ ] Click an item: verify the item page shows metadata and content (or link-out for live scout)

## Weeding

- [ ] `/coll` → remove-item: choose an item, give a reason
- [ ] Verify: item's metadata.yaml shows `status: removed`, `removed_at`, `removed_reason`
- [ ] Verify: wiki shows the item with "removed" marker on section page and removal notice on item page
- [ ] `/coll` → delete-item: choose a different item, confirm destructive action
- [ ] Verify: item directory and catalog entry are both gone
- [ ] Verify: wiki no longer shows the deleted item anywhere

## Scout settling

- [ ] (If a scout was created above) `/coll` → settle-scout
- [ ] Verify: metadata.yaml shows `settled: true` and `settled_at`
- [ ] Regenerate wiki
- [ ] Verify: settled scout's wiki page renders content inline (not link-out)

## Section management

- [ ] Add items until a section has 10+ items
- [ ] Verify: Claude mentions the possibility of a section review
- [ ] `/coll` → review-sections
- [ ] Verify: Claude proposes a reorganization with rationale
- [ ] Accept or edit the proposal
- [ ] Verify: items moved to new sections, metadata.yaml `section` fields updated, wiki regenerated

## Persistent context

- [ ] `/coll-notes` inside an item directory
- [ ] Verify: `context.md` created (or appended to) with a timestamped checkpoint
- [ ] Verify: `CLAUDE.md`'s "Recent context" section updated
- [ ] Start a new Claude Code session in the same item directory
- [ ] Ask Claude something that depends on prior context
- [ ] Verify: Claude reads `context.md` and has awareness of the prior session

## Cleanup

- [ ] Delete the test library when done
