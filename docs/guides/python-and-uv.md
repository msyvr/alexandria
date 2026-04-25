## Python and uv: what they are and why you need them

Alexandria uses a few tools behind the scenes. Knowing Python or uv is not among the skills alexandria sets out to teach — these are dependencies the collection runs on, not fluencies you are building. One paragraph on each is enough to understand what is happening when you set things up and when something goes wrong.

### At a glance

| Tool | What it does | You need to |
|---|---|---|
| **Python** | Runs alexandria's scripts | Install it once ([python.org](https://www.python.org/downloads/)) |
| **uv** | Installs Python dependencies | Install it once, then run `uv sync` in the alexandria directory |
| **Git** | Downloads alexandria and tracks file changes | Install it once, then run `git clone` to download |
| **Claude Code** | The AI assistant that reads the skills and does the work | Install it once ([claude.ai/claude-code](https://claude.ai/claude-code)) |

None of these require ongoing maintenance. Install once, use as needed. The rest of this guide explains each one in more detail.

### What is a programming language?

A programming language is a way of writing instructions that a computer can follow. Instead of clicking buttons in an app someone built, you write the instructions yourself (or, increasingly, have an AI write them for you). The instructions are stored as text files — readable, editable, and yours to keep.

### What is Python?

[Python](https://www.python.org/) is the most widely used programming language for AI and data work. When you hear about AI tools, machine learning, or data science, Python is almost always involved somewhere. It's popular because it's relatively readable (compared to other languages) and has a vast ecosystem of shared code that anyone can use.

Alexandria's tools — the wiki generator, metadata extractors, and discovery scripts — are written in Python. You don't need to read or write Python to use alexandria. You just need Python installed on your machine so the tools can run.

### What are dependencies?

When someone writes a program, they often build on code that other people have already written and shared. These shared building blocks are called **dependencies** — your program depends on them to work.

For example, alexandria's wiki generator depends on:
- **PyYAML** — reads the YAML files that store your catalog data
- **markdown-it-py** — converts markdown files to HTML for the wiki
- **beautifulsoup4** — reads web pages when you import content from URLs

These are all open-source Python packages, freely available and widely used. You don't install them one by one — that's what uv does for you.

### What is uv?

[uv](https://docs.astral.sh/uv/) is a tool that manages Python dependencies. When you run `uv sync` inside the alexandria directory, it:

1. Reads the list of dependencies alexandria needs (stored in a file called `pyproject.toml`)
2. Downloads and installs each one
3. Keeps them organized in a separate area (called a "virtual environment") so they don't interfere with anything else on your computer

That's it. One command (`uv sync`) and everything is ready. If alexandria adds new dependencies later, running `uv sync` again picks them up.

#### Installing uv

On macOS or Linux, paste this into your terminal:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

This downloads and installs uv. You only need to do this once. After that, `uv sync` and `uv run` are available in your terminal.

The `curl` command in that line is a built-in tool that downloads files from the internet. The rest of the line tells it where to find the uv installer and to run it immediately.

### What is a virtual environment?

When uv installs dependencies, it puts them in a folder called `.venv` inside the alexandria directory. This is a "virtual environment" — a self-contained space where Python packages live without affecting the rest of your computer.

You don't need to think about the virtual environment. It's created automatically by `uv sync` and used automatically when you run commands with `uv run`. If you delete it accidentally, running `uv sync` again recreates it.

### What is Git?

[Git](https://git-scm.com/) is a tool that tracks changes to files over time — like a detailed undo history for an entire directory. When you "clone" the alexandria repo, you're downloading a copy of all the files plus their full change history.

You need git installed to download alexandria (`git clone`). After that, you don't need to use git directly — though it's there if you want to track changes to your own collection. See the [terminal basics guide](terminal-basics.md) for more on git repos.

