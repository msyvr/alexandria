# /coll-build-new-collection

Create a new personal collection — a directory on your machine where books of all
types live, organized by sections, with a catalog and a browseable wiki view.

This skill is typically run once. After the collection exists, use `/coll-menu` for
guided management or invoke individual `/coll-*` skills directly to add books,
remove books, and so on.

## Before starting

If a `.collection-index.yaml` already exists in the current directory or a parent,
a collection already exists here. Let the user know and ask if they want to create
a separate collection elsewhere, or work with the existing one.

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
   ├── coll-scout/SKILL.md
   └── coll-notes/SKILL.md
   ```

   This makes all `/coll-*` commands available when the user starts Claude Code
   from their collection directory. They don't need to install skills globally.

5. **Create a root README.md** for the collection:

   ```markdown
   # {collection name}

   A personal curated collection managed by [alexandria](https://github.com/msyvr/alexandria).

   ## Sections

   (Sections will appear here as you add books.)

   ## Browsing

   Open `wiki/index.html` in any browser for the full browseable view.
   Or start Claude Code from this directory and type `/coll-menu` for guided access.
   ```

6. **Tell the user what to do next:**

   > Your collection is ready at `{path}`. To start using it:
   >
   > ```
   > cd {path}
   > claude
   > ```
   >
   > Then type `/coll-menu` for guided options, or invoke skills directly:
   > - `/coll-physical` — catalog a physical book
   > - `/coll-digital` — add digital content (files, URLs, text)
   > - `/coll-scout` — create a living knowledge base on a topic
   >
   > Type `/coll-` and hit tab to see all available commands.

## What this skill does NOT do

- Does not create any books (that's what the other `/coll-*` skills are for)
- Does not require an existing collection (that's the whole point — it creates one)
- Does not install skills globally (skills live in the collection's `.claude/skills/`)
