## Backing up your collection

Alexandria uses a two-track approach to backup, each track suited to what it covers. Understanding the distinction makes both work better and makes recovery from problems straightforward.

### The two tracks

**Git tracks the textual backbone of your collection.** Catalog metadata, item READMEs, notes, the wiki generator's configuration, skill files. When git is enabled (the default for new collections), every skill that modifies a collection file makes a commit automatically. You can rewind changes and, when GitHub-push support lands, push the repo to a private GitHub account for off-machine backup of everything git tracks. See `docs/guides/version-control-for-your-collection.md` for how git works in practice.

**`/coll-backup` backs up everything to a location you choose.** That includes the binary content git deliberately doesn't track (PDFs, photos, audio, video), the generated wiki, plus a full copy of the textual backbone. The destination is yours to pick — an external drive, a cloud-synced folder (iCloud Drive, Google Drive, Dropbox, OneDrive), or another folder on your machine. The skill detects cloud folders automatically and offers them as first-class options.

Together, the two tracks give you complete coverage:

| Risk | What helps |
|---|---|
| Accidental edit or deletion | Git (rewind via `git restore`) |
| Accidental loss of a photo or PDF | `/coll-backup` (restore from external backup) |
| Whole-machine failure (dead laptop) | GitHub clone + `/coll-backup` restore |
| Cloud-service failure (Dropbox loses data) | Git repo + local backup on external drive |

### What `/coll-backup` does

Run `/coll-backup` from anywhere inside your collection directory. The skill:

1. **First run — asks where to back up to.** Detects cloud-synced folders on your machine (iCloud Drive, Google Drive, Dropbox, OneDrive) and offers them as numbered options alongside "External drive or folder" and "Another location." When you pick one, the skill appends `alexandria-backup-{collection-name}/` as a subdirectory to keep the backup scoped.

2. **Subsequent runs — confirms the stored destination.** You see `Backup destination: {path}. Use this target? [Y/n]` and usually just hit Enter.

3. **Notifies you about stray files.** Before copying, the skill scans the collection root for files or directories that aren't part of the usual alexandria structure. If it finds any, it lists them so you can decide whether to remove them before backing up. It does not block — you can proceed with them included if that's what you want.

4. **Validates the destination.** Refuses dangerous targets (the collection itself, a parent of the collection, `/`, `$HOME` directly). Destinations that would cause a recursive backup or a --delete disaster are rejected before anything touches disk.

5. **Runs rsync** with `-a --delete` to mirror the collection's current state into the destination subdirectory. The `--delete` flag keeps the backup a true mirror — files you remove from your collection are removed from the backup, too. Because everything is scoped to `alexandria-backup-{collection-name}/`, unrelated content on the destination drive is never touched.

6. **Saves the destination** for next time and prints a restore command.

### What to put in your collection (and what not to)

The backup mirrors the collection directory. If you wouldn't want something backed up, don't put it there.

**Belongs in the collection:**

- Item directories (per section): metadata, README, notes, content (PDFs, photos, etc.)
- Scout directories (each its own git repo)
- Catalog: `.collection-index.yaml`
- Journal: `collection-context.md`
- Collection-level READMEs and CLAUDE.md

**Does not belong:**

- Loose files at the collection root that aren't alexandria-managed. A stray tax return PDF, a scratch note, a temporary file — these don't belong.

`/coll-backup` will back up whatever's there, but alexandria's structure assumes the collection directory is for collection content. Stray files at the root are notified at backup time.

### Restoring from a backup

The backup is a direct copy of your collection — no proprietary archive format, no special restore tool. To restore to a new or rebuilt collection path:

```
rsync -a {destination}/ {new-collection-path}/
```

That's it. Every file is in its place. If version control was enabled, the `.git/` directory is part of the backup, so git history is restored too. Scouts retain their own git repos. Open `wiki/index.html` in a browser and the collection is fully browseable again.

### When to run `/coll-backup`

No strict rule; whatever rhythm feels right. Practical options:

- **After any session where you added meaningful items or notes.** Lowest effort, highest reliability — the backup is current with your recent work.
- **Weekly or monthly.** For users who add items regularly, a recurring cadence works fine because rsync is incremental.
- **Before major changes.** Renaming the collection, restructuring sections, importing another collection — any operation that touches a lot of files.

### Can I automate it?

Yes, on any Unix-family machine. The skill's command (`uv run python tools/backup_collection.py {collection_path}`) can be scheduled via `cron`, `launchd` (on macOS), or a systemd timer (on Linux). This is a small setup that's out of scope for alexandria itself — you'd configure the scheduler to run the command on whatever cadence you prefer. First-run prompts aren't interactive-friendly in a cron context; run the skill interactively once to pick a destination, and then subsequent runs confirm the stored destination automatically (still prompts, so for cron you'd need to pipe `y` or pass a flag — not currently supported; noted as a future enhancement).

### Troubleshooting

If the skill reports an error, it points at a section in `docs/guides/troubleshooting.md`. Common ones:

- **`rsync-not-installed`** — rsync isn't on your machine. One install command, usually. See the troubleshooting anchor for the specific command per OS.
- **`backup-destination-unsafe`** — the destination you picked is inside the collection, contains the collection, or is `/` / `$HOME` directly. Pick a different folder outside the collection.
- **`rsync-failed`** — rsync ran but exited nonzero. The collection itself is untouched; read the rsync output for specifics (usually a permissions issue on the destination or a full disk).

### Further reading

- `docs/guides/version-control-for-your-collection.md` — git's role in the two-track story.
- [rsync man page](https://linux.die.net/man/1/rsync) — the authoritative reference for the `-a --delete` semantics the skill relies on.
