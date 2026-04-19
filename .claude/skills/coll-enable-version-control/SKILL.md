# /coll-enable-version-control

Enable git version control for a collection that doesn't currently have it.
Use this for collections that were built before version control was a default,
or collections where the user opted out at build time and has since changed
their mind.

## Before starting

Detect the collection context by walking up from the current directory looking
for `.collection-index.yaml`. If not found, explain that this skill must run
inside a collection directory.

Check whether the collection already has a `.git/` directory. If it does,
explain that version control is already enabled and point the user at
`/coll-menu` for other actions.

## The workflow

1. **Locate the alexandria repo** that this collection was built from (the
   directory that holds `tools/init_version_control.py`). Typically this is
   `~/alexandria` or a sibling of the user's collection directory. If the
   user isn't sure, ask.

2. **Run the initializer** from the alexandria repo directory, pointing at
   the user's collection:

   ```
   uv run python tools/init_version_control.py {collection_path} \
     --message "Initialize version control for existing collection"
   ```

   The script:
   - Runs `git init` in the collection
   - Copies the `.gitignore` template
   - Resolves git identity (global if set, asks if missing)
   - Makes an initial commit capturing the collection's current state

   Pass its output through to the user as-is; do not summarize.

3. **Confirm what was done.** Briefly tell the user:

   - Version control is now enabled
   - The initial commit captures the collection's state *now* — anything
     before this moment is present as files but not as git history
   - Changes from this point forward will be auto-committed by skills that
     modify collection files
   - They can disable it anytime with `/coll-disable-version-control`

## What this does NOT do

- Does not reconstruct history for changes that happened before this skill
  ran — git can only track forward from the initial commit
- Does not push to GitHub or any remote — that is a separate step (future
  skill, not yet available)
- Does not modify any of the collection's items, metadata, or wiki content

## If something goes wrong

If the initializer errors out, surface the error message to the user (it
includes a plain-English description and a link to the troubleshooting
guide). Do not attempt to repair git state by running commands by hand
unless the user asks.
