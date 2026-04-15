# /coll-build-new-collection

Create a new personal collection — a directory on your machine where items of all
types live, organized by sections, with a catalog and a browseable wiki view.

This skill is typically run once. After the collection exists, use `/coll-menu` for
guided management or invoke individual `/coll-*` skills directly to add items,
remove items, and so on.

## Before starting

**Always start by asking the user for a name and location.** Go straight to
the two questions below — do not check the filesystem or rely on memory from
previous sessions first. Your memory about whether a collection exists at a
given path may be stale (the user may have deleted it, moved it, or started
fresh since your last session). The user invoked this skill because they want
to create a new collection; trust that intent.

After the user provides a name and location, **verify by actually reading the
filesystem** — check whether `.collection-index.yaml` exists at that specific
path right now. Do not rely on memory to answer this; only trust what the
filesystem shows. If the file exists, let the user know and ask: create a
fresh collection there (overwriting the index), use a different location, or
work with the existing one? If it doesn't exist, proceed with creation.

## The workflow

1. **Ask the user what to name their collection.** Default: "my-collection". The name
   is used in the catalog and wiki homepage. It doesn't need to match the directory
   name but typically does.

2. **Ask where to create it.** Default: `~/my-collection`. The user can choose any
   path. The directory will be created if it doesn't exist.

3. **Create the collection directory** and initialize `.collection-index.yaml`:

   ```yaml
   collection_name: "my-collection"
   created: "YYYY-MM-DD"
   source_repo: "/path/to/current/project"
   sections: {}
   ```

   The `source_repo` field records where the alexandria repo lives on this machine.
   It's used by `/coll-menu` → update-skills to find the latest skill files.
   Set it to the current project root (the directory Claude Code is running from,
   which should be the cloned alexandria repo on first run).

4. **Copy the collection skills** from the current project's `.claude/skills/`
   directory into the new collection's `.claude/skills/` directory:

   ```
   {new-collection}/.claude/skills/
   ├── coll-menu/SKILL.md
   ├── coll-build-new-collection/SKILL.md
   ├── coll-physical/SKILL.md
   ├── coll-hardcover/SKILL.md
   ├── coll-paperback/SKILL.md
   ├── coll-digital/SKILL.md
   ├── coll-new-scout/SKILL.md
   ├── coll-scout/SKILL.md
   └── coll-notes/SKILL.md
   ```

   This makes all `/coll-*` commands available when the user starts Claude Code
   from their collection directory. They don't need to install skills globally.

5. **Create a root README.md** for the collection:

   ```markdown
   # {collection name}

   A private curated collection managed by [alexandria](https://github.com/msyvr/alexandria).

   ## Sections

   (Sections will appear here as you add items.)

   ## Browsing

   Open `wiki/index.html` in any browser for the full browseable view.
   Or start Claude Code from this directory and type `/coll-menu` for guided access.
   ```

6. **Create a CLAUDE.md** for the collection. This is what Claude reads on
   every session start from the collection directory. It should orient Claude
   to the collection context and guide first interactions:

   ```markdown
   # {collection name}

   This is a private collection managed by alexandria. The user is working
   from inside their collection — it already exists.

   ## Quick start

   - **New here?** Type `/coll-menu` for a guided menu of what you can do
   - **Adding items?** Type `/coll-physical`, `/coll-digital`, or `/coll-new-scout`
   - **Browsing?** Type `/coll-menu` → browse, or open `wiki/index.html` in a browser
   - **Need help?** Just describe what you're trying to do

   Type `/coll-` and press tab to see all available commands.

   ## Important

   - Do NOT offer to create a new collection — this collection already exists
   - Do NOT offer to run `/coll-build-new-collection` — that skill is for
     creating collections from the alexandria repo, not for use inside an
     existing collection
   - The `.collection-index.yaml` in this directory is the collection's catalog
   - Items are organized in section subdirectories
   ```

7. **Tell the user what to do next:**

   > Your collection is ready at `{path}`.
   >
   > To start using it, **close this Claude Code session first** (type `/exit`
   > or press `Ctrl+C`), then open a new terminal session from your collection
   > directory:
   >
   > ```
   > cd {path}
   > claude
   > ```
   >
   > (Or open a new terminal tab with `Cmd+T` on macOS, then run those two
   > commands there.)
   >
   > From your collection directory, type `/coll-menu` for guided options, or
   > invoke skills directly:
   > - `/coll-physical` — catalog a physical item
   > - `/coll-digital` — add digital content (files, URLs, text)
   > - `/coll-new-scout` — create a living knowledge base on a topic
   > - `/coll-scout` — import an existing scout into the collection
   >
   > Type `/coll-` and hit tab to see all available commands.

## What this skill does NOT do

- Does not create any items (that's what the other `/coll-*` skills are for)
- Does not require an existing collection (that's the whole point — it creates one)
- Does not install skills globally (skills live in the collection's `.claude/skills/`)
