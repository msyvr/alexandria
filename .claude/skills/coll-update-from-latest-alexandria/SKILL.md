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

1. **Check for a stored default collection.** Read
   `.claude/state/default-collection` (relative to the alexandria repo
   root). If the file exists and the path it contains still has a
   `.collection-index.yaml`, treat it as the current default; read its
   `collection_name` from that index file. If the file is missing or
   the path is no longer valid, there is no default.

2. **Offer the default first (if one exists).** This avoids the scan
   latency when the user wants what they had last time:

   > Default collection: **{name}** at `{path}`. Use this? [Y/n]

   - If the user accepts (yes / Y / empty): skip to step 4.
   - If the user declines: continue to step 3. Do NOT delete the
     stored default yet — it will be reassigned by the scan if
     appropriate.

3. **Scan for collections and reassign the default.** Look for
   directories containing `.collection-index.yaml` in:
   - `~/` (direct children only — e.g., `~/my-collection`)
   - `~/Documents/` (direct children)
   - The parent directory of the current project (siblings of the repo)

   For each found, read the `collection_name` from the index file.

   **Reassign the stored default** based on the scan results, writing the
   new value to `.claude/state/default-collection` (create the directory
   if needed, overwrite the file if present):

   - If any found collection's path is different from the current stored
     default, the first such "different" collection becomes the new
     default.
   - Otherwise, if there is no stored default and the scan found at least
     one collection, the first found becomes the default.
   - Otherwise, the stored default is unchanged.

   The default is reassigned even if the user just declined it in step 2.
   That is intentional: the old default still appears in the list below,
   so picking it is a single keystroke (forgiveness for accidental
   rejection), and the new default gives the user a fresh option on the
   next invocation without forcing the scan.

   **Present the numbered list** of all found collections plus a manual
   entry option, in discovery order (the old default is shown if it was
   found, because it remains easy to pick):

   > Found these collections:
   > 1. my-collection (~/my-collection)
   > 2. work-references (~/Documents/work-references)
   > 3. Enter a different path

   If no collections are found and no default exists, ask for the path
   directly.

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

7. **Offer a one-time permission pin (do NOT silent-write).** After a
   successful update, optionally offer to pin this exact script in the
   alexandria repo's local settings so future runs skip the approval prompt.

   Process:

   a. Read `.claude/settings.local.json` at the alexandria repo root. If it
      does not exist, treat it as an empty object.
   b. Check whether `permissions.allow` already contains the string
      `"Bash(bash scripts/update_collection.sh:*)"`. If present, skip this
      whole step silently — do not mention it.
   c. If absent, show the user the exact JSON that would be merged in:

      ```json
      {
        "permissions": {
          "allow": ["Bash(bash scripts/update_collection.sh:*)"]
        }
      }
      ```

      Then say, verbatim or close to it:

      > This pins ONLY this exact script, scoped to the alexandria repo's
      > local settings. It lets future `/coll-update-from-latest-alexandria`
      > runs skip the approval prompt for the update command. Add it? (y/n)

   d. If the user says yes: merge the entry into
      `.claude/settings.local.json` (do not overwrite unrelated keys or
      existing allow rules — append to the `allow` array, create
      `permissions.allow` only if missing).
   e. If the user says no or anything non-affirmative: move on. Do NOT
      persist the decline to disk; the offer will reappear next run. This
      is intentional — we keep no hidden state.

   **Hard constraints — do not violate these even if asked:**
   - Never pin any command broader than
     `Bash(bash scripts/update_collection.sh:*)`.
   - Never write to `~/.claude/settings.json` (user-global settings).
   - Never merge in permissions unrelated to this skill.
   - Never perform the merge without an explicit "yes" in the current turn.

8. **Remind the user.** Updated skills take effect in the next Claude Code
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
