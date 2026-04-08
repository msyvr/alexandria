# alexandria

Build and organize a personal curated library — a collection of living resources on topics that matter to you.

alexandria is a set of Claude Code skills for creating, organizing, and maintaining a personal library of structured "books." Each book is a self-contained project you own and understand. The library provides a lightweight organizational layer so you can find things as the collection grows.

See [ASPIRATIONS.md](ASPIRATIONS.md) for where this project is headed.

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
- **[Claude Code](https://claude.ai/claude-code)** — an AI assistant that runs in your terminal. It reads the alexandria skills and does the research, building, and organization work. You'll need an Anthropic account.
- **A terminal** — Claude Code runs here. On macOS, open Terminal. On Windows, use WSL.
- **Python 3.10+** — for the scripts within built tracker books. Check with `python3 --version`.

### Optional
- **A GitHub account** — for automated discovery in tracker books. Not required; everything works offline.
- **Git** — recommended for version control of individual books.

### No coding experience required
You don't need to know how to code. Claude Code generates everything. You guide the process by answering questions about what you care about. You will use the terminal to run a few commands — the process walks you through exactly what to type.

If you're new to working in a terminal, that's fine. The skills you pick up here — running commands, reading structured data, using version control — are useful far beyond this tool. See [ASPIRATIONS.md](ASPIRATIONS.md) for more on this.

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
