# /coll-update-from-latest-alexandria

Update an existing collection to match the current alexandria repo — skills,
tools, dependencies, and generated views. Run this from the alexandria repo
directory after pulling the latest changes.

## When to use this

After updating your alexandria clone:

```
cd ~/alexandria
git pull
uv sync
```

Then start Claude Code from the alexandria repo and run this skill.

## The workflow

1. **Check for a stored default collection.** Run the helper script —
   it does the state-file read, path check, and `collection_name`
   lookup in one shot:

   ```
   bash scripts/get_default_collection.sh
   ```

   - **Exit 0**: stdout is two lines — line 1 is the collection path,
     line 2 is the `collection_name`. Use those values as the current
     default and continue to step 2.
   - **Exit 1/2/3**: no valid stored default. **Skip step 2 — do not
     prompt the user about "choosing a default"** — and go to step 3.

   (The fallback of reading `.claude/state/default-collection` directly
   still works if the helper script isn't available; the skill may do
   that instead when the script is missing.)

2. **Offer the stored default first (only if one exists).** This avoids
   the scan latency when the user wants what they had last time:

   > Default collection: **{name}** at `{path}`. Use this? [Y/n]

   - If the user accepts (yes / Y / an empty line / bare Enter): skip
     to step 4.
   - If the user declines (n / no): continue to step 3. Do NOT delete
     the stored default yet — it may be reassigned by the scan.

3. **Scan for collections, present the list, record the selection.**

   Scan for directories containing `.collection-index.yaml` in:
   - `~/` (direct children only — e.g., `~/my-collection`)
   - `~/Documents/` (direct children)
   - The parent directory of the current project (siblings of the repo)

   For each found, read the `collection_name` from the index file.

   **Handling the stored default across this step** depends on what
   happened in step 2:

   - **If a stored default was just declined (step 2):** among the
     found collections, the first path different from the current
     stored default becomes the new default. Write it to
     `.claude/state/default-collection` now (create the directory if
     needed, overwrite if present). The old default still appears in
     the list below — picking it again is a single keystroke
     (forgiveness for accidental rejection), and the new default gives
     the user a fresh option next time without forcing another scan.

   - **If no default was stored:** do **not** write a default yet. The
     user's selection in this step will become the default, written
     after they pick.

   **Present the numbered list** of all found collections plus a manual
   entry option, in discovery order. Option 1 is always the first-found
   collection — Enter accepts it:

   > Found these collections. Press Enter to accept [1], or type a
   > number to choose something else.
   >
   > 1. my-collection (~/my-collection)
   > 2. work-references (~/Documents/work-references)
   > 3. Enter a different path

   An **empty input (bare Enter) selects option 1**. A digit selects
   that numbered option. Typing a path directly also works and is
   treated as the manual-entry option.

   If no collections are found and no default exists, skip the list and
   ask for the path directly.

   **After the user picks**, if no default was stored at the start of
   step 3, write the selected path to
   `.claude/state/default-collection` now. This makes the user's
   initial selection the default going forward.

4. **Verify the collection.** Whether accepted as the default, selected
   from the list, or entered manually, check that the path contains a
   `.collection-index.yaml`. If not, explain and ask again.

5. **Run the update script.** Execute the repo's bundled update script,
   passing the verified collection path as its single argument. Do NOT
   inline the individual copy/sync/regen steps — always call the script:

   ```
   bash scripts/update_collection.sh {collection_path}
   ```

   The script does all of the following in one shot:
   - Copies `.claude/skills/` from the repo into the collection
   - Copies `tools/` from the repo into the collection
   - Copies `pyproject.toml` from the repo into the collection
   - Runs `uv sync` inside the collection
   - Regenerates the wiki via the collection's own copy of the tools

   If the script exits non-zero, surface its stderr to the user and stop —
   do not attempt to repair the update by running the individual commands
   by hand.

6. **Report what was updated:**
   - Skills: list directories copied (note any new ones)
   - Tools: updated (generator, templates, stylesheet)
   - Dependencies: synced
   - Wiki: regenerated with latest styling and templates

7. **Remind the user.** Updated skills take effect in the next Claude Code
   session from the collection directory:

   > Collection at `{path}` updated:
   > - Skills, tools, and dependencies: latest versions
   > - Wiki: regenerated with current styling
   >
   > To use the updated skills, start a new Claude Code session:
   >
   > ```
   > cd {path}
   > claude
   > ```

## What this updates

- Skill instruction files (`.claude/skills/coll-*/SKILL.md`)
- Wiki generator and templates (`tools/`)
- Stylesheet (`tools/_wiki_style.css` → copied into `wiki/_assets/` on regen)
- Python dependency list (`pyproject.toml`)
- All generated wiki HTML

## What this does NOT modify

- The collection's data (items, metadata, sections, journal content)
- Item directories or their contents (README, metadata.yaml, notes/)
- The `.collection-index.yaml` catalog (read for wiki generation, not written)
