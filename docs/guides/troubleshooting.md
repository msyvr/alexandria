## Troubleshooting

Common issues and how to fix them.

### Skills not found

**Symptom**: You type `/coll-menu` (or any `/coll-*` command) and Claude Code doesn't recognize it.

**Cause**: You're not in a directory where the skills are discoverable. The skills live in your collection's `.claude/skills/` directory. Claude Code looks for skills in the current directory and its parents.

**Fix**:
- Make sure you're inside your collection directory: `cd ~/my-collection`
- Verify the skills are there: `ls .claude/skills/` — you should see `coll-menu`, `coll-physical`, etc.
- If the `.claude/skills/` directory is empty or missing, the skills weren't copied during collection creation. Re-run from the alexandria repo: `cd ~/alexandria && claude`, then use `/coll-build-new-collection` and provide your existing collection's path.

### Wiki not generating

**Symptom**: You run the wiki generator and get an error about a missing file or module.

**Fix**:
1. Make sure dependencies are installed: `cd ~/alexandria && uv sync`
2. Run the generator with the full path: `uv run python tools/generate_wiki.py .`
3. If you get "No such file or directory" for `.collection-index.yaml`, the collection index is missing. Create it by asking Claude (from inside the collection) to scan the collection and rebuild the index.

### Photo not reading (physical items)

**Symptom**: Claude can't extract metadata from a photo you provided.

**Possible causes**:
- The file path is wrong — check that the file exists: `ls /path/to/your/photo.jpg`
- The file format isn't supported — use JPEG, PNG, HEIC, or WebP
- The photo is too dark, blurry, or the item spine text isn't legible
- The file is very large (>20MB) — try a smaller version

**Fix**: Try a clearer photo, or switch to manual entry. Claude will always offer manual entry as a fallback.

### metadata.yaml has an error

**Symptom**: The wiki generator or Claude Code reports an error reading an item's `metadata.yaml`.

**Common causes**:
- A colon in a value that isn't quoted: `title: LLMs: A Survey` should be `title: "LLMs: A Survey"`
- Inconsistent indentation (mixing tabs and spaces, or different numbers of spaces)
- A missing required field (slug, title, book_type, section, description, date_added, form, media_type, status)

**Fix**: Open the file in a text editor, find the issue, correct it. See the [YAML basics guide](yaml-basics.md) for formatting rules. If you're stuck, ask Claude to look at the file and fix it.

### "command not found" errors

**Symptom**: You type a command (`claude`, `uv`, `python3`, `git`) and the terminal says "command not found."

**Fix**: The tool isn't installed. Follow the relevant step in the [setup walkthrough](../../README.md#detailed-setup-walkthrough):
- `claude` → install Claude Code from [claude.ai/claude-code](https://claude.ai/claude-code)
- `uv` → `curl -LsSf https://astral.sh/uv/install.sh | sh`
- `python3` → install from [python.org/downloads](https://python.org/downloads)
- `git` → macOS: `xcode-select --install`; Linux: `sudo apt install git`

After installing, close and reopen your terminal (some tools aren't available until you start a new session).

### Collection index seems stale

**Symptom**: You added or removed an item, but the wiki or browse view doesn't reflect the change.

**Fix**: Regenerate the wiki:
```
uv run python tools/generate_wiki.py .
```

If the `.collection-index.yaml` is also stale (e.g., an item you added manually without using a skill), ask Claude to rebuild the index by scanning the collection for `metadata.yaml` files.

### Scout discovery script fails

**Symptom**: `python scripts/discover.py` in a scout directory throws an error.

**Common causes**:
- Missing dependencies — run `pip install pyyaml requests` (or `uv pip install pyyaml requests` if using uv)
- GitHub API rate limit — the script may need a `GITHUB_TOKEN` environment variable for authenticated requests
- Network issue — check your internet connection

**Fix**: Read the error message — it usually tells you what's wrong. If it mentions a missing module, install it. If it mentions rate limits, set up a GitHub token.

### Update-script errors

The update script (`/coll-update-from-latest-alexandria`) is careful about your local edits and will pause and ask for your decision when it cannot act safely. If it prints an error, the anchor at the end of the message points here.

#### not-a-collection

The script expects the path you gave it to contain a `.collection-index.yaml` file, which every alexandria collection has at its root. If it doesn't find one, it stops rather than risk writing into an unrelated directory.

**Fix**: double-check the path. If you meant a collection that doesn't exist yet, run `/coll-build-new-collection` first.

#### managed-paths-missing

The update script reads `tools/managed-paths.yaml` in the alexandria repo to know which files to update. If that file is missing, it stops — without it, the script doesn't know what to manage.

**Fix**: make sure you are running the script from a complete alexandria repo. If you cloned partially or the file was deleted, re-run `git pull` (or re-clone the repo).

#### manifest-corrupted

The manifest (`.alexandria-manifest.yaml` in your collection) records which upstream files alexandria manages in your collection. If it becomes unreadable — usually because something modified it by hand and broke the YAML — the script moves it aside and re-creates a fresh one on the next run.

**Fix**: re-run the update. The damaged file is kept with a `.corrupted-<timestamp>` suffix for reference if you need to look at it. The fresh manifest will surface every upstream-managed file for your decision (one-time event), because without the old manifest the script can't tell which files you customized vs. which are old upstream versions. Pick `[A]` at the batch prompt if you haven't customized anything; otherwise walk through them normally.

#### schema-too-new

The manifest carries a `schema_version` field. If it's newer than the script understands, the script refuses to run rather than risk misinterpreting it.

**Fix**: update the alexandria repo to a newer version (`cd ~/alexandria && git pull && uv sync`). If you already have the latest and still see this, the manifest may have been hand-edited — see manifest-corrupted above.

#### init-manifest-exists

The `--init` mode of the script is used by `/coll-build-new-collection` to write a fresh manifest for a new collection. It refuses to run against a collection that already has a manifest, to avoid overwriting install history that future updates rely on.

**Fix**: you probably don't want `--init` here. If you meant to update the collection, use `/coll-update-from-latest-alexandria` instead (without `--init`). If you genuinely want to reset the manifest (rare — only if the manifest has a bug you can't work around), delete `.alexandria-manifest.yaml` first.

#### editor-not-set

When you pick `[e] Edit manually` to resolve a conflict, the script opens a merge-view file in your text editor. It uses the `EDITOR` environment variable to know which editor to open.

**Fix**: set `EDITOR` to your preferred editor in your shell, then re-run the update. Common choices:

- `export EDITOR=nano` — nano is beginner-friendly and installed on most systems
- `export EDITOR=vim` — vim if you know it
- `export EDITOR="code --wait"` — VS Code (the `--wait` flag is important so the script waits for you to close the file)

To make the setting permanent, add the line to your `~/.bashrc` or `~/.zshrc`. Or skip `[e]` and use `[k]`, `[u]`, or `[d]` for this file.

#### ancestor-commit-unreachable

When you pick `[c] What changed upstream` or `[e] Edit manually`, the script uses git history to reconstruct the version of the file that was last installed. If the repo's history has been rewritten or the repo was re-cloned shallowly, that historical commit may no longer be available.

**Fix**: the `[d] Show the diff` option still works (it compares your local version directly to the current upstream version) and is usually enough to decide. If you want the full three-way view, make sure your alexandria repo has full history (`git fetch --unshallow` if it was cloned shallow).

#### uv-sync-failed

The update succeeded at copying files and saving the manifest, but `uv sync` (which installs any new Python dependencies) returned an error.

**Fix**: run `uv sync` manually inside the collection directory and read the error. Common causes are missing system tools (git, a C compiler) or network issues. The file updates are already saved, so you can retry the sync alone without re-running the update.

#### wiki-regen-failed

The update succeeded but the wiki regeneration step (which builds the browseable HTML) returned an error.

**Fix**: run `uv run python tools/generate_wiki.py .` inside the collection directory and read the error. Common causes are a malformed `metadata.yaml` in one of your items (see the metadata.yaml error section above). The file updates are already saved, so you can retry the wiki generation alone.

### Version-control errors

#### git-not-installed

The version-control setup needs `git`, but it's not installed on the machine.

**Fix**:

- macOS: `xcode-select --install`
- Linux (Debian/Ubuntu): `sudo apt install git`
- Linux (Fedora): `sudo dnf install git`

Then re-run the skill that was trying to enable version control.

#### version-control-already-enabled

You tried to enable git on a collection that already has a `.git/` directory. This is intentional — the skill refuses to overwrite existing history.

**Fix**: nothing needed; version control is already active. If you want to start fresh (lose all history), run `/coll-disable-version-control` first, then re-enable.

#### gitignore-template-missing

The `.gitignore` template at `tools/collection-gitignore.template` is missing from the alexandria repo.

**Fix**: your alexandria repo is incomplete. Run `git pull` in the alexandria repo, or re-clone it.

#### git-init-failed

`git init` returned an error. Usually a permissions issue on the collection directory.

**Fix**: check that you own the collection directory and have write permission. Run `ls -la <collection-path>` to verify. If the directory is read-only or owned by another user, correct the permissions and re-run.

#### git-identity-save-failed

Git couldn't save your name/email for this collection. The `.git/` directory has been created but isn't usable for commits until identity is set.

**Fix**: inside the collection directory, run:

```
git config --local user.name "Your Name"
git config --local user.email "you@example.com"
```

#### git-initial-commit-failed

Git was set up but couldn't make the initial commit. Most often caused by missing identity.

**Fix**: inside the collection directory, run `git status` to see what's staged. Set identity if needed (see `git-identity-save-failed`). Then run `git commit -m "Initial commit"` when ready.

### Backup errors

#### rsync-not-installed

The backup skill needs `rsync`, but it's not installed or isn't on the path.

**Fix**:

- macOS: rsync is built-in. If the command isn't found, try opening a new terminal — your shell may not have picked it up yet.
- Linux (Debian/Ubuntu): `sudo apt install rsync`
- Linux (Fedora): `sudo dnf install rsync`
- Windows (WSL): `sudo apt install rsync` in your WSL terminal

Then re-run `/coll-backup`.

#### backup-destination-unsafe

The destination you picked would either (a) recurse into the collection, (b) overlap with the collection, or (c) is a too-broad path like `/` or your home directory directly. The skill refuses to run in any of these cases because `rsync --delete` would risk your data.

**Fix**: pick a destination folder outside your collection. An external drive, a cloud-synced folder (iCloud Drive, Dropbox, Google Drive, OneDrive), or a different folder on your machine that isn't your home root. The skill appends `alexandria-backup-{collection-name}/` automatically, so you only need to give it the parent.

#### rsync-failed

`rsync` ran but returned an error. Your collection is untouched; the backup may be partial.

**Fix**: read the rsync output for specifics. Common causes:

- Destination disk is full
- Destination drive unplugged mid-operation
- Permission issue on the destination
- Network issue if the destination is on a network mount

After fixing the underlying issue, re-run the skill — rsync is incremental, so it picks up where it left off.

### Something else went wrong

Start Claude Code inside your collection directory and describe the problem:

```
cd ~/my-collection
claude
```

Then tell Claude what happened. It can read your files, check for issues, and often fix things directly. Include:
- What you were trying to do
- What happened instead
- Any error messages you saw
