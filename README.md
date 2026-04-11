# alexandria

Lightweight library infrastructure for the books and content you want to own, keep, and reference — physical and digital alike.

Alexandria borrows from the real-world library: a curated collection where things live in predictable places, findable by catalog or by walking the stacks. The library is a directory on your machine. Inside it, "books" are the things you hold — self-contained units with a consistent shape. Most books are content you've collected from elsewhere or written yourself. A few may be dynamic, living resources that update themselves. The library's job is to hold them, organize them, and make them browseable — with or without a librarian's help.

**Why not just a plain folder?** A folder is fine at ten items. At a hundred, you can't find anything you didn't name carefully, you can't remember why half of it is there, and nothing ties related items together. Alexandria adds the minimum structure that makes a collection browseable at scale: a catalog, consistent book shape, classification conventions, and generated views. The structure is lightweight enough that you can browse it without invoking any AI at all.

See [ASPIRATIONS.md](ASPIRATIONS.md) for the full vision, library invariants, and where this project is headed. If you're new to working in a terminal, see the [detailed setup walkthrough](#detailed-setup-walkthrough) at the end of this page.

## Who is this for?

Anyone who would benefit from an organized, personal collection of structured digital content — and wants to own the result rather than depend on someone else's platform. No technical background required, though technical users are equally welcome.

### An optional side benefit: technical upskilling

For users who want it, alexandria doubles as a low-friction path to a disproportionately useful skill set: knowing how to direct AI tools effectively without needing to become a programmer. Building real things you actually need — opening a terminal, reading structured data, running scripts, understanding what "you own this data" means technically — teaches you what matters and what doesn't. The skills transfer well beyond this tool. See [ASPIRATIONS.md](ASPIRATIONS.md) for more on the technical minimalism philosophy.

If that's not your goal, fine — alexandria still works the same way. You get a library; the upskilling is opt-in.

## Book types

All book types share a universal outer shape: a README (the spine), metadata (the catalog entry), and content. Each type has its own creation process within that shape.

### Physical (available now)
A record of a physical book you own. No content is copied — the book lives on your shelf; the catalog entry represents it in your library. Creation is photo-based: photograph a single book or a whole shelf, and alexandria extracts title, author, and other metadata from the image (with your confirmation). Manual entry works too, with or without a photo. Optional online metadata and summaries are available for users who want them. Run `/new-physical` or `/library` → add a book → physical.

Existing cataloging tools (LibraryThing, Libib, CLZ Books) handle barcode scanning and standard metadata well. Alexandria differentiates on shelf photo accuracy (using stronger vision models than existing apps), local-first ownership (files on your machine, not in someone's cloud), no subscription, and integration with other book types in a single library. Leading with physical signals what alexandria values: a book on your shelf is as first-class as a PDF on your drive.

### Digital (available now)
Digital content you want to bring into the library — local files (PDFs, HTML, markdown, text, images, audio, video), URLs to fetch and archive, or pasted text. The library copies the content, preserves the original exactly, and extracts metadata so you can find it later. Run `/new-digital` or `/library` → add a book → digital.

### Author (coming soon)
Content you produce yourself — notes, research, drafts, project plans, task lists, journal entries. Structured enough to be searchable, flexible enough for freeform writing.

### Scout (available now — the exception, not the rule)
A living knowledge base that monitors a domain. Unlike import and author, a scout is actively maintained by AI — researched, organized, systematically critiqued, and kept current through automated discovery. Scouts are powerful but are the exception rather than the rule: most library holdings should be static, like most of a real library's holdings.

A scout can be **short-lived** (built for an immediate need, updated briefly, then settled into a static reference) or **long-lived** (kept updating indefinitely for an evolving domain). You decide when to settle a scout — to freeze it as a static book in your library.

Scout is useful when a topic is complex enough to warrant careful organization, personal enough that no generic tool quite fits, and evolving fast enough that a static resource goes stale. For example: navigating a complex medical situation, monitoring a professional field, or tracking fast-moving developments.

## Getting started

### What you need

- **[Claude Code](https://claude.ai/claude-code)** — the AI assistant that creates books and manages the library. Included with a [Claude Pro subscription](https://claude.com/pricing) ($20/month). Runs in your terminal, [in a browser](https://claude.ai/code), or via the phone app ([iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684), [Android](https://play.google.com/store/apps/details?id=com.anthropic-claude)). Browser and phone require a GitHub-hosted library.
- **Python 3.10+** — for scripts within built scouts. Check with `python3 --version`.
- No coding experience required. You guide the process by answering questions; Claude Code generates all scripts and data files. See [ASPIRATIONS.md](ASPIRATIONS.md) for more on the skills you'll pick up along the way.

### Create your library

1. Install Claude Code: [claude.ai/claude-code](https://claude.ai/claude-code)
2. Install the alexandria skills (one-time):
   ```
   git clone https://github.com/msyvr/alexandria.git
   cp -r alexandria/skills/* ~/.claude/skills/
   ```
3. Start Claude Code and type `/library`
4. Name your library (or accept the default: "alexandria")

Your library is now set up — an organized directory ready to hold books.

### Add a book

From `/library`, choose "add a book" and describe what you need:

- "I have a physical book I want to catalog" — runs /new-physical
- "I want to photograph my bookshelf and catalog the books" — runs /new-physical with the shelf workflow
- "I want to add these PDFs (or URLs, or notes) to my library" — runs /new-digital
- "I need to understand treatment options for [condition]" — runs /new-scout
- "I want to track developments in [field]" — runs /new-scout

Claude Code determines the appropriate book type and guides you through building it. Physical and scout book types are available now; import and author are planned.

### Day-to-day use

- **Browse**: open `~/alexandria/wiki/index.html` in any browser — the wiki view gives you a familiar, navigable interface with multi-axis indexes (by section, date, type, form, media type). Works fully offline. No terminal needed for daily browsing.
- **Add more books**: `/library` → add a book (the wiki regenerates automatically after each addition)
- **Update a book**: `cd` into it and work with Claude Code directly
- **Reorganize**: `/library` → reorganize when the structure needs adjusting
- **Remove a book**: `/library` → remove-book (keeps the catalog entry marked as removed) or `delete-book` (removes the entry entirely)
- **Regenerate the wiki manually**: `/library` → regenerate-wiki (or run the generator directly via `uv run python ~/alexandria/tools/generate_wiki.py ~/my-library`)

## What uses Claude Code and what doesn't

**Requires Claude Code** (internet + Anthropic account): Creating a new library, adding books, and creating scouts (the scout process involves research, schema design, editorial writing, systematic critique, and script generation). During these tasks, your prompts and responses pass through Anthropic's servers. Your data files — YAML, markdown, scripts — remain on your machine and are not uploaded.

**Works fully offline, no AI or subscription needed:** Reading and browsing your library, navigating via HTML links, regenerating READMEs, editing entries, running discovery scripts. Once built, the files are entirely yours and work independently of any service.

**No local model alternative currently exists for creating scouts.** The scout's seven-phase process — particularly research, critique, and editorial writing — depends on Claude's capabilities. The skills are plain markdown instructions; if a local-model agent runner with comparable quality becomes available, they will work without modification.

**Long-term direction**: the default librarian will be a local, open-source model. Library-level tasks (browsing, cataloging, search, cross-book questions) don't require Claude's capabilities and shouldn't depend on a subscription. Claude will remain the default only for scout creation and maintenance, where the quality gap meaningfully matters. Users who never build scouts will eventually be able to use alexandria with only a local model.

## What's in this repo

### Skills
- [/library](skills/library/SKILL.md) — create and manage your library (main entry point)
- [/new-physical](skills/new-physical/SKILL.md) — catalog a physical book from a photo or manual entry
- [/new-hardcover](skills/new-hardcover/SKILL.md) — shortcut for a hardcover (calls /new-physical with media_type pre-set)
- [/new-paperback](skills/new-paperback/SKILL.md) — shortcut for a paperback
- [/new-digital](skills/new-digital/SKILL.md) — bring digital content (files, URLs, text) into the library
- [/new-scout](skills/new-scout/SKILL.md) — create a scout for any topic
- [/take-notes](skills/take-notes/SKILL.md) — maintain persistent context in a book or library

### Reference docs
- [docs/scout/](docs/scout/) — process phases, critique checklist, schema patterns, walkthroughs

### Project direction
- [ASPIRATIONS.md](ASPIRATIONS.md) — project vision, library architecture, technical minimalism, planned book types
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

### 7. Install the skills

```
mkdir -p ~/.claude/skills
cp -r ~/alexandria/skills/* ~/.claude/skills/
```

No output means it worked.

### 8. Create your library

```
claude
```

At the Claude Code prompt, type:
```
/library
```

Name your library (or press Enter for "alexandria"). Your library directory is now set up.

### 9. Add your first book

From the `/library` prompt, choose "add a book" and describe what you need. A few examples:

- **Physical book**: "I have a physical book I want to catalog" — you'll be asked for a photo (single book or shelf) or to enter the metadata by hand
- **Digital content**: "I want to add these files" or "save this URL" — files are copied, URLs are fetched and archived, metadata is extracted
- **Scout**: "I need to understand treatment options for [condition]" or "I want to track developments in [field]" — Claude Code builds a structured knowledge base through a seven-phase process

Claude Code guides you from there, asking the questions relevant to the book type you chose. You provide the direction; it handles the construction.

### 10. Browse your library

In Claude Code: `/library` → browse

In a browser:
- **macOS**: `open ~/alexandria/index.html`
- **Windows (WSL)**: `explorer.exe $(wslpath -w ~/alexandria/index.html)`
- **Linux**: `xdg-open ~/alexandria/index.html`

### 11. Add more books

In Claude Code: `/library` → add a book. Same process as step 9.

### Troubleshooting

**"command not found"**: The tool isn't installed. Return to the relevant step above.

**"permission denied"**: Try `sudo` before the command (e.g., `sudo cp -r ...`).

**`/library` not recognized**: Re-run step 7. Ensure `~/.claude/skills/` exists.

**Other issues**: Start Claude Code and describe the problem — it can often diagnose and fix things directly.
