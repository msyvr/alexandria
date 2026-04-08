# alexandria

A personal curated library — organized, browsable, and entirely yours.

Alexandria helps you create and manage a library of "books" on topics that matter to you. The library is a directory on your machine with a lightweight organizational layer: sections, an index, and a table of contents. Each book is a self-contained project inside it. You can browse the library in a browser, in a markdown viewer, or through Claude Code.

Books come in different types. The first available type is the **scout** — a living knowledge base that monitors a domain for new developments. Other types (importing external content, organizing your own writing) are planned.

See [ASPIRATIONS.md](ASPIRATIONS.md) for where this project is headed. If you're new to working in a terminal, see the [detailed setup walkthrough](#detailed-setup-walkthrough) at the end of this page.

## Who is this for?

Anyone who would benefit from an organized, personal collection of structured resources — and wants to own the result rather than depend on someone else's platform. No technical background required, though technical users are equally welcome.

## Book types

### Scout (available now)
A curated, living knowledge base that monitors a domain. Created through a seven-phase process with built-in self-critique that catches categorization errors, brand-recognition bias, and missing risk callouts. Once built, automated discovery keeps it current with new developments.

Scouts are most useful when a topic is complex enough to warrant careful organization, personal enough that no generic tool quite fits, and evolving fast enough that a static resource goes stale. For example:
- Navigating a complex medical situation: treatment options, evolving evidence, specialist landscape
- Entering or monitoring a professional field: a biologist tracking sequencing methods, an economist monitoring causal inference techniques
- Following fast-moving developments: an emerging infectious disease, rapidly evolving regulation across jurisdictions

### Import (coming soon)
A curated collection of external content — papers, articles, books. Organized, annotated, and cross-referenced.

### Author (coming soon)
Your own creative and professional output — notes, projects, task lists. Structured, searchable, and maintained.

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

- "I need to understand treatment options for [condition]"
- "I want to track developments in [field]"
- "I need to monitor [topic] and stay current on new developments"

Claude Code determines the appropriate book type (currently: scout), creates the book in your library, and guides you through building it.

### Day-to-day use

- **Browse**: `/library` → browse (or open `~/alexandria/index.html` in a browser)
- **Add more books**: `/library` → add a book
- **Update a book**: `cd` into it and work with Claude Code directly
- **Reorganize**: `/library` → reorganize when the structure needs adjusting

## What uses Claude Code and what doesn't

**Requires Claude Code** (internet + Anthropic account): Creating a new library, adding books, and creating scouts (the scout process involves research, schema design, editorial writing, systematic critique, and script generation). During these tasks, your prompts and responses pass through Anthropic's servers. Your data files — YAML, markdown, scripts — remain on your machine and are not uploaded.

**Works fully offline, no AI or subscription needed:** Reading and browsing your library, navigating via HTML links, regenerating READMEs, editing entries, running discovery scripts. Once built, the files are entirely yours and work independently of any service.

**No local model alternative currently exists for creating scouts.** The seven-phase process — particularly research, critique, and editorial writing — depends on Claude's capabilities. The skills are plain markdown instructions; if a local-model agent runner with comparable quality becomes available, they will work without modification.

## What's in this repo

### Skills
- [/library](skills/library/SKILL.md) — create and manage your library (main entry point)
- [/new-scout](skills/new-scout/SKILL.md) — create a scout for any topic (also available directly)

### Reference docs
- [docs/scout/](docs/scout/) — process phases, critique checklist, schema patterns, walkthroughs

### Project direction
- [ASPIRATIONS.md](ASPIRATIONS.md) — project vision, technical minimalism, planned book types
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

### 6. Install the skills

```
mkdir -p ~/.claude/skills
cp -r ~/alexandria/skills/* ~/.claude/skills/
```

No output means it worked.

### 7. Create your library

```
claude
```

At the Claude Code prompt, type:
```
/library
```

Name your library (or press Enter for "alexandria"). Your library directory is now set up.

### 8. Add your first book

From the `/library` prompt, choose "add a book" and describe what you need:

- "I need to understand treatment options for [condition]"
- "I want to track developments in [field]"
- "I need to monitor [topic] and stay current on new developments"

Claude Code guides you from there — asking about scope, audience, and how you'd want to compare entries. You provide the direction; it handles the construction.

### 9. Browse your library

In Claude Code: `/library` → browse

In a browser:
- **macOS**: `open ~/alexandria/index.html`
- **Windows (WSL)**: `explorer.exe $(wslpath -w ~/alexandria/index.html)`
- **Linux**: `xdg-open ~/alexandria/index.html`

### 10. Add more books

In Claude Code: `/library` → add a book. Same process as step 8.

### Troubleshooting

**"command not found"**: The tool isn't installed. Return to the relevant step above.

**"permission denied"**: Try `sudo` before the command (e.g., `sudo cp -r ...`).

**`/library` not recognized**: Re-run step 6. Ensure `~/.claude/skills/` exists.

**Other issues**: Start Claude Code and describe the problem — it can often diagnose and fix things directly.
