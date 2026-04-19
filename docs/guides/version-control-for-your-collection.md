## Version control for your collection

This guide is the reference for one of the practical skills alexandria exercises: using git to version-track your collection. It starts with what you most need to know about safety and privacy, then covers the small set of commands that matter in practice.

### What git actually does for your collection

When you create a collection (or opt in later via `/coll-enable-version-control`), alexandria runs `git init` inside the collection directory. From that point on, every skill that modifies collection files — adding an item, writing notes, updating the journal, importing another collection — records its change in the git repo automatically. You don't run any git commands yourself; the auto-commits happen in the background.

What this gets you:

- **Rewind.** If you accidentally delete a note, overwrite a description, or break something you didn't mean to, you can roll a single file or the whole collection back to an earlier state. One command, no fancy tools required.
- **History.** You can see what changed between two points in time, and why. The commit messages from alexandria's auto-commits describe each change ("Add physical item: The Dispossessed," "Journal entry: 2026-04-18," etc.).
- **Cross-machine portability.** If you eventually connect your collection to a GitHub repo (or any other remote), you can clone the same collection on another machine, or recover from a dead laptop. Git handles the sync.

### Privacy first: what git actually sends when you push

This is ground-floor awareness for anyone using git on files they care about. Read this section before connecting your collection to any remote.

**Every commit is permanent in history.** When you commit a file, it goes into git's history. Even if you later delete the file, the deleted version remains in history. Pushing your repo to GitHub (or anywhere) sends the full history, not just the current state. Which means:

- **Anything you've ever committed is included in a push.** Secrets, drafts, embarrassing notes you meant to delete — if it was committed, it's in the history.
- **Deleting a committed file doesn't scrub it.** The file is gone from the *current* state but still in *past commits*. Someone browsing history sees it.
- **If you accidentally commit a secret (API key, password, private note) and push, the right response is usually to rotate the secret** (generate a new one, invalidate the old) rather than try to scrub git history. History scrubbing is technical and mistake-prone; rotation is simple and certain.

**Alexandria's default `.gitignore` is your first line of defense.** It excludes common sensitive-file patterns by default:

- `.env`, `.env.*` — environment files that typically hold API keys
- `*.key`, `*.pem`, `*.pfx`, `*.p12` — cryptographic keys
- `credentials*`, `secrets*`, `id_rsa*`, `id_ed25519*` — common credential-file names
- `.aws/`, `.ssh/`, `.gnupg/` — directories holding tool credentials
- Binary formats (PDFs, images, audio, video) — these go to `/coll-backup`, not git

If you drop a file matching one of those patterns into your collection, git simply doesn't track it. No accidental commit, no push surprise.

**Only commit what you'd show to the audience of your push.** If your collection's repo is private on GitHub, the audience is just you and anyone you explicitly invite. If it's public, the audience is the whole internet. **Default to private.** GitHub's free tier allows unlimited private repos, and there's no reason to publish a personal collection unless you've specifically decided you want to.

**Your commit email is visible on every commit.** When you push, the email in your git identity appears on every commit in your repo's history. GitHub offers a "noreply" email of the form `YourUsername+ID@users.noreply.github.com` that you can use instead of your real address. See [GitHub's docs on commit email](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address) for how to set it up for a specific repo or globally.

### What to do in practice (day to day)

For most users, most of the time: **nothing**. Alexandria's skills auto-commit as you work. You don't type any git commands.

The one moment it helps to know something: when you want to rewind.

**Rewind a single file to an earlier version:**

```
cd ~/my-collection
git log --oneline {path/to/file}
```

That prints a list of commits that touched the file, newest first. Each line looks like `a3f1b2c Add notes to the-dispossessed`. Copy the short hash of the commit you want to go back to, then:

```
git restore --source=a3f1b2c {path/to/file}
```

The file is now at its state from that commit. Your other files are unchanged. Nothing else happens.

**See what changed in a recent commit:**

```
git show {commit-hash}
```

Or to see the most recent commit:

```
git show HEAD
```

**Undo the last commit (keep the changes in your files):**

```
git reset --soft HEAD~1
```

This is useful if the auto-commit happened but you realized you wanted to bundle the change with the next one. Your files are untouched; only the commit record is rewound.

### If you want to push to a private GitHub repo

GitHub-push support is planned as a separate alexandria skill and isn't available yet. When it lands, it'll walk you through creating a private repo, setting up authentication, and pushing — with guardrails against accidentally making the repo public or pushing sensitive files.

If you want to push manually in the meantime, the short version: create a private repo on GitHub (explicitly private, never public for a personal collection unless you've decided otherwise), add it as a remote with `git remote add origin git@github.com:yourusername/your-collection.git`, and `git push -u origin main`. Re-read the privacy section above before doing this — pushing is one-way in terms of publication, and your entire committed history goes in the initial push.

### Disabling version control

Run `/coll-disable-version-control` from inside the collection. This removes the `.git/` directory and the collection's `.gitignore`. Your items, notes, metadata, and wiki are untouched. You can re-enable later with `/coll-enable-version-control`, but that starts a fresh history — the record between disable and re-enable is not preserved.

### Further reading

- [Pro Git book](https://git-scm.com/book/en/v2) — the free canonical reference for git. Chapters 1 and 2 cover everything most users need.
- [GitHub's commit email docs](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address) — how to use a noreply email for commits.
- `docs/guides/backing-up-your-collection.md` — git's sibling. Git versions the textual backbone; `/coll-backup` handles binary content and the generated wiki.
