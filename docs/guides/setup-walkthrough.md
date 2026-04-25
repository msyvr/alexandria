## Setup walkthrough

Step-by-step instructions for setting up alexandria from scratch. Every command is shown exactly as you would type it. The setup is also the first occasion to use most of the collection skills; that is intentional.

Alexandria needs a few tools installed on your machine. For background on what each tool is and why it is needed, see the [Python and uv guide](python-and-uv.md). For the terminal itself, see the [terminal basics guide](terminal-basics.md).

### 1. Open a terminal

A terminal is a text window where you type commands. See the [terminal basics guide](terminal-basics.md) for more detail.

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

Alexandria's tools depend on a few shared Python packages (for reading YAML files, converting markdown to HTML, extracting PDF metadata, and so on). [uv](https://docs.astral.sh/uv/) is the tool that installs and manages these. See the [Python and uv guide](python-and-uv.md) for more about what these are.

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
