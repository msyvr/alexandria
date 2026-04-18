## alexandria

Alexandria is a way of building and keeping a private library — books, papers, notes, research, whatever else you would like to have organized — in a form you own and can use without any particular app or service.

The motivation is practical. As AI takes on more of the work of making, editing, and organizing digital material, retaining control of one's own work has begun to depend on a small, practical fluency. Not programming — a narrower set: enough terminal to navigate and recover, enough structured text to read a YAML file, enough command of an AI assistant to direct and correct its work, enough sense of what a file is to know when you own it. People who have that fluency can remain in control as AI advances. People who do not are increasingly renting the capability from whoever made the nearest app.

Alexandria is for people who would like that fluency but have not yet built it. The collection is the vehicle. Each skill comes up in the course of the work, when there is something concrete to apply it to.

![Example alexandria collection landing page](docs/images/wiki-landing-example.png)

The collection itself borrows from the real-world library: a curated set of items that live in predictable places, findable by catalog or by walking the stacks, with or without a librarian's help. It is a directory on your machine. Inside it, items have a consistent shape — a catalog entry, content files, and a README. Most items are static; a few ("scouts") are AI-curated and evolving, and can be settled into static references when they are done. The finished collection is entirely yours, and works whether or not any AI is running.

See [ASPIRATIONS.md](docs/ASPIRATIONS.md) for the full thesis and where the project is headed. If you are new to working in a terminal, the [detailed setup walkthrough](#detailed-setup-walkthrough) at the end of this page shows every step, and the [terminal basics guide](docs/guides/terminal-basics.md) covers the fundamentals.

### Quick start

If you're comfortable in the terminal, [jump in](#create-your-collection). If you're new to the terminal, start with the [detailed walkthrough](#detailed-setup-walkthrough) — it shows every step. You'll work in two windows: this page (for reference) and a terminal (where you type commands).

### Who this is for

People who would like a working fluency with their own digital material in the presence of AI, and are open to developing it as they go. No prior technical background is expected — the process introduces what is needed when it is needed. Software engineers who would rather not build the scaffolding from scratch are equally welcome.

### What the process touches

The skills that come up, in roughly the order they appear:

- Working in a terminal — enough to navigate, start tools, and recover from small mistakes.
- Reading structured data — YAML and markdown with frontmatter, as a shape rather than as a language.
- Directing an AI assistant — prompting, reviewing, pushing back, verifying.
- File ownership in practice — what a local file is, what a format is, whether the data is yours.
- Version control as insurance — git, used lightly, against mistakes on files you care about.

The set is small by design, and chosen for leverage rather than breadth. Someone who can direct AI and verify the result can accomplish a great deal without learning to program. The intention is not to teach software engineering; it is to mark out the fluency that lets a person retain control of their own work.

### Item types

All item types share a universal outer shape: a README (the spine), metadata (the catalog entry), and content. Each type has its own creation process within that shape.

#### Physical

A record of a physical item you own. No content is copied — the item lives on your shelf; the catalog entry represents it in your collection. Creation is photo-based: photograph a single item or a whole shelf, and alexandria extracts title, author, and other metadata from the image, which you confirm. Manual entry works too, with or without a photo. Optional online metadata and summaries are available for users who want them. Run `/coll-physical` or `/coll` → add an item → physical.

Physical items are the simplest case of the collection's shape: something you own in the world is given a catalog entry that lives with you, built from a photo or entered by hand. A book on your shelf is treated on equal footing with a PDF on your drive.

#### Digital

Digital content you want to bring into the collection — local files (PDFs, HTML, markdown, text, images, audio, video), URLs to fetch and archive, or pasted text. The collection copies the content, preserves the original exactly, and extracts metadata so you can find it later. Run `/coll-digital` or `/coll` → add an item → digital.

#### Scout

A knowledge base on a topic, actively maintained by AI — researched, organized, critiqued, and kept current through discovery scripts. A scout is the fullest expression of what this collection makes possible: a resource on a subject you care about, built and owned by you, rather than a subscription to a generic version of it.

A scout can be **short-lived** (built for an immediate need, updated briefly, then settled into a static reference) or **long-lived** (kept updating indefinitely for an evolving domain). You decide when to settle a scout — to freeze it as a static item in your collection. Most items in a mature collection are static, as most holdings in a real library are; scouts are the ones that keep moving until you decide otherwise.

Scout is useful when a topic is complex enough to warrant careful organization, personal enough that no generic tool quite fits, and evolving fast enough that a static resource goes stale. For example: navigating a complex medical situation, monitoring a professional field, or tracking fast-moving developments.

### Getting started

#### What you need

- **[Claude Code](https://claude.ai/claude-code)** — the AI assistant that creates items and manages the collection. Included with a [Claude Pro subscription](https://claude.com/pricing) ($20/month). Runs in your terminal, [in a browser](https://claude.ai/code), or via the phone app ([iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684), [Android](https://play.google.com/store/apps/details?id=com.anthropic-claude)). Browser and phone require a GitHub-hosted library.
- **Python 3.10+** — for scripts within built scouts. Check with `python3 --version`.
- No prior technical background is expected. You direct the process by answering questions and reviewing output; Claude Code writes the scripts and data files. See [ASPIRATIONS.md](docs/ASPIRATIONS.md) for the thesis and the fluency developed along the way.

#### Create your collection

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

#### Add an item

From `/coll`, choose "add an item" and describe what you need:

- "I have a physical item I want to catalog" — runs /coll-physical
- "I want to photograph my bookshelf and catalog the books" — runs /coll-physical with the shelf workflow
- "I want to add these PDFs (or URLs, or notes) to my library" — runs /coll-digital
- "I need to understand treatment options for [condition]" — runs /coll-new-scout
- "I want to track developments in [field]" — runs /coll-new-scout

Claude Code determines the appropriate item type and guides you through building it. Physical and scout item types are available now; import and author are planned.

#### Day-to-day use

- **Browse**: open `~/alexandria/wiki/index.html` in any browser — the wiki view gives you a familiar, navigable interface with indexes across the full collection (All), By section, By author/artist, By medium & format, and Let the LLM decide (placeholder for a narrative layer). Works fully offline, and the fonts ship with the collection (no CDN lookups), so the rendering is identical on any machine. See the [fonts and typography guide](docs/guides/fonts-and-typography.md) for how to swap them.
- **Add more items**: `/coll` → add an item (the wiki regenerates automatically after each addition)
- **Update an item**: `cd` into it and work with Claude Code directly
- **Reorganize**: `/coll` → reorganize when the structure needs adjusting
- **Remove an item**: `/coll` → remove-item (keeps the catalog entry marked as removed) or `delete-item` (removes the entry entirely)
- **Regenerate the wiki manually**: `/coll-menu` → regenerate-wiki (or from the collection directory: `uv run python tools/generate_wiki.py .`)

### What uses Claude Code and what doesn't

**Requires Claude Code** (internet + Anthropic account): Creating a new collection, adding items, and creating scouts (the scout process involves research, schema design, editorial writing, systematic critique, and script generation). During these tasks, your prompts and responses pass through Anthropic's servers. Your data files — YAML, markdown, scripts — remain on your machine and are not uploaded.

**Works fully offline, no AI or subscription needed:** Reading and browsing your collection, navigating via HTML links, regenerating READMEs, editing entries, running discovery scripts. Once built, the files are entirely yours and work independently of any service.

**No local model alternative currently exists for creating scouts.** The scout's seven-phase process — particularly research, critique, and editorial writing — depends on Claude's capabilities. The skills are plain markdown instructions; if a local-model agent runner with comparable quality becomes available, they will work without modification.

**Long-term direction**: the default librarian will be a local, open-source model. Library-level tasks (browsing, cataloging, search, cross-item questions) don't require Claude's capabilities and shouldn't depend on a subscription. Claude will remain the default only for scout creation and maintenance, where the quality gap meaningfully matters. Users who never build scouts will eventually be able to use alexandria with only a local model.

### What's in this repo

#### Skills

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
- [/coll-rename](.claude/skills/coll-rename/SKILL.md) — rename the collection (display name and optionally directory)
- [/coll-import-collection](.claude/skills/coll-import-collection/SKILL.md) — import all items from another collection into this one
- [/coll-update-from-latest-alexandria](.claude/skills/coll-update-from-latest-alexandria/SKILL.md) — update skills to the latest version from the alexandria repo

#### Guides

- [Terminal basics](docs/guides/terminal-basics.md) — directories, git repos, Claude Code sessions, running multiple sessions with tabs
- [Python and uv](docs/guides/python-and-uv.md) — what Python, dependencies, uv, and git are (one paragraph each) and why you need them
- [YAML basics](docs/guides/yaml-basics.md) — reading and editing metadata.yaml files
- [Anatomy of an item](docs/guides/anatomy-of-an-item.md) — what's inside an item directory, what each file does, what you can safely change
- [Working with scouts](docs/guides/working-with-scouts.md) — the scout lifecycle: creating, maintaining, settling, importing
- [Fonts and typography](docs/guides/fonts-and-typography.md) — which fonts ship with the wiki, why they're self-hosted, how to swap them
- [Troubleshooting](docs/guides/troubleshooting.md) — common issues and how to fix them

#### Reference docs

- [docs/collection/](docs/collection/) — collection-level specs (universal item shape)
- [docs/scout/](docs/scout/) — scout process phases, critique checklist, schema patterns, walkthroughs

#### Project direction

- [ASPIRATIONS.md](docs/ASPIRATIONS.md) — project vision, collection architecture, technical minimalism, planned item types

---

### Detailed setup walkthrough

Step-by-step instructions for readers without prior terminal experience. Every command is shown exactly as you would type it. The setup is also the first occasion to use most of the skills described above; that is intentional.

Alexandria needs a few tools installed on your machine. For background on what each tool is and why it is needed, see the [Python and uv guide](docs/guides/python-and-uv.md). For the terminal itself, see the [terminal basics guide](docs/guides/terminal-basics.md).

#### 1. Open a terminal

A terminal is a text window where you type commands. See the [terminal basics guide](docs/guides/terminal-basics.md) for more detail.

- **macOS**: Press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows**: You'll need WSL (Windows Subsystem for Linux), which lets you run Linux commands on Windows. Install "Ubuntu" from the Microsoft Store, then open it from the Start menu. This gives you a terminal.
- **Linux**: Open your Terminal or Konsole application.

#### 2. Check that Python is installed

Python is the programming language alexandria's tools are written in. You don't need to write Python — you just need it installed so the tools can run.

```
python3 --version
```

You should see something like `Python 3.13.2`. If you see "command not found," install Python from [python.org/downloads](https://python.org/downloads) — download the installer for your system, run it, then try the command again.

#### 3. Check that Git is installed

Git is a tool for downloading and tracking changes to projects. You need it to download alexandria.

```
git --version
```

You should see something like `git version 2.43.0`. If you see "command not found":

- **macOS**: type `xcode-select --install` and follow the prompts
- **Windows (WSL/Ubuntu)**: type `sudo apt install git` (it will ask for your password)
- **Linux**: type `sudo apt install git` (Ubuntu/Debian) or `sudo dnf install git` (Fedora)

#### 4. Install Claude Code

Claude Code is the AI assistant that reads alexandria's skills and helps you build and manage your collection. You'll need an Anthropic account (free to create; Claude Code is included with a [Claude Pro subscription](https://claude.com/pricing) at $20/month).

Go to [claude.ai/claude-code](https://claude.ai/claude-code) and follow their installation instructions.

Verify it's installed by typing: `claude --version`

#### 5. Download alexandria

This command downloads the alexandria project to your computer:

```
cd ~
git clone https://github.com/msyvr/alexandria.git
```

The first line (`cd ~`) goes to your home directory. The second line downloads alexandria into a folder called `alexandria`. You'll see progress messages — wait until you're back at the prompt.

#### 6. Install uv and alexandria's dependencies

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

#### 7. Create your collection

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

#### 8. Switch to your collection

Open a new terminal (or a new tab with `Cmd+T` on macOS) and start Claude Code from your collection directory:

```
cd ~/my-collection
claude
```

You're now working from your collection. Type `/coll-` and hit tab to see all available commands, or type `/coll-menu` for a guided menu. You can keep the alexandria session open for reference, or close it when you're comfortable (`/exit` or `Ctrl+C`).

#### 9. Add your first item (from your collection directory)

From the `/coll` prompt, choose "add an item" and describe what you need. A few examples:

- **Physical item**: "I have a physical item I want to catalog" — you'll be asked for a photo (single item or shelf) or to enter the metadata by hand
- **Digital content**: "I want to add these files" or "save this URL" — files are copied, URLs are fetched and archived, metadata is extracted (also use this for your own writing — markdown notes, drafts, anything you've created)
- **Scout**: "I need to understand treatment options for [condition]" or "I want to track developments in [field]" — Claude Code builds a structured knowledge base through a seven-phase process

Claude Code guides you from there, asking the questions relevant to the item type you chose. You provide the direction; it handles the construction.

#### 10. Browse your collection

In Claude Code: `/coll` → browse

In a browser:

- **macOS**: `open ~/alexandria/index.html`
- **Windows (WSL)**: `explorer.exe $(wslpath -w ~/alexandria/index.html)`
- **Linux**: `xdg-open ~/alexandria/index.html`

#### 11. Add more items

In Claude Code: `/coll` → add an item. Same process as step 9.

#### Troubleshooting

**"command not found"**: The tool isn't installed. Return to the relevant step above.

**"permission denied"**: Try `sudo` before the command (e.g., `sudo cp -r ...`).

**`/coll` not recognized**: Re-run step 7. Ensure `~/.claude/skills/` exists.

**Other issues**: Start Claude Code and describe the problem — it can often diagnose and fix things directly.
