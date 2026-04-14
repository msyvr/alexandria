# alexandria

## First time here?

If you're a new user setting up your private collection for the first time:

1. Type `/coll-build-new-collection` — this creates your collection and copies
   the skills into it so they're available whenever you work from your collection
   directory.

2. After creation, the skill tells you what to do next: navigate to your collection
   directory and start a new Claude Code session there.

3. From your collection directory, type `/coll-menu` for a guided menu of everything
   you can do, or type `/coll-` and press tab to see all available commands.

If you need help at any point, just describe what you're trying to do in plain
language. See the [guides](docs/guides/) for reference on terminals, YAML,
book structure, scouts, and troubleshooting.

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
