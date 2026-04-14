# alexandria

## Quick start

- **Building a new collection from scratch?** Type `/coll-build-new-collection`
- **Working on an existing collection?** Type `/coll-menu` for guided options, or type `/coll-` and press tab for direct access to all collection skills

If you need help at any point, just describe what you're trying to do in plain
language. See the [guides](docs/guides/) for reference on terminals, YAML,
book structure, scouts, and troubleshooting.

## A note about permissions

When working on the collection, you'll sometimes see prompts asking "Do you want
to proceed?" before a command runs. This is a safety feature — Claude Code asks
before making changes to your files. It's always safe to say "Yes" for the commands
the collection skills run (creating directories, copying files, reading metadata).
If you're ever unsure, choose "No" and ask what the command does — Claude will
explain in plain language.

---

## For developers working on alexandria

This repo contains the alexandria toolkit — Claude Code skills and reference docs for
building and organizing private curated collections.

### Repo structure
- `.claude/skills/` — all collection skills (coll-build-new-collection, coll-menu,
  coll-physical, coll-hardcover, coll-paperback, coll-digital, coll-new-scout,
  coll-scout, coll-notes)
- `docs/collection/` — collection-level specs (universal book shape)
- `docs/scout/` — scout book type reference docs (process, prompts, conventions, examples)
- `docs/guides/` — user-facing guides (terminal basics, YAML, book anatomy, scouts, troubleshooting)
- `tools/` — Python tools (wiki generator, templates, stylesheet)
- `tests/` — automated tests and manual testing checklist

### Development notes
- Skill files must be self-contained — they're copied into each collection's `.claude/skills/`
- Skills in this repo are the master copies; `/coll-build-new-collection` copies them into new collections
- Users update their collection's skills via `/coll-menu` → update-skills (re-copies from this repo)
- Reference docs in docs/scout/ informed the /coll-new-scout skill; they're not loaded during build sessions
- Changes to skills should be reflected in both the skill file and any relevant reference docs
- Future book types will add: a skill in `.claude/skills/` and reference docs in `docs/[type]/`
