# alexandria

Build and organize a personal curated library — a collection of living resources on topics that matter to you.

alexandria is a set of Claude Code skills for creating, organizing, and maintaining a personal library of structured "books." Each book is a self-contained project you own and understand. The library provides a lightweight organizational layer so you can find things as the collection grows.

See [ASPIRATIONS.md](ASPIRATIONS.md) for where this project is headed. If you're new to working in a terminal, see the [detailed setup walkthrough](#detailed-setup-walkthrough) at the end of this page.

## Who is this for?

**You need to get smart on a complex topic fast — and you want a resource you own and control, not someone else's app.**

You don't need to be a software engineer. You don't need to be technical at all. But if you are, you still don't want to build the scaffolding from scratch — you want the structured result and the ongoing discovery.

**High-stakes personal decisions** — consequential, ongoing, too specific for any app:
- Navigating a complex medical situation: treatment options, evolving evidence, specialist landscape
- Planning an international relocation: visa pathways, cost of living, schools, healthcare systems, tax implications — across multiple candidate countries

**Professional domain mastery** — entering or deepening in a technical field, or bespoke monitoring of a niche one:
- A biologist tracking single-cell sequencing methods and when to use each
- An economist monitoring causal inference techniques and their applicability to policy evaluation
- Whatever your field, the pattern is the same: map the landscape, stay current, make better decisions

**Monitoring fast-moving, high-consequence developments** — information arriving faster than you can process it, much of it unreliable:
- Tracking an emerging infectious disease: transmission data, treatment protocols, public health guidance, local outbreak patterns
- Following rapidly evolving regulation across jurisdictions that directly affects your work or life

In each case: **the stakes justify the effort, the need is yours specifically, and the landscape won't hold still.**

## What you get

A library on your computer — a directory containing books organized by your needs:

```
~/alexandria/
├── health/
│   ├── condition-treatments/        ← a tracker book (its own project)
│   └── outbreak-monitoring/         ← another tracker book
└── professional/
    └── inference-methods/           ← tracker book
```

Each book is a self-contained project with structured data, a generated overview, editorial guides, and automated discovery. You own all of it — it's files on your machine.

The library itself is a lightweight layer: an index, sections, and a table of contents. As it grows, the `/library` skill helps you reorganize — proposing groupings, subdividing sections that get too large.

## Book types

### Tracker (available now)
A curated, structured knowledge base on a domain. Researched, organized, systematically critiqued, and kept current with automated discovery of new developments. Built through a seven-phase process that catches category errors, brand bias, and missing risk callouts.

### Import (coming soon)
Curated collection of external content — papers, articles, books. Organized, annotated, cross-referenced.

### Author (coming soon)
Your own creative and professional output — notes, projects, task lists. Structured, searchable, maintained.

## What you need

### Required
- **[Claude Code](https://claude.ai/claude-code)** — the AI assistant that powers the book-building process. Included with a [Claude Pro subscription](https://claude.com/pricing) ($20/month). Claude Code runs in your terminal or [in a browser](https://claude.ai/code) — see below for options. See "What uses Claude Code and what doesn't" for details on data and privacy.
- **Python 3.10+** — for the scripts within built tracker books. Check with `python3 --version`.

### How to run Claude Code

**Option A: Terminal (recommended).** Claude Code runs in your terminal. On macOS, open Terminal. On Windows, use WSL. This is the most capable option — full access to your local filesystem, no GitHub required.

**Option B: Browser.** Claude Code runs at [claude.ai/code](https://claude.ai/code) — no terminal needed. Connect your GitHub account to give it access to your repos. Your library must be in a GitHub repo for this option. Good if you prefer not to install anything locally.

**Option C: Phone.** The Claude app ([iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684), [Android](https://play.google.com/store/apps/details?id=com.anthropic-claude)) can start builds and monitor progress on a GitHub-hosted library. Useful for kicking off a new book or checking discovery results on the go — detailed work is better on a desktop or in the browser.

### Optional
- **A GitHub account** — for automated discovery in tracker books. Not required; everything works offline.
- **Git** — recommended for version control of individual books.

### No coding experience required
You don't need to know how to code. Claude Code generates everything. You guide the process by answering questions about what you care about. You will use the terminal to run a few commands — the process walks you through exactly what to type.

If you're new to working in a terminal, that's fine. The skills you pick up here — running commands, reading structured data, using version control — are useful far beyond this tool. See [ASPIRATIONS.md](ASPIRATIONS.md) for more on this.

### What uses Claude Code and what doesn't

**Requires Claude Code** (internet connection + Anthropic account):
- Building a tracker book — the seven-phase process includes research, schema design, editorial writing, systematic critique, and script generation. These are the heavy tasks that depend on Claude's capabilities.
- Creating a library and adding a book to it — Claude Code understands your intent ("I need to track treatments for X") and handles the conversational setup. This is lightweight compared to the build itself.

During these tasks, your prompts and the AI's responses pass through Anthropic's servers. Your data files — the YAML, markdown, and scripts that make up your books — stay on your machine and are not uploaded.

**Works fully offline, no AI, no subscription needed:**
- Reading and browsing your library (open `index.html` in any browser, or read the markdown files directly)
- Navigating between books and sections via HTML links
- Regenerating a book's README (`python scripts/generate_readme.py`)
- Manually editing entries in `data/entries.yaml`
- Running discovery scripts (`python scripts/discover.py` — calls public APIs, not AI)

Once your library is built, you can cancel your subscription and keep using it indefinitely. The files are yours. AI is needed only when you want to build new books or run the critique process.

**No local model alternative currently exists for building tracker books.** The tracker's seven-phase process — particularly research (gathering and synthesizing landscape data), critique (systematic error detection across categories, bias, and risk callouts), and editorial writing (getting-started guides, decision trees) — depends on Claude's capabilities. The skills are written as markdown instructions that any sufficiently capable AI agent could follow; if a local-model agent runner with comparable quality emerges, the skills will work with it without changes. Discovery scripts will support configurable model endpoints in the future for tasks like relevance scoring.

## How to use it

### Install the skills

1. Install Claude Code: see [claude.ai/claude-code](https://claude.ai/claude-code)
2. Install the alexandria skills (one-time):
   ```
   git clone https://github.com/msyvr/alexandria.git
   cp -r alexandria/skills/* ~/.claude/skills/
   ```

That's it. The `/library` and `/build-tracker` commands are now available in any Claude Code session.

### Create your library

1. Open a terminal and start Claude Code:
   ```
   claude
   ```
2. Type `/library`
3. Name your library (or accept the default: "alexandria")
4. Tell it what you need: "I need to understand the treatment landscape for [condition]" or "I want to track developments in [field]"
5. The skill determines the right book type, creates it in your library, and guides you through building it

### After it's built

- **Browse your library**: Run `/library` → browse to see your table of contents
- **Add more books**: Run `/library` → add a book
- **Update a book**: `cd` into it and work with Claude Code directly
- **Reorganize**: Run `/library` → reorganize when the structure needs adjusting

## What's in this repo

### Skills
- [/library](skills/library/SKILL.md) — create and manage your library (the main entry point)
- [/build-tracker](skills/build-tracker/SKILL.md) — build a landscape tracker book (also available directly)

### Reference docs (tracker book type)
Detailed process docs, prompt templates, conventions, and examples that informed the build-tracker skill:
- [docs/tracker/](docs/tracker/) — process phases, critique checklist, schema patterns, walkthroughs

### Project direction
- [ASPIRATIONS.md](ASPIRATIONS.md) — project vision, the technical minimalism goal, planned book types
- [TODO.md](TODO.md) — planned additions and improvements

---

## Detailed setup walkthrough

Step-by-step instructions for getting started, assuming no prior terminal experience. Every command is shown exactly as you'll type it.

### 1. Open a terminal

- **macOS**: Press `Cmd + Space`, type `Terminal`, press Enter. A window with a text prompt appears — this is your terminal.
- **Windows**: You'll need WSL (Windows Subsystem for Linux). Search for "WSL" in the Microsoft Store, install Ubuntu, then open it from the Start menu.
- **Linux**: Open your system's terminal application (usually called Terminal or Konsole).

### 2. Check that Python is installed

Type this in your terminal and press Enter:
```
python3 --version
```

You should see something like `Python 3.13.2`. If you see "command not found," install Python from [python.org/downloads](https://python.org/downloads) — download the installer, run it, then try the command again.

### 3. Check that Git is installed

Type this and press Enter:
```
git --version
```

You should see something like `git version 2.43.0`. If you see "command not found":
- **macOS**: Type `xcode-select --install` and follow the prompts
- **Windows (WSL)**: Type `sudo apt install git`
- **Linux**: Type `sudo apt install git` (Ubuntu/Debian) or `sudo dnf install git` (Fedora)

### 4. Install Claude Code

Go to [claude.ai/claude-code](https://claude.ai/claude-code) and follow the installation instructions. You'll need to create an Anthropic account if you don't have one.

Once installed, verify it works by typing:
```
claude --version
```

### 5. Download alexandria

Type these two commands, pressing Enter after each:
```
cd ~
```
```
git clone https://github.com/msyvr/alexandria.git
```

The first command takes you to your home directory. The second downloads the alexandria project. You'll see progress messages — wait until you're back at the prompt.

### 6. Install the skills

Type this command:
```
cp -r ~/alexandria/skills/* ~/.claude/skills/
```

This copies the skill files to where Claude Code can find them. You won't see any output — that's normal. It means it worked.

### 7. Create your library

Start Claude Code:
```
claude
```

You'll see a prompt where you can type messages to Claude Code. Type:
```
/library
```

Claude Code will ask you what to name your library (you can just press Enter to accept "alexandria") and where to put it. Then tell it what you want to build:

- "I need to understand treatment options for [condition]"
- "I want to track developments in [field]"
- "I need to monitor [topic] and stay current on new developments"

Claude Code will guide you through the rest — asking questions about what to cover, who it's for, and how you'd want to compare entries. Your job is to answer those questions. It handles the building.

### 8. Browse your library

Once you've built your first book, you can browse your library anytime:

1. Start Claude Code: `claude`
2. Type `/library`
3. Choose "browse"

To view your library in a browser, open this file (replace `alexandria` with your library name if you chose a different one):
- **macOS**: `open ~/alexandria/index.html`
- **Windows (WSL)**: `explorer.exe $(wslpath -w ~/alexandria/index.html)`
- **Linux**: `xdg-open ~/alexandria/index.html`

### 9. Add more books

Start Claude Code, type `/library`, and choose "add a book." Same process as step 7 — describe what you need, and it guides you through building it.

### Troubleshooting

**"command not found" for any command**: The tool isn't installed. Go back to the relevant installation step.

**"permission denied"**: On macOS/Linux, try adding `sudo` before the command (e.g., `sudo cp -r ...`). You'll be asked for your computer's password.

**Claude Code doesn't recognize `/library`**: The skills weren't copied correctly. Re-run step 6. Make sure the `~/.claude/skills/` directory exists — if not, create it first with `mkdir -p ~/.claude/skills/`.

**Something else went wrong**: Start Claude Code (`claude`) and describe the problem. It can often diagnose and fix issues directly.
