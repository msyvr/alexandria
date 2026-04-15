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
- **Add a physical item** (photograph an item or shelf, or enter by hand) → `/coll-physical`
- **Add a hardcover** (shortcut — skips the media type question) → `/coll-hardcover`
- **Add a paperback** (shortcut) → `/coll-paperback`
- **Add digital content** (files, URLs, or pasted text) → `/coll-digital`
- **Create a new scout** (a living knowledge base that monitors a domain) → `/coll-new-scout`
- **Import an existing scout** (one built independently, outside the collection) → `/coll-scout`

**Manage:**
- **Browse my collection** — show the table of contents in the terminal; or regenerate
  the wiki and open it in a browser
- **Remove an item** — mark an item as removed (keeps the catalog entry as a historical
  record) or fully delete it (opt-in, destructive). See "Remove an item" below.
- **Settle a scout** — freeze a live scout into a static reference. See "Settle a scout"
  below.
- **Review sections** — propose reorganization when sections have grown or drifted. See
  "Soft-locked section management" below.
- **Regenerate wiki** — rebuild the browseable HTML view from the current catalog
- **Update skills** → `/coll-update-from-latest-alexandria`
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

**Full browse**: regenerate the wiki (`uv run python tools/generate_wiki.py .` from the collection directory) and open `wiki/index.html` in the default browser.

## Remove an item (weeding)

Two removal modes. Default keeps a historical record; full deletion is opt-in.

**Default: remove-item** — marks the item as removed but keeps the catalog entry and
directory intact.

1. Identify the item to remove (ask by title or slug; confirm the match).
2. Ask for a removal reason (optional but encouraged).
3. Confirm the action before making changes.
4. Update `metadata.yaml`: set `status: removed`, `removed_at: YYYY-MM-DD`,
   `removed_reason: "..."`.
5. Update `.collection-index.yaml` to match.
6. Invoke `/coll-notes` to log the removal in `collection-context.md`.
7. Regenerate the wiki.

**Opt-in: delete-item** — fully removes the catalog entry and deletes the item's
directory. Destructive.

1. Identify the item. Confirm the match.
2. Warn clearly: this deletes the item's directory and removes the catalog entry.
   Only the log entry in `collection-context.md` will remain.
3. Ask for a deletion reason.
4. Require explicit confirmation ("yes, delete").
5. Remove from `.collection-index.yaml`.
6. Delete the item's directory.
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

Sections are stable between organizational reviews. New items go into existing
sections; `unsorted` is the fallback when nothing fits. Claude proposes a review when
conditions suggest the structure isn't serving the collection:

**Triggers** (mention to the user when noticed, but don't force a review):
- A section has 15+ items (getting catch-all-y)
- The collection has 50+ items but only 2-3 sections
- A section has fewer than 3 items in a collection with 20+
- More than ~12 top-level sections
- Visibly unrelated topics sharing a section
- 5+ items in "unsorted"

**review-sections workflow**:
1. Read `.collection-index.yaml` and each item's metadata.
2. Identify what triggered the review.
3. Propose a new section structure (rename, split, merge, create, move items).
4. Show the user: current → proposed, per-item diff, rationale per change.
5. Let the user: approve each individually / accept all / edit / defer.
6. Execute: create dirs, mv item dirs, update metadata.yaml `section` fields,
   update `.collection-index.yaml`, rmdir emptied sections.
7. Invoke `/coll-notes` to log the review.
8. Regenerate the wiki.

## Collection index cache format

The `.collection-index.yaml` at the collection root is a regenerable cache of universal
fields from every item's `metadata.yaml`. Type-specific fields are not in the cache.

```yaml
collection_name: "my-collection"
created: "2026-04-07"
sections:
  fiction:
    items:
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
uv run python tools/generate_wiki.py .
```
