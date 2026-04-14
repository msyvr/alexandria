# /coll-menu

Guided menu for managing your personal collection. Presents the available actions
and routes to the right skill. For users who prefer to invoke skills directly, every
action listed here is also available as its own `/coll-*` command.

## How it works

Show the user the menu below. When they choose an option, invoke the corresponding
skill. If the user doesn't have a collection yet (no `.collection-index.yaml` found
in the current directory or any parent), suggest `/coll-build-new-collection` first.

## Menu

Present these options:

**Create and add:**
- **Create a new collection** → `/coll-build-new-collection`
- **Add a physical book** (photograph a book or shelf, or enter by hand) → `/coll-physical`
- **Add a hardcover** (shortcut — skips the media type question) → `/coll-hardcover`
- **Add a paperback** (shortcut) → `/coll-paperback`
- **Add digital content** (files, URLs, or pasted text) → `/coll-digital`
- **Create a scout** (a living knowledge base that monitors a domain) → `/coll-scout`

**Manage:**
- **Browse my collection** — show the table of contents in the terminal; or regenerate
  the wiki and open it in a browser
- **Remove a book** — mark a book as removed (keeps the catalog entry as a historical
  record) or fully delete it (opt-in, destructive). See "Remove a book" below.
- **Settle a scout** — freeze a live scout into a static reference. See "Settle a scout"
  below.
- **Review sections** — propose reorganization when sections have grown or drifted. See
  "Soft-locked section management" below.
- **Regenerate wiki** — rebuild the browseable HTML view from the current catalog
- **Update skills** — copy the latest skills from the alexandria repo into this
  collection. See "Update skills" below.
- **Save notes** → `/coll-notes`

## Adapting to the user

Same principle as other skills: gauge technical comfort, use plain language by default.
"Your collection" not "the index." "Sections" not "taxonomy." Present the menu in
whatever form feels natural — a numbered list, a conversational offer, whatever suits
the user's style.

For new users, explain briefly what each option does. For returning users who know
the commands, be concise.

## Browse

Two modes:

**Quick browse** (default): show the collection's table of contents in the terminal,
organized by section:

```
My Collection
├── Fiction
│   ├── The Dispossessed (physical, text:hardcover)
│   └── Short Stories (digital, text:markdown)
└── Research
    ├── AI Safety Scout (scout, live)
    └── Causal Inference Primer (digital, text:pdf)
```

Read `.collection-index.yaml` to build the TOC. If the index is missing or stale,
regenerate it by scanning the collection tree for `metadata.yaml` files.

**Full browse**: regenerate the wiki (`uv run python {alexandria-repo}/tools/generate_wiki.py {collection-path}`) and open `wiki/index.html` in the default browser.

## Remove a book (weeding)

Two removal modes. Default keeps a historical record; full deletion is opt-in.

**Default: remove-book** — marks the book as removed but keeps the catalog entry and
directory intact.

1. Identify the book to remove (ask by title or slug; confirm the match).
2. Ask for a removal reason (optional but encouraged).
3. Confirm the action before making changes.
4. Update `metadata.yaml`: set `status: removed`, `removed_at: YYYY-MM-DD`,
   `removed_reason: "..."`.
5. Update `.collection-index.yaml` to match.
6. Invoke `/coll-notes` to log the removal in `collection-context.md`.
7. Regenerate the wiki.

**Opt-in: delete-book** — fully removes the catalog entry and deletes the book's
directory. Destructive.

1. Identify the book. Confirm the match.
2. Warn clearly: this deletes the book's directory and removes the catalog entry.
   Only the log entry in `collection-context.md` will remain.
3. Ask for a deletion reason.
4. Require explicit confirmation ("yes, delete").
5. Remove from `.collection-index.yaml`.
6. Delete the book's directory.
7. Invoke `/coll-notes` to log the deletion in `collection-context.md`.
8. Regenerate the wiki.

## Settle a scout

Freezes a live scout into a static reference.

1. Identify the scout. Confirm `book_type: scout` and `settled: false`.
2. Ask for an optional note about why they're settling.
3. Update `metadata.yaml`: set `settled: true`, `settled_at: YYYY-MM-DD`.
4. Stop any discovery automation (describe what's being disabled).
5. Invoke `/coll-notes` to log the settling.
6. Regenerate the wiki (settled scouts render inline instead of linking out).

## Soft-locked section management

Sections are stable between organizational reviews. New books go into existing
sections; `unsorted` is the fallback when nothing fits. Claude proposes a review when
conditions suggest the structure isn't serving the collection:

**Triggers** (mention to the user when noticed, but don't force a review):
- A section has 15+ books (getting catch-all-y)
- The collection has 50+ books but only 2-3 sections
- A section has fewer than 3 books in a collection with 20+
- More than ~12 top-level sections
- Visibly unrelated topics sharing a section
- 5+ books in "unsorted"

**review-sections workflow**:
1. Read `.collection-index.yaml` and each book's metadata.
2. Identify what triggered the review.
3. Propose a new section structure (rename, split, merge, create, move books).
4. Show the user: current → proposed, per-book diff, rationale per change.
5. Let the user: approve each individually / accept all / edit / defer.
6. Execute: create dirs, mv book dirs, update metadata.yaml `section` fields,
   update `.collection-index.yaml`, rmdir emptied sections.
7. Invoke `/coll-notes` to log the review.
8. Regenerate the wiki.

## Update skills

Copies the latest skills from the alexandria source repo into this collection.

1. Read `source_repo` from `.collection-index.yaml`.
2. Check that the path exists and has `.claude/skills/`.
3. If the path is missing, ask the user for the current path to the alexandria repo.
4. Copy `.claude/skills/` from the source repo into the collection's `.claude/skills/`,
   overwriting existing files.
5. Confirm what was updated.

## Collection index cache format

The `.collection-index.yaml` at the collection root is a regenerable cache of universal
fields from every book's `metadata.yaml`. Type-specific fields are not in the cache.

```yaml
collection_name: "my-collection"
created: "2026-04-07"
source_repo: "/Users/me/alexandria"
sections:
  fiction:
    books:
      - slug: "the-dispossessed"
        title: "The Dispossessed"
        book_type: "physical"
        description: "Ursula K. Le Guin's anarchist utopia novel."
        date_added: "2026-04-10"
        form: "physical"
        media_type: "text:hardcover"
        status: "active"
        author: "Ursula K. Le Guin"
        path: "fiction/the-dispossessed"
```

### Regenerating the index

If missing or stale, rebuild by scanning the collection tree for `metadata.yaml` files,
reading universal fields, grouping by section.

## Wiki view

The collection has a generated wiki at `{collection}/wiki/index.html`. Regenerate
with the `regenerate-wiki` menu option or directly via:

```
uv run python {alexandria-repo}/tools/generate_wiki.py {collection-path}
```
