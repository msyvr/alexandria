# alexandria

Lightweight private collection infrastructure for items and other content/items you own, keep, and reference — physical and digital alike.

Alexandria provides minimal structure to make a collection browseable at scale: a catalog, consistent item shape, classification conventions, and generated views. The structure is lightweight enough that you can browse it without invoking any AI at all.

> **Getting started?** You'll work in two windows: this page (for reference) and a terminal (where you type commands). If you're new to the terminal, start with the [detailed walkthrough](#detailed-setup-walkthrough) — it shows every step. If you're comfortable in the terminal, jump to the [quick start](#create-your-collection).

Alexandria borrows heavily from the real-world library: a curated collection where items are stored in predictable places, findable by catalog or by walking the stacks. The collection is a directory on your machine. Inside it, "items" are the things you hold — self-contained units with a consistent shape. Most items are content you've collected from elsewhere or written yourself. A few may be dynamic, living resources that update themselves (see [scout](#scout-available-now--the-exception-not-the-rule)). The collection's job is to hold them, organize them, and make them browseable — with or without an agent-librarian's help.

See [ASPIRATIONS.md](ASPIRATIONS.md) for the full vision, collection invariants, and where this project is headed. If you're new to working in a terminal, see the [detailed setup walkthrough](#detailed-setup-walkthrough) at the end of this page and the [terminal basics guide](docs/guides/terminal-basics.md).

## Who is this for?

Anyone who wants to organize a private collection independently — to own the result rather than depend on an external platform, and to have the ability to use the collection without any special or proprietary software. Content can be viewed in any browser, in a simple format. No technical background required, though technical users are equally welcome.

### An optional side benefit: technical upskilling

For users who want it, alexandria doubles as a low-friction path to a disproportionately useful skill set: knowing how to direct AI tools effectively without needing to become a programmer. Building real things you actually need — opening a terminal, reading structured data, running scripts, understanding what "you own this data" means technically — teaches you what matters and what doesn't. The skills transfer well beyond this tool. See [ASPIRATIONS.md](ASPIRATIONS.md) for more on the technical minimalism philosophy.

If that's not your goal, clear instructions are provided for building and extending your collection. After that, exploring it as as easy as using Wikipedia.

## Item types

All item types share a universal outer shape: a README (the spine), metadata (the catalog entry), and content. Each type has its own creation process within that shape.

### Physical

A record of a physical item you own. No content is copied — the item lives on your shelf; the catalog entry represents it in your collection. Creation is photo-based: photograph a single item or a whole shelf, and alexandria extracts title, author, and other metadata from the image (with your confirmation). Manual entry works too, with or without a photo. Optional online metadata and summaries are available for users who want them. Run `/coll-physical` or `/coll` → add an item → physical.

Existing cataloging tools (LibraryThing, Libib, CLZ Books) handle barcode scanning and standard metadata well. Alexandria differentiates on shelf photo accuracy (using stronger vision models than existing apps), local-first ownership (files on your machine, not in someone's cloud), no subscription, and integration with other item types in a single collection. Leading with physical signals what alexandria values: a book on your shelf is as first-class as a PDF on your drive.

### Digital

Digital content you want to bring into the collection — local files (PDFs, HTML, markdown, text, images, audio, video), URLs to fetch and archive, or pasted text. The collection copies the content, preserves the original exactly, and extracts metadata so you can find it later. Run `/coll-digital` or `/coll` → add an item → digital.

### Scout

A living knowledge base that monitors a domain. Unlike import and author, a scout is actively maintained by AI — researched, organized, systematically critiqued, and kept current through automated discovery. Scouts are powerful but are the exception rather than the rule: most library holdings should be static, like most of a real library's holdings.

A scout can be **short-lived** (built for an immediate need, updated briefly, then settled into a static reference) or **long-lived** (kept updating indefinitely for an evolving domain). You decide when to settle a scout — to freeze it as a static item in your collection.

Scout is useful when a topic is complex enough to warrant careful organization, personal enough that no generic tool quite fits, and evolving fast enough that a static resource goes stale. For example: navigating a complex medical situation, monitoring a professional field, or tracking fast-moving developments.

## Getting started

### What you need

- **[Claude Code](https://claude.ai/claude-code)** — the AI assistant that creates items and manages the collection. Included with a [Claude Pro subscription](https://claude.com/pricing) ($20/month). Runs in your terminal, [in a browser](https://claude.ai/code), or via the phone app ([iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684), [Android](https://play.google.com/store/apps/details?id=com.anthropic-claude)). Browser and phone require a GitHub-hosted library.
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

### Add an item

From `/coll`, choose "add an item" and describe what you need:

- "I have a physical item I want to catalog" — runs /coll-physical
- "I want to photograph my bookshelf and catalog the books" — runs /coll-physical with the shelf workflow
- "I want to add these PDFs (or URLs, or notes) to my library" — runs /coll-digital
- "I need to understand treatment options for [condition]" — runs /coll-new-scout
- "I want to track developments in [field]" — runs /coll-new-scout

Claude Code determines the appropriate item type and guides you through building it. Physical and scout item types are available now; import and author are planned.

### Day-to-day use

- **Browse**: open `~/alexandria/wiki/index.html` in any browser — the wiki view gives you a familiar, navigable interface with multi-axis indexes (by section, date, type, form, media type). Works fully offline. No terminal needed for daily browsing.
- **Add more items**: `/coll` → add an item (the wiki regenerates automatically after each addition)
- **Update an item**: `cd` into it and work with Claude Code directly
- **Reorganize**: `/coll` → reorganize when the structure needs adjusting
- **Remove an item**: `/coll` → remove-item (keeps the catalog entry marked as removed) or `delete-item` (removes the entry entirely)
- **Regenerate the wiki manually**: `/coll-menu` → regenerate-wiki (or from the collection directory: `uv run python tools/generate_wiki.py .`)

## What uses Claude Code and what doesn't

**Requires Claude Code** (internet + Anthropic account): Creating a new collection, adding items, and creating scouts (the scout process involves research, schema design, editorial writing, systematic critique, and script generation). During these tasks, your prompts and responses pass through Anthropic's servers. Your data files — YAML, markdown, scripts — remain on your machine and are not uploaded.

**Works fully offline, no AI or subscription needed:** Reading and browsing your collection, navigating via HTML links, regenerating READMEs, editing entries, running discovery scripts. Once built, the files are entirely yours and work independently of any service.

**No local model alternative currently exists for creating scouts.** The scout's seven-phase process — particularly research, critique, and editorial writing — depends on Claude's capabilities. The skills are plain markdown instructions; if a local-model agent runner with comparable quality becomes available, they will work without modification.

**Long-term direction**: the default librarian will be a local, open-source model. Library-level tasks (browsing, cataloging, search, cross-item questions) don't require Claude's capabilities and shouldn't depend on a subscription. Claude will remain the default only for scout creation and maintenance, where the quality gap meaningfully matters. Users who never build scouts will eventually be able to use alexandria with only a local model.

## What's in this repo

### Skills

- [/coll-build-new-collection](.claude/skills/coll-build-new-collection/SKILL.md) — create a new collection (run once from the alexandria repo)
- [/coll-menu](.claude/skills/coll-menu/SKILL.md) — guided menu for all collection actions
- [/coll-physical](.claude/skills/coll-physical/SKILL.md) — catalog a physical item from a photo or manual entry
- [/coll-hardcover](.claude/skills/coll-hardcover/SKILL.md) — shortcut for a hardcover (calls /coll-physical with media_type pre-set)
- [/coll-paperback](.claude/skills/coll-paperback/SKILL.md) — shortcut for a paperback
- [/coll-digital](.claude/skills/coll-digital/SKILL.md) — bring digital content (files, URLs, text) into the collection
- [/coll-new-scout](.claude/skills/coll-new-scout/SKILL.md) — create a new scout for any topic
- [/coll-scout](.claude/skills/coll-scout/SKILL.md) — import an existing scout into the collection
- [/coll-notes](.claude/skills/coll-notes/SKILL.md) — save notes about an item or the collection
- [/coll-add-item-notes](.claude/skills/coll-add-item-notes/SKILL.md) — add personal notes to an item (from a .md, .txt, or .pdf file)
- [/coll-update-from-latest-alexandria](.claude/skills/coll-update-from-latest-alexandria/SKILL.md) — update skills to the latest version from the alexandria repo

### Guides

- [Terminal basics](docs/guides/terminal-basics.md) — directories, git repos, Claude Code sessions, running multiple sessions with tabs
- [Python and uv](docs/guides/python-and-uv.md) — what Python, dependencies, uv, and git are (one paragraph each) and why you need them
- [YAML basics](docs/guides/yaml-basics.md) — reading and editing metadata.yaml files
- [Anatomy of an item](docs/guides/anatomy-of-an-item.md) — what's inside an item directory, what each file does, what you can safely change
- [Working with scouts](docs/guides/working-with-scouts.md) — the scout lifecycle: creating, maintaining, settling, importing
- [Troubleshooting](docs/guides/troubleshooting.md) — common issues and how to fix them

### Reference docs

- [docs/collection/](docs/collection/) — collection-level specs (universal item shape)
- [docs/scout/](docs/scout/) — scout process phases, critique checklist, schema patterns, walkthroughs

### Project direction

- [ASPIRATIONS.md](ASPIRATIONS.md) — project vision, collection architecture, technical minimalism, planned item types
- [TODO.md](TODO.md) — planned additions and improvements

---

## Detailed setup walkthrough

Step-by-step instructions assuming no prior terminal experience. Every command is shown exactly as you'll type it.

Alexandria needs a few tools installed on your machine. For background on what each tool is and why it's needed, see the [Python and uv guide](docs/guides/python-and-uv.md). For help with the terminal itself, see the [terminal basics guide](docs/guides/terminal-basics.md).

### 1. Open a terminal

A terminal is a text window where you type commands. See the [terminal basics guide](docs/guides/terminal-basics.md) for more detail.

- **macOS**: Press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows**: You'll need WSL (Windows Subsystem for Linux), which lets you run Linux commands on Windows. Install "Ubuntu" from the Microsoft Store, then open it from the Start menu. This gives you a terminal.
- **Linux**: Open your Terminal or Konsole application.

### 2. Check that Python is installed

Python is the programming language alexandria's tools are written in. You don't need to write Python — you just need it installed so the tools can run.

```
python3 --version
```

You should see something like `Python 3.13.2`. If you see "command not found," install Python from [python.org/downloads](https://python.org/downloads) — download the installer for your system, run it, then try the command again.

### 3. Check that Git is installed

Git is a tool for downloading and tracking changes to projects. You need it to download alexandria.

```
git --version
```

You should see something like `git version 2.43.0`. If you see "command not found":

- **macOS**: type `xcode-select --install` and follow the prompts
- **Windows (WSL/Ubuntu)**: type `sudo apt install git` (it will ask for your password)
- **Linux**: type `sudo apt install git` (Ubuntu/Debian) or `sudo dnf install git` (Fedora)

### 4. Install Claude Code

Claude Code is the AI assistant that reads alexandria's skills and helps you build and manage your collection. You'll need an Anthropic account (free to create; Claude Code is included with a [Claude Pro subscription](https://claude.com/pricing) at $20/month).

Go to [claude.ai/claude-code](https://claude.ai/claude-code) and follow their installation instructions.

Verify it's installed by typing: `claude --version`

### 5. Download alexandria

This command downloads the alexandria project to your computer:

```
cd ~
git clone https://github.com/msyvr/alexandria.git
```

The first line (`cd ~`) goes to your home directory. The second line downloads alexandria into a folder called `alexandria`. You'll see progress messages — wait until you're back at the prompt.

### 6. Install uv and alexandria's dependencies

Alexandria's tools depend on a few shared Python packages (for reading YAML files, converting markdown to HTML, extracting PDF metadata, and so on). [uv](https://docs.astral.sh/uv/) is the tool that installs and manages these. See the [Python and uv guide](docs/guides/python-and-uv.md) for more about what these are.

Install uv (one-time — paste this line and press Enter):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install alexandria's dependencies:

```
cd ~/alexandria
uv sync
```

This reads the list of what alexandria needs and installs it. You'll see output showing what was installed. After this, everything is ready.

### 7. Create your collection

You should still be in the alexandria directory from the previous step. Start Claude Code:

```
claude
```

You'll see a prompt that looks like `❯`. This is where you type messages to Claude. Claude has already read the project's instructions — it knows about your collection skills, but it won't say anything until you type first.

Type:

```
/coll-build-new-collection
```

Name your collection and choose where to create it. Claude will then create the collection's files. You'll see prompts asking for permission to create files and directories — for example:

```
Create file
  .collection-index.yaml

Do you want to create .collection-index.yaml?
> 1. Yes
  2. Yes, allow all edits in my-collection/ during this session
  3. No
```

Say **Yes** (or choose option 2 to allow all edits in the collection without being asked for each one — recommended if you don't want to approve every file individually). These are the collection's catalog and skill files being set up. The skill copies the collection skills into your new collection's `.claude/skills/` directory.

### 8. Switch to your collection

Open a new terminal (or a new tab with `Cmd+T` on macOS) and start Claude Code from your collection directory:

```
cd ~/my-collection
claude
```

You're now working from your collection. Type `/coll-` and hit tab to see all available commands, or type `/coll-menu` for a guided menu. You can keep the alexandria session open for reference, or close it when you're comfortable (`/exit` or `Ctrl+C`).

### 9. Add your first item (from your collection directory)

From the `/coll` prompt, choose "add an item" and describe what you need. A few examples:

- **Physical item**: "I have a physical item I want to catalog" — you'll be asked for a photo (single item or shelf) or to enter the metadata by hand
- **Digital content**: "I want to add these files" or "save this URL" — files are copied, URLs are fetched and archived, metadata is extracted (also use this for your own writing — markdown notes, drafts, anything you've created)
- **Scout**: "I need to understand treatment options for [condition]" or "I want to track developments in [field]" — Claude Code builds a structured knowledge base through a seven-phase process

Claude Code guides you from there, asking the questions relevant to the item type you chose. You provide the direction; it handles the construction.

### 10. Browse your collection

In Claude Code: `/coll` → browse

In a browser:

- **macOS**: `open ~/alexandria/index.html`
- **Windows (WSL)**: `explorer.exe $(wslpath -w ~/alexandria/index.html)`
- **Linux**: `xdg-open ~/alexandria/index.html`

### 11. Add more items

In Claude Code: `/coll` → add an item. Same process as step 9.

### Troubleshooting

**"command not found"**: The tool isn't installed. Return to the relevant step above.

**"permission denied"**: Try `sudo` before the command (e.g., `sudo cp -r ...`).

**`/coll` not recognized**: Re-run step 7. Ensure `~/.claude/skills/` exists.

**Other issues**: Start Claude Code and describe the problem — it can often diagnose and fix things directly.
