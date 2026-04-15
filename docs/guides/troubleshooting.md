# Troubleshooting

Common issues and how to fix them.

## Skills not found

**Symptom**: You type `/coll-menu` (or any `/coll-*` command) and Claude Code doesn't recognize it.

**Cause**: You're not in a directory where the skills are discoverable. The skills live in your collection's `.claude/skills/` directory. Claude Code looks for skills in the current directory and its parents.

**Fix**:
- Make sure you're inside your collection directory: `cd ~/my-collection`
- Verify the skills are there: `ls .claude/skills/` — you should see `coll-menu`, `coll-physical`, etc.
- If the `.claude/skills/` directory is empty or missing, the skills weren't copied during collection creation. Re-run from the alexandria repo: `cd ~/alexandria && claude`, then use `/coll-build-new-collection` and provide your existing collection's path.

## Wiki not generating

**Symptom**: You run the wiki generator and get an error about a missing file or module.

**Fix**:
1. Make sure dependencies are installed: `cd ~/alexandria && uv sync`
2. Run the generator with the full path: `uv run python tools/generate_wiki.py .`
3. If you get "No such file or directory" for `.collection-index.yaml`, the collection index is missing. Create it by asking Claude (from inside the collection) to scan the collection and rebuild the index.

## Photo not reading (physical items)

**Symptom**: Claude can't extract metadata from a photo you provided.

**Possible causes**:
- The file path is wrong — check that the file exists: `ls /path/to/your/photo.jpg`
- The file format isn't supported — use JPEG, PNG, HEIC, or WebP
- The photo is too dark, blurry, or the item spine text isn't legible
- The file is very large (>20MB) — try a smaller version

**Fix**: Try a clearer photo, or switch to manual entry. Claude will always offer manual entry as a fallback.

## metadata.yaml has an error

**Symptom**: The wiki generator or Claude Code reports an error reading an item's `metadata.yaml`.

**Common causes**:
- A colon in a value that isn't quoted: `title: LLMs: A Survey` should be `title: "LLMs: A Survey"`
- Inconsistent indentation (mixing tabs and spaces, or different numbers of spaces)
- A missing required field (slug, title, book_type, section, description, date_added, form, media_type, status)

**Fix**: Open the file in a text editor, find the issue, correct it. See the [YAML basics guide](yaml-basics.md) for formatting rules. If you're stuck, ask Claude to look at the file and fix it.

## "command not found" errors

**Symptom**: You type a command (`claude`, `uv`, `python3`, `git`) and the terminal says "command not found."

**Fix**: The tool isn't installed. Follow the relevant step in the [setup walkthrough](../../README.md#detailed-setup-walkthrough):
- `claude` → install Claude Code from [claude.ai/claude-code](https://claude.ai/claude-code)
- `uv` → `curl -LsSf https://astral.sh/uv/install.sh | sh`
- `python3` → install from [python.org/downloads](https://python.org/downloads)
- `git` → macOS: `xcode-select --install`; Linux: `sudo apt install git`

After installing, close and reopen your terminal (some tools aren't available until you start a new session).

## Collection index seems stale

**Symptom**: You added or removed an item, but the wiki or browse view doesn't reflect the change.

**Fix**: Regenerate the wiki:
```
uv run python tools/generate_wiki.py .
```

If the `.collection-index.yaml` is also stale (e.g., an item you added manually without using a skill), ask Claude to rebuild the index by scanning the collection for `metadata.yaml` files.

## Scout discovery script fails

**Symptom**: `python scripts/discover.py` in a scout directory throws an error.

**Common causes**:
- Missing dependencies — run `pip install pyyaml requests` (or `uv pip install pyyaml requests` if using uv)
- GitHub API rate limit — the script may need a `GITHUB_TOKEN` environment variable for authenticated requests
- Network issue — check your internet connection

**Fix**: Read the error message — it usually tells you what's wrong. If it mentions a missing module, install it. If it mentions rate limits, set up a GitHub token.

## Something else went wrong

Start Claude Code inside your collection directory and describe the problem:

```
cd ~/my-collection
claude
```

Then tell Claude what happened. It can read your files, check for issues, and often fix things directly. Include:
- What you were trying to do
- What happened instead
- Any error messages you saw
