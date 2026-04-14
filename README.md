# alexandria

Lightweight private collection infrastructure for books and other content/items you own, keep, and reference — physical and digital alike.

Alexandria provides minimal structure to make a collection browseable at scale: a catalog, consistent book shape, classification conventions, and generated views. The structure is lightweight enough that you can browse it without invoking any AI at all.

Alexandria borrows heavily from the real-world library: a curated collection where items are stored in predictable places, findable by catalog or by walking the stacks. The collection is a directory on your machine. Inside it, "books" are the things you hold — self-contained units with a consistent shape. Most books are content you've collected from elsewhere or written yourself. A few may be dynamic, living resources that update themselves (see [scout](#scout-available-now--the-exception-not-the-rule)). The collection's job is to hold them, organize them, and make them browseable — with or without an agent-librarian's help.

See [ASPIRATIONS.md](ASPIRATIONS.md) for the full vision, collection invariants, and where this project is headed. If you're new to working in a terminal, see the [detailed setup walkthrough](#detailed-setup-walkthrough) at the end of this page.

## Who is this for?

Anyone who wants to organize a private collection independently — to own the result rather than depend on an external platform, and to have the ability to use the collection without any special or proprietary software. Content can be viewed in any browser, in a simple format. No technical background required, though technical users are equally welcome.

### An optional side benefit: technical upskilling

For users who want it, alexandria doubles as a low-friction path to a disproportionately useful skill set: knowing how to direct AI tools effectively without needing to become a programmer. Building real things you actually need — opening a terminal, reading structured data, running scripts, understanding what "you own this data" means technically — teaches you what matters and what doesn't. The skills transfer well beyond this tool. See [ASPIRATIONS.md](ASPIRATIONS.md) for more on the technical minimalism philosophy.

If that's not your goal, clear instructions are provided for building and extending your collection. After that, exploring it as as easy as using Wikipedia.

## Book types

All book types share a universal outer shape: a README (the spine), metadata (the catalog entry), and content. Each type has its own creation process within that shape.

### Physical

A record of a physical book you own. No content is copied — the book lives on your shelf; the catalog entry represents it in your collection. Creation is photo-based: photograph a single book or a whole shelf, and alexandria extracts title, author, and other metadata from the image (with your confirmation). Manual entry works too, with or without a photo. Optional online metadata and summaries are available for users who want them. Run `/coll-physical` or `/coll` → add a book → physical.

Existing cataloging tools (LibraryThing, Libib, CLZ Books) handle barcode scanning and standard metadata well. Alexandria differentiates on shelf photo accuracy (using stronger vision models than existing apps), local-first ownership (files on your machine, not in someone's cloud), no subscription, and integration with other book types in a single library. Leading with physical signals what alexandria values: a book on your shelf is as first-class as a PDF on your drive.

### Digital

Digital content you want to bring into the collection — local files (PDFs, HTML, markdown, text, images, audio, video), URLs to fetch and archive, or pasted text. The collection copies the content, preserves the original exactly, and extracts metadata so you can find it later. Run `/coll-digital` or `/coll` → add a book → digital.

### Scout

A living knowledge base that monitors a domain. Unlike import and author, a scout is actively maintained by AI — researched, organized, systematically critiqued, and kept current through automated discovery. Scouts are powerful but are the exception rather than the rule: most library holdings should be static, like most of a real library's holdings.

A scout can be **short-lived** (built for an immediate need, updated briefly, then settled into a static reference) or **long-lived** (kept updating indefinitely for an evolving domain). You decide when to settle a scout — to freeze it as a static book in your collection.

Scout is useful when a topic is complex enough to warrant careful organization, personal enough that no generic tool quite fits, and evolving fast enough that a static resource goes stale. For example: navigating a complex medical situation, monitoring a professional field, or tracking fast-moving developments.

## Getting started

### What you need

- **[Claude Code](https://claude.ai/claude-code)** — the AI assistant that creates books and manages the collection. Included with a [Claude Pro subscription](https://claude.com/pricing) ($20/month). Runs in your terminal, [in a browser](https://claude.ai/code), or via the phone app ([iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684), [Android](https://play.google.com/store/apps/details?id=com.anthropic-claude)). Browser and phone require a GitHub-hosted library.
- **Python 3.10+** — for scripts within built scouts. Check with `python3 --version`.
- No coding experience required. You guide the process by answering questions; Claude Code generates all scripts and data files. See [ASPIRATIONS.md](ASPIRATIONS.md) for more on the skills you'll pick up along the way.

### Create your collection

1. Install Claude Code: [claude.ai/claude-code](https://claude.ai/claude-code)
2. Clone the alexandria repo and install dependencies:
   ```
   git clone https://github.com/msyvr/alexandria.git
   cd alexandria
   uv sync
   ```
3. Start Claude Code from the alexandria repo directory and type `/coll-build-new-collection`
4. Name your collection (or accept the default) and choose where to create it
5. The skill copies the collection skills into your new collection's `.claude/skills/` directory automatically

After creation, work from your collection directory:

```
cd ~/my-collection
claude
```

All `/coll-*` commands are available inside the collection directory. No global skill installation needed.

### Add a book

From `/coll`, choose "add a book" and describe what you need:

- "I have a physical book I want to catalog" — runs /coll-physical
- "I want to photograph my bookshelf and catalog the books" — runs /coll-physical with the shelf workflow
- "I want to add these PDFs (or URLs, or notes) to my library" — runs /coll-digital
- "I need to understand treatment options for [condition]" — runs /coll-scout
- "I want to track developments in [field]" — runs /coll-scout

Claude Code determines the appropriate book type and guides you through building it. Physical and scout book types are available now; import and author are planned.

### Day-to-day use

- **Browse**: open `~/alexandria/wiki/index.html` in any browser — the wiki view gives you a familiar, navigable interface with multi-axis indexes (by section, date, type, form, media type). Works fully offline. No terminal needed for daily browsing.
- **Add more books**: `/coll` → add a book (the wiki regenerates automatically after each addition)
- **Update a book**: `cd` into it and work with Claude Code directly
- **Reorganize**: `/coll` → reorganize when the structure needs adjusting
- **Remove a book**: `/coll` → remove-book (keeps the catalog entry marked as removed) or `delete-book` (removes the entry entirely)
- **Regenerate the wiki manually**: `/coll` → regenerate-wiki (or run the generator directly via `uv run python ~/alexandria/tools/generate_wiki.py ~/my-collection`)

## What uses Claude Code and what doesn't

**Requires Claude Code** (internet + Anthropic account): Creating a new collection, adding books, and creating scouts (the scout process involves research, schema design, editorial writing, systematic critique, and script generation). During these tasks, your prompts and responses pass through Anthropic's servers. Your data files — YAML, markdown, scripts — remain on your machine and are not uploaded.

**Works fully offline, no AI or subscription needed:** Reading and browsing your collection, navigating via HTML links, regenerating READMEs, editing entries, running discovery scripts. Once built, the files are entirely yours and work independently of any service.

**No local model alternative currently exists for creating scouts.** The scout's seven-phase process — particularly research, critique, and editorial writing — depends on Claude's capabilities. The skills are plain markdown instructions; if a local-model agent runner with comparable quality becomes available, they will work without modification.

**Long-term direction**: the default librarian will be a local, open-source model. Library-level tasks (browsing, cataloging, search, cross-book questions) don't require Claude's capabilities and shouldn't depend on a subscription. Claude will remain the default only for scout creation and maintenance, where the quality gap meaningfully matters. Users who never build scouts will eventually be able to use alexandria with only a local model.

## What's in this repo

### Skills

- [/coll-build-new-collection](.claude/skills/coll-build-new-collection/SKILL.md) — create a new collection (run once from the alexandria repo)
- [/coll-menu](.claude/skills/coll-menu/SKILL.md) — guided menu for all collection actions
- [/coll-physical](.claude/skills/coll-physical/SKILL.md) — catalog a physical book from a photo or manual entry
- [/coll-hardcover](.claude/skills/coll-hardcover/SKILL.md) — shortcut for a hardcover (calls /coll-physical with media_type pre-set)
- [/coll-paperback](.claude/skills/coll-paperback/SKILL.md) — shortcut for a paperback
- [/coll-digital](.claude/skills/coll-digital/SKILL.md) — bring digital content (files, URLs, text) into the collection
- [/coll-scout](.claude/skills/coll-scout/SKILL.md) — create a scout for any topic
- [/coll-notes](.claude/skills/coll-notes/SKILL.md) — save notes about a book or the collection

### Reference docs

- [docs/scout/](docs/scout/) — process phases, critique checklist, schema patterns, walkthroughs

### Project direction

- [ASPIRATIONS.md](ASPIRATIONS.md) — project vision, collection architecture, technical minimalism, planned book types
- [TODO.md](TODO.md) — planned additions and improvements

---

## Detailed setup walkthrough

Step-by-step instructions assuming no prior terminal experience. Every command is shown exactly as you'll type it.

### 1. Open a terminal

- **macOS**: Press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows**: Install WSL (Windows Subsystem for Linux) from the Microsoft Store, then open Ubuntu from the Start menu.
- **Linux**: Open your Terminal or Konsole application.

### 2. Check that Python is installed

```
python3 --version
```

You should see something like `Python 3.13.2`. If you see "command not found," install Python from [python.org/downloads](https://python.org/downloads).

### 3. Check that Git is installed

```
git --version
```

You should see something like `git version 2.43.0`. If not:

- **macOS**: `xcode-select --install`
- **Windows (WSL)**: `sudo apt install git`
- **Linux**: `sudo apt install git` (Ubuntu/Debian) or `sudo dnf install git` (Fedora)

### 4. Install Claude Code

Go to [claude.ai/claude-code](https://claude.ai/claude-code) and follow the installation instructions. You'll need an Anthropic account.

Verify: `claude --version`

### 5. Download alexandria

```
cd ~
git clone https://github.com/msyvr/alexandria.git
```

### 6. Install uv and alexandria's Python dependencies

Alexandria uses [uv](https://docs.astral.sh/uv/) to manage Python dependencies. Install uv (one-time):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install alexandria's dependencies:

```
cd ~/alexandria
uv sync
```

This creates a virtual environment in `~/alexandria/.venv` and installs everything alexandria needs (PyYAML, requests, markdown-it-py, BeautifulSoup, html2text, pypdf).

### 7. Create your collection

Start Claude Code from the alexandria repo directory:

```
cd ~/alexandria
claude
```

At the Claude Code prompt, type:

```
/coll-build-new-collection
```

Name your collection and choose where to create it. The skill copies the collection skills into your new collection's `.claude/skills/` directory.

### 8. Work from your collection

For all future sessions, start Claude Code from your collection directory:

```
cd ~/my-collection
claude
```

Type `/coll-` and hit tab to see all available commands. Or type `/coll-menu` for a guided menu.

All `/coll-*` commands are available here. Type `/coll` and hit tab to see the full list.

### 9. Add your first book (from your collection directory)

From the `/coll` prompt, choose "add a book" and describe what you need. A few examples:

- **Physical book**: "I have a physical book I want to catalog" — you'll be asked for a photo (single book or shelf) or to enter the metadata by hand
- **Digital content**: "I want to add these files" or "save this URL" — files are copied, URLs are fetched and archived, metadata is extracted (also use this for your own writing — markdown notes, drafts, anything you've created)
- **Scout**: "I need to understand treatment options for [condition]" or "I want to track developments in [field]" — Claude Code builds a structured knowledge base through a seven-phase process

Claude Code guides you from there, asking the questions relevant to the book type you chose. You provide the direction; it handles the construction.

### 10. Browse your collection

In Claude Code: `/coll` → browse

In a browser:

- **macOS**: `open ~/alexandria/index.html`
- **Windows (WSL)**: `explorer.exe $(wslpath -w ~/alexandria/index.html)`
- **Linux**: `xdg-open ~/alexandria/index.html`

### 11. Add more books

In Claude Code: `/coll` → add a book. Same process as step 9.

### Troubleshooting

**"command not found"**: The tool isn't installed. Return to the relevant step above.

**"permission denied"**: Try `sudo` before the command (e.g., `sudo cp -r ...`).

**`/coll` not recognized**: Re-run step 7. Ensure `~/.claude/skills/` exists.

**Other issues**: Start Claude Code and describe the problem — it can often diagnose and fix things directly.
