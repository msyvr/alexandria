# alexandria

This repo contains the alexandria toolkit — Claude Code skills and reference docs for
building and organizing personal curated collections.

## Repo structure
- `.claude/skills/coll-build-new-collection/SKILL.md` — create a new collection (run once from this repo)
- `.claude/skills/coll-menu/SKILL.md` — guided menu for all collection actions
- `.claude/skills/coll-physical/SKILL.md` — catalog a physical book
- `.claude/skills/coll-hardcover/SKILL.md` — shortcut for hardcover (calls coll-physical)
- `.claude/skills/coll-paperback/SKILL.md` — shortcut for paperback
- `.claude/skills/coll-digital/SKILL.md` — bring in digital content
- `.claude/skills/coll-new-scout/SKILL.md` — create a new scout (living knowledge base)
- `.claude/skills/coll-scout/SKILL.md` — import an existing scout into the collection
- `.claude/skills/coll-notes/SKILL.md` — maintain persistent context
- `docs/collection/` — collection-level reference docs (book shape spec)
- `docs/scout/` — scout book type reference docs (process, prompts, conventions, examples)
- `tools/` — Python tools (wiki generator, templates, stylesheet)
- `tests/` — automated tests and manual testing checklist

## Development notes
- Skill files must be self-contained — they're copied into each collection's `.claude/skills/`
- Skills in this repo are the master copies; `/coll-build-new-collection` copies them into new collections
- Users update their collection's skills via `/coll-menu` → update-skills (re-copies from this repo)
- Reference docs in docs/scout/ informed the /coll-new-scout skill; they're not loaded during build sessions
- Changes to skills should be reflected in both the skill file and any relevant reference docs
- Future book types will add: a skill in `.claude/skills/` and reference docs in `docs/[type]/`
