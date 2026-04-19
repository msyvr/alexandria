# /coll-digital

Bring digital content into the collection — files you already have on your machine, URLs
you want to save, or text you want to paste in. The collection copies the content, extracts
readable metadata, and creates a catalog entry conforming to the universal item shape
(see `docs/coll/book-shape.md`).

"Digital" here means the same thing it does for `/coll-physical`: the form of the
catalog entry. A physical item record catalogs something that lives on a shelf; a
digital item record catalogs content that lives as files in the collection. The name
is symmetric with `/coll-physical` and deliberately doesn't use "import" — which could
mislead users into thinking the skill only fetches from elsewhere.

## Before starting

Detect the collection context by walking up from the current directory looking for
`.collection-index.yaml`. If not found, explain that /coll-digital must run inside an
alexandria collection and offer to help create one with /coll.

## The workflow

Four things need to happen, conversationally:

1. **Gather intent and input** — what's being added and from where
2. **Extract candidates** — produce a list of draft item records
3. **Confirm, edit, optionally enrich** — user reviews each candidate
4. **Classify, create, record** — write the item directories and update the index

### 1. Gather intent and input

Ask the user what they're adding. Inputs can be **mixed in a single invocation**: a
user might say "add these 3 PDFs from my Downloads folder, plus these 2 URLs I saved,
plus this snippet I want to keep." All get processed as one batch.

Input types:
- **Local files**: individual paths or a directory
- **URLs**: one or more web addresses the collection will fetch and archive
- **Pasted text**: user provides a title and the text

If the user wants to skip per-item confirmation for clean extractions, they can opt
into **yolo mode** here. Partial and failed extractions still require user input.

**Validation**:
- Files: exist, readable, not empty
- URLs: reachable (a quick HEAD request is sufficient)
- Pasted text: title and content both present

If inputs fail validation, report and offer alternatives.

### 2. Extract candidates

Produce a list of candidate item records. Each candidate has draft metadata: title,
author if detectable, description, and the right `media_type` (a `{content_type}:{format}`
value from the v1 vocabulary — see book-shape.md).

**Local files** — extract based on format:

- **PDF**: read embedded metadata with pypdf (title, author, creation date, subject).
  If metadata is sparse, fall back to filename as title. Set `media_type: text:pdf`.
- **HTML (local)**: parse with beautifulsoup4 — `<title>`, meta tags (`author`,
  `description`, `og:title`, `og:description`), main content area. Set
  `media_type: text:html`.
- **Markdown**: read YAML frontmatter if present (look for `title`, `author`, `description`
  fields). Otherwise use the first `#` heading as title. Set `media_type: text:markdown`.
- **Plain text**: use the first non-empty line as title; filename as fallback. Set
  `media_type: text:plaintext`.
- **Image** (jpg, png, heic, gif, webp): use EXIF metadata if present; filename as title.
  Set `media_type: image:digital`.
- **Audio files** (mp3, flac, wav, m4a, ogg): use filename as title; `media_type: audio:digital`.
- **Video files** (mp4, mov, mkv, avi, webm): use filename as title; `media_type: video:digital`.
- **Other formats**: use filename as title; `media_type: text:plaintext` for recognized
  text formats, otherwise ask the user.

**URLs** — fetch with requests:
1. Do a GET with a reasonable timeout
2. Check `Content-Type` header:
   - `application/pdf` → download as-is; run pypdf metadata extraction
   - `text/html` → parse with beautifulsoup4; extract title, author from meta tags;
     extract main content for the content.md preview
   - Other → download and store; use URL as title fallback
3. Record `imported_from: url`, `fetched_at: {ISO timestamp}` in provenance
4. Set `media_type` from the response content type

**Pasted text** — user provides the title directly. `media_type: text:plaintext`.

**Candidate confidence**:
- **Clean**: title and (when applicable) author detected; user can confirm
- **Partial**: title detected but author missing, or vice versa; user can accept or edit
- **Failed**: no useful metadata; requires manual entry before confirmation

**Failure modes**:
- Unreadable or corrupt file → report, offer different file or manual entry
- Unreachable URL → report, offer different URL or manual entry
- Paywalled URL (returns login page) → detect heuristically (short content,
  login-related title), warn the user, let them decide whether to keep the fetched
  content or skip
- Parser extracts nothing useful → fall back to filename/URL as title, mark as failed

### 3. Confirm, edit, optionally enrich

**Default mode**: for each candidate, show the draft metadata (title, author,
description, media_type, provenance) and let the user confirm, edit fields, or skip.
A skipped candidate doesn't become an item. Failed candidates require manual entry
before they can be confirmed.

**Yolo mode**: accept clean extractions as-is. Partial and failed still prompt for
user input.

**Enrichment** is a single batch decision after candidates are confirmed:

> "For these N items, want me to fetch public metadata from open databases? (Items →
> Open Library; academic papers → Semantic Scholar.) Options: yes-all / no / per-item."

- **yes-all**: fetch metadata for every confirmed candidate, present fetched data for
  a final accept-all or edit-individually pass
- **no**: skip enrichment entirely. Nothing is sent to external services.
- **per-item**: ask the user per candidate

Enrichment fetches only bibliographic metadata — title, author, publisher, subjects,
short description. Item content is never fetched. General web content (not matching
an item or paper) doesn't get enrichment; the source URL is its provenance.

### 4. Classify, create, record

**Propose a major section and section** for each confirmed candidate.
Major section is the top-level grouping on the By section wiki view
(`Books`, `Research papers`, `Visual`, `Audio`, `Personal`, `Etc` —
user can supply a custom name). Section is the specific subsection
(e.g., `ai safety`, `fiction`, `photographs`). The same subsection
name can live under different majors (e.g., `Books / ai safety`
vs. `Research papers / ai safety`), so both must be captured.

For section:

- **Local file batch from a single directory**: propose one section as the batch
  default (based on directory name, content subjects, and recent placements). Let the
  user accept or override per file.
- **URL batch (mixed sources)**: propose per-URL based on content. Present all
  proposals as a list with "accept all" / "edit individually" / "set one section for
  all" options — same pattern as enrichment.
- **Single item**: propose based on content and recent placements.

**Generate a slug** from the title per `docs/coll/book-shape.md` rules. Check
uniqueness; suffix with `-2`, `-3` if needed.

**Create the item directory** at `{library}/{section}/{slug}/`.

**Copy or save the content** using the filename convention
`{slug}-{original-stem}.{ext}` — the item slug, a hyphen, the original filename
stem (basename without extension), then a dot and the original extension preserved
with its original case. The original bytes are preserved exactly.

- Local files: e.g., `Oxford_canal_boat_church_20200701.JPEG` imported for an item
  titled "Oxford canal boat & church" becomes
  `oxford-canal-boat-church-Oxford_canal_boat_church_20200701.JPEG`
- URL-fetched content: use the URL's basename stem when present, otherwise fall back
  to the slug alone. Extensions by content type:
  - HTML → `.html` (e.g., `my-item.html` or `my-item-<url-stem>.html`)
  - PDF → `.pdf`
  - Other → extension from the response content type
- Pasted text: `{slug}.txt`

The original is preserved exactly as received. Alexandria does not modify the source.

**Write the universal files**:

- `metadata.yaml` — catalog entry (template below)
- `README.md` — the item's spine (template below)
- `content.md` — **only** for HTML sources: a one-time markdown extraction via html2text.
  Not regenerated automatically. User hand-edits persist across re-runs. Not created
  for PDF, plain text, markdown, or other formats.
- `{slug}-{original-stem}.{ext}` — the preserved source (see naming convention above)

**PDFs are preserved as-is with no `content.md`.** The README links to `original.pdf`
and tells the user to open it in their PDF viewer. Full-text extraction is intentionally
not done in this skill — it's lossy, dependency-heavy, and users open PDFs in PDF
viewers anyway.

**Update `.collection-index.yaml`** with each new item's universal fields. For multi-item
batches, update once at the end rather than per item.

**Commit the item(s) to the collection's git repo** (silent no-op if version control
isn't enabled). Once per invocation, after all item files and the index are written:

```
uv run python tools/commit_change.py {collection_path} \
  --message "Add digital item: {title}" \
  .collection-index.yaml \
  {section}/{slug}
```

For batches, use a single commit with a message like
`"Add {N} digital items"` and pass all section/slug paths plus the index.

**Invoke /coll-notes** once at the end of the invocation to log the import batch to
`collection-context.md`: how many items were added, what sources, any notable preferences
observed (e.g., "user declined online enrichment").

## metadata.yaml template

```yaml
# Universal fields
slug: "{generated-slug}"
title: "{confirmed title}"
book_type: "digital"
major_section: "{selected major section}"
section: "{selected section}"
description: "{generated — see below}"
date_added: "{today's date, YYYY-MM-DD}"
form: "digital"
media_type: "{inferred or user-selected, e.g., text:pdf}"
status: "active"

# Universal optional
author: "{canonical name only — e.g., 'Ursula Le Guin', not 'Written by Ursula Le Guin'}"
author_role: "{role as it would be phrased before the name — Author (default for text), Writer, Director, Photographer, Artist, Performer, Composer, Producer, Illustrator, Translator, Editor, Narrator, Curator. Infer from media_type when possible: video:* → Director, audio:* (music) → Artist, image:* → Photographer, text:* → Author. Ask the user if ambiguous.}"
date_created: "{the date the work itself was made — publication date for papers/articles, release date for audio/video, date taken for photos (often available in EXIF), date written for user-authored drafts; ISO date, year+month, or just year}"
acquired_at: "{YYYY-MM-DD, if the user knows when they got this item}"
provenance:
  source: "{original file path or URL}"
  notes: "{user-provided context, or omit}"
  imported_from: "local-file"         # local-file, url, or pasted-text
  fetched_at: "2026-04-10T14:23:00Z"  # only for url source
  original_path: "{slug}-{original-stem}.{ext}"  # e.g., "oxford-canal-boat-church-Oxford_canal_boat_church_20200701.JPEG"
  extracted_path: "content.md"        # only if HTML extraction was created
```

**Description generation**: compose a short natural-prose description (1–3
sentences) that reads on its own. The grid already shows title, author,
role, date, format, section, and source; so the description focuses on
**subject, premise, and notable context** — what the item is *about*, not
the catalog attributes.

Template: `{subject/genre phrase}{, optional one-sentence premise}{, optional tail of notable secondary credits or context}`

Loose scope: light repetition with grid fields is fine when the grammar
wants it. The rule is "read naturally," not "zero overlap."

Per-type guidance:

- **Paper / research article**: research domain + central claim or question + (optional) co-authors, methodology, venue
  - e.g. *"Retrieval-augmented generation study evaluating context-window effects on hallucination rates across three model families. Co-authored with Chen and Nakamura; NeurIPS 2024."*
- **Article / web content**: topic + main point + (optional) source context
  - e.g. *"Profile of the 1968 Memphis sanitation strike, reconstructed from union archives. Long-form essay from The Atlantic's 50th-anniversary series."*
- **Digital audio**: genre + concept or era + (optional) featured players, producers
- **Digital video**: genre + premise + (optional) notable cast, director, production context
- **Digital image / photograph**: subject + location + (optional) context, camera or series
  - e.g. *"Narrowboat moored on the Oxford canal at golden hour, with a 14th-century church rising behind. Part of a summer canal-walk series."*
- **User-authored writing (drafts, notes, essays)**: topic/type + angle or purpose + (optional) status
  - e.g. *"Working notes on continuous-integration strategies for monorepos. Collected while evaluating Bazel migration at work."*

Fallback when little is known: empty description (the item page simply
won't render a description line).

## README.md template

The README is both the wiki's content source and a standalone readable
document on disk (for browsing an item's directory in a markdown reader
without alexandria). The layout follows the catalog-style convention:
identification → reference card → body. The two `<!-- alexandria:metadata-*
-->` HTML comments are invisible in rendered markdown but act as
deterministic delimiters for the wiki generator's stripper — everything
between them is dropped from the wiki item page because the page already
renders those fields as a structured grid.

Byline wording is role-aware: use the `author_role` to phrase it
(`*Photographed by Ansel Adams*`, `*Written by Ursula Le Guin*`,
`*by Ursula Le Guin*` for default Author). If role is absent or equals
`Author`, use `*by {author}*`; otherwise use `*{role-verb} by {author}*`.

```markdown
# {title}

{if author:} *{role-aware byline}*

{description}

<!-- alexandria:metadata-start -->

## Catalog entry

- **Title**: {title}
- **{role-aware author label}**: {author}
- **Created**: {date_created if known}
- **Acquired**: {acquired_at if known}
- **Added**: {date_added}
- **Section**: {major_section} / {section}
- **Format**: {media_type} ({form})

## Source

- **Original**: `{original_path}` ({media_type})
{if imported_from == "url":}
- **Fetched from**: [{url}]({url})
- **Fetched at**: {fetched_at}
{if imported_from == "local-file":}
- **Imported from**: `{source path}`
{if provenance.notes:}
- **Notes**: {notes}

<!-- alexandria:metadata-end -->

{if HTML extracted:}
## Content

{readable extraction from content.md, embedded in full if under ~500 words,
otherwise a preview with a link to content.md for the full extraction}

{if PDF or other binary format:}
## Content

Content is preserved in its original format. Open `{original_path}` to view.

See `metadata.yaml` for the full catalog entry.
```

No CLAUDE.md is generated for digital items. The metadata.yaml is self-documenting
and Claude can derive operational context from it directly.

## Dependencies

/coll-digital relies on these Python libraries (installed via `uv sync` from the
alexandria `pyproject.toml`):

- `pypdf` — PDF metadata extraction (title, author, creation date). Not used for
  full-text extraction.
- `beautifulsoup4` — HTML parsing for local and URL-fetched HTML
- `html2text` — HTML-to-markdown conversion for the content.md extraction
- `requests` — URL fetching
- `pyyaml` — YAML read/write for metadata.yaml and .collection-index.yaml

If any dependency is missing, report clearly and suggest `uv sync` in the alexandria
repo directory.

## Adapting to the user

Use plain language. "Digital content" not "imported resources." "Fetch the page" not
"HTTP GET." When extraction is uncertain, say so: "I couldn't find a clean title in
the PDF metadata — the filename is `document-3-final.pdf`. What should this be called?"

Respect privacy defaults. Enrichment is opt-in and defaults to "ask." The user's
prompts and the extraction operations don't send anything to external services beyond
the explicit URL fetches they provided and the optional enrichment lookups.

## Privacy and data handling

- **Files and URLs are processed locally** wherever possible. URL fetching uses
  requests directly from the user's machine. Local files are read from disk.
- **The LLM running this skill** sees the file paths, URLs, and extracted content in
  order to reason about them — that's inherent to how Claude Code skills work. The
  content is not sent to any other service.
- **Enrichment is opt-in** and fetches only bibliographic metadata (title, author,
  publisher, subjects, short description) from Open Library or Semantic Scholar.
  Item content is never fetched.
- **No crawling**: the skill fetches only URLs the user explicitly provides. It does
  not follow links or discover related content.
- **Originals are preserved exactly** in the item's directory. Alexandria does not
  convert or modify them.

## What /coll-digital does not do

- Does not extract full text from PDFs (only metadata)
- Does not convert files between formats
- Does not strip DRM or bypass paywalls
- Does not crawl, follow links, or discover related content
- Does not upload files to any service beyond optional enrichment metadata lookups
