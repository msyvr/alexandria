## Reading and editing YAML

Every item in your collection has a `metadata.yaml` file — the catalog entry that stores the item's title, author, section, and other information. This guide explains what you're looking at when you open one, and how to make changes safely.

### What is YAML?

YAML is a way of writing structured data that's designed to be readable by humans. It looks like this:

```yaml
title: "The Dispossessed"
author: "Ursula K. Le Guin"
section: "fiction"
date_added: "2026-04-10"
```

Each line has a **field name** (like `title`), a colon, and a **value** (like `"The Dispossessed"`). That's it — field: value, one per line.

### A real metadata.yaml file

Here's what a complete item entry looks like:

```yaml
slug: "the-dispossessed"
title: "The Dispossessed"
book_type: "physical"
section: "fiction"
description: "Ursula K. Le Guin's anarchist utopia novel."
date_added: "2026-04-10"
form: "physical"
media_type: "text:hardcover"
status: "active"

author: "Ursula K. Le Guin"
user_notes: "First edition, signed. Handle with care."
provenance:
  source: "Personal collection"
  notes: "Inherited from family"

photo: "photo.jpg"
shelf_location: "Living room, top shelf"
isbn: "978-0-06-012563-3"
```

#### What each field means

The first group (required for every item):

| Field | What it is | Example |
|---|---|---|
| `slug` | URL-safe name (matches the directory name) | `the-dispossessed` |
| `title` | Display name | `The Dispossessed` |
| `book_type` | What kind of book (physical, digital, scout) | `physical` |
| `section` | Which section of the collection it's in | `fiction` |
| `description` | One-line summary | `Ursula K. Le Guin's anarchist utopia novel.` |
| `date_added` | When you added it (YYYY-MM-DD format) | `2026-04-10` |
| `form` | Physical or digital | `physical` |
| `media_type` | Specific format (content type:format) | `text:hardcover` |
| `status` | Active or removed | `active` |

The second group (optional — include what's relevant):

| Field | What it is |
|---|---|
| `author` | Who wrote or created it |
| `user_notes` | Your personal notes about this item |
| `provenance` | Where it came from and why you have it |

The third group (type-specific — varies by item type):

| Field | Which types use it |
|---|---|
| `photo` | Physical items (path to the photograph) |
| `shelf_location` | Physical items |
| `isbn` | Physical and digital items |
| `settled` | Scouts (true if frozen as a static reference) |

### How to edit metadata.yaml

Open the file in any text editor. On macOS, you can type this in the terminal:

```
open -e ~/my-collection/fiction/the-dispossessed/metadata.yaml
```

This opens it in TextEdit. Make your change, save, close. That's it.

#### What you can safely change

- **`title`** — if you want to correct the title
- **`description`** — if you want a better one-line summary
- **`user_notes`** — add, edit, or remove your personal notes anytime
- **`author`** — correct or add the author
- **`section`** — move the item to a different section (but you'll also need to move the directory; it's easier to use `/coll-menu` → reorganize for this)
- **`shelf_location`** — update where the item is on your shelf
- **`provenance`** — add notes about where the item came from

#### What you should leave alone

- **`slug`** — this matches the directory name. Changing one without the other breaks things.
- **`book_type`** — this describes what kind of book it is. Changing it doesn't change what's in the directory.
- **`date_added`** — this is the historical record of when you added it.
- **`form`** and **`media_type`** — these describe the format. If they're wrong, it's fine to correct them, but changing `form: physical` to `form: digital` doesn't make a physical item into a digital one.

#### After editing

If you've changed a field that shows up in the collection views (title, description, author, section), you'll want to regenerate the wiki so the views reflect the change:

```
uv run python tools/generate_wiki.py .
```

Or, from a Claude Code session inside your collection: ask Claude to regenerate the wiki, or use `/coll-menu` → regenerate wiki.

### YAML formatting rules

A few things to keep in mind when editing:

**Quotes around values are optional** for simple text, but recommended for anything with special characters:
```yaml
title: The Dispossessed        # works fine
title: "LLMs: A Survey"       # needs quotes because of the colon
```

**Indentation matters** for nested fields. Use spaces (not tabs), and keep the indentation consistent:
```yaml
provenance:
  source: "Personal collection"   # indented with 2 spaces
  notes: "Inherited from family"  # same indentation
```

**Null values** (empty fields) can be written as `null` or simply omitted:
```yaml
author: null       # explicitly empty
                   # or just don't include the author line at all
```

**Dates** should be in `YYYY-MM-DD` format and quoted:
```yaml
date_added: "2026-04-10"
```

If you make a formatting mistake and something breaks, the worst case is that the wiki generator or Claude Code reports an error when it tries to read the file. The fix is always: open the file, find the formatting issue, correct it. Your data is never lost — it's a text file.
