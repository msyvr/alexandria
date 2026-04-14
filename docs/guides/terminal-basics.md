# Working with your collection: terminal basics

This guide covers the practical skills you need to work with your private collection. It assumes you've never worked in a terminal before, or have but want a clear reference for how things fit together in the context of alexandria.

## What is a terminal?

A terminal is a text-based window where you type commands and see results. It's how you talk to your computer without clicking buttons. Every computer has one built in:

- **macOS**: press `Cmd + Space`, type `Terminal`, press Enter
- **Windows**: use WSL (Windows Subsystem for Linux) — see the [setup walkthrough](../../README.md#detailed-setup-walkthrough) for installation
- **Linux**: look for "Terminal" or "Konsole" in your applications

When you open a terminal, you see a prompt — something like `~$` or `user@computer:~$`. This is where you type. After you type a command and press Enter, the computer runs it and shows you the result.

## Directories (folders)

A directory is a folder. They're the same thing — "directory" is the terminal word, "folder" is the visual word you see in Finder or File Explorer.

Your collection is a directory. Each book in your collection is a subdirectory inside it. The sections are directories too.

```
my-collection/              ← this is a directory
├── fiction/                 ← this is a subdirectory (a section)
│   ├── the-dispossessed/   ← this is a subdirectory (a book)
│   └── short-stories/      ← another book
└── research/               ← another section
    └── ai-safety-scout/    ← a book (this one is a scout)
```

### Useful commands

| What you want to do | Command | Example |
|---|---|---|
| See where you are | `pwd` | Shows `/Users/you/my-collection` |
| List what's here | `ls` | Shows the files and directories in the current location |
| Go into a directory | `cd name` | `cd fiction` moves you into the fiction directory |
| Go up one level | `cd ..` | Goes back to the parent directory |
| Go home | `cd ~` | Goes to your home directory (where `my-collection` probably lives) |
| Go to your collection | `cd ~/my-collection` | Goes directly to your collection from anywhere |

You can always type `pwd` to check where you are if you get lost.

## Git repos

Git is a tool that tracks changes to files over time — like a detailed undo history for an entire directory. A directory that uses git is called a "git repo" (short for repository).

**Not every directory is a git repo.** Your collection directory (`my-collection/`) is not a git repo — it's just a plain directory. But each book inside it might be its own git repo, especially scouts. This means each book has its own change history, independent of the others.

### Why this matters

You don't need to use git directly. But it's useful to know that:

- **Scout books are git repos.** They track their own changes, which is helpful when the scout is actively updating.
- **Your collection is not a git repo.** It's a plain directory holding book directories. The `.collection-index.yaml` and wiki files are managed by the collection skills, not by git.
- **Claude Code uses the git repo to scope its memory.** When you start Claude Code inside a git repo, it remembers things about that specific repo between sessions. When you start it in a non-git directory (like your collection root), it doesn't have repo-scoped memory — but it can still read the collection's context files.

### If you want to learn more about git

Git is a deep topic, but the basics that matter for your collection are:

- `git status` — shows what has changed since the last save point
- `git log --oneline` — shows the history of changes
- `git add . && git commit -m "description"` — saves a snapshot of the current state

You don't need these to use your collection. They're here if you're curious.

## Claude Code sessions

Claude Code runs inside a terminal. When you type `claude` and press Enter, you start a session — a conversation with Claude that lasts until you close it (by typing `/exit` or pressing `Ctrl+C`).

### Permission prompts

While working, Claude Code sometimes shows a prompt like:

```
Bash command
  mkdir -p ~/my-collection/fiction

Do you want to proceed?
> 1. Yes
  2. Yes, allow reading from ...
  3. No
```

This is a safety feature. Claude Code asks before running commands that create, change, or read files on your machine. For the commands the collection skills run (creating directories, copying files, reading your catalog), it's safe to say **Yes**. If you're ever unsure what a command does, choose **No** and ask Claude to explain it — it will describe what the command does in plain language before you decide.

### Where you start matters

The directory you're in when you type `claude` determines:

- **Which skills are available.** Your collection's `/coll-*` commands are found because the `.claude/skills/` directory is inside your collection (or a parent of where you are).
- **What Claude knows automatically.** If there's a `CLAUDE.md` in the current directory (or the git repo's root), Claude reads it at the start of the session. This is how scouts give Claude operational context — their `CLAUDE.md` describes the schema, file locations, and update commands.
- **What Claude remembers between sessions.** In a git repo, Claude can build up memory about that project over time. In a non-git directory, it doesn't retain memory but can still read any files you've created (like `context.md`).

### Two common starting points

**From your collection root** (`cd ~/my-collection && claude`):
- All `/coll-*` commands are available
- Good for: browsing, adding books, weeding, settling scouts, reviewing sections, any collection-level operation
- Claude doesn't auto-load any book's context — you're at the collection level

**From inside a specific book** (`cd ~/my-collection/research/ai-safety-scout && claude`):
- All `/coll-*` commands are still available (found in the parent collection's `.claude/skills/`)
- Claude auto-loads this book's `CLAUDE.md` (schema, files, update instructions)
- Good for: substantive work on this specific book (adding many entries, running critique, restructuring)
- The book's operational context is loaded; the rest of the collection isn't

**Rule of thumb**: start from the collection root for general work. Move into a specific book's directory when you're doing focused work on that one book.

## Running multiple sessions

You can have more than one Claude Code session open at the same time. This is useful when you want to work on a scout in one window and manage the collection in another.

### Option 1: Multiple terminal windows

The simplest approach. Open a new terminal window for each session:

- **macOS Terminal**: `Cmd + N` opens a new window
- **Windows (WSL)**: open another WSL instance from the Start menu
- **Linux**: `Ctrl + Shift + N` in most terminals

In one window: `cd ~/my-collection && claude`
In another: `cd ~/my-collection/research/ai-safety-scout && claude`

Each window has its own Claude Code session with its own context.

### Option 2: Terminal tabs

Most modern terminals support tabs — multiple sessions in the same window, switching between them with keyboard shortcuts.

- **macOS Terminal**: `Cmd + T` opens a new tab. `Cmd + Shift + [` and `Cmd + Shift + ]` switch between tabs. Or click the tabs at the top.
- **iTerm2** (a popular macOS terminal, free): same shortcuts, plus split panes with `Cmd + D` (side by side) or `Cmd + Shift + D` (top and bottom)
- **Windows Terminal** (recommended for WSL): `Ctrl + Shift + T` for a new tab. `Ctrl + Tab` to switch.
- **Linux**: varies by terminal. Most support `Ctrl + Shift + T` for new tabs.

Tabs are convenient because you can see which tab is which (label them or look at the directory name in the prompt) and switch quickly.

### Option 3: Terminal multiplexers (for the adventurous)

Tools like `tmux` or `screen` let you manage multiple sessions inside a single terminal window, with named sessions that persist even if you close the terminal. These are powerful but have a learning curve — worth exploring later if you find yourself juggling many sessions regularly.

### Which option to start with

**Start with tabs.** They're built into every modern terminal, require no installation, and give you the most useful pattern: one tab for your collection, one tab for a specific book you're working on. You can always come back to the collection tab to browse, add a new book, or check on other items.

## A typical workflow

1. Open your terminal
2. Navigate to your collection: `cd ~/my-collection`
3. Start Claude Code: `claude`
4. Do collection-level work: `/coll-menu` to browse, add books, or manage
5. If you need to do focused work on a scout:
   - Open a new tab (`Cmd + T` on macOS)
   - In the new tab: `cd ~/my-collection/research/ai-safety-scout && claude`
   - Work on the scout there
   - Switch back to your collection tab when done
6. When finished, type `/exit` in each Claude Code session to close it
