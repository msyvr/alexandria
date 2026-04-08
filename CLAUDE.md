# alexandria

This repo contains the alexandria toolkit — Claude Code skills and reference docs for
building and organizing personal curated libraries.

## Repo structure
- `skills/library/SKILL.md` — the /library skill (primary entry point for users)
- `skills/new-scout/SKILL.md` — the /new-scout skill (scout book type)
- `docs/scout/` — reference material for the scout book type
  - `process/` — seven-phase process docs
  - `prompts/` — prompt templates (critique checklist, research gathering, etc.)
  - `conventions/` — file structure and schema patterns
  - `examples/` — walkthroughs
- `ASPIRATIONS.md` — project vision and direction
- `TODO.md` — planned additions

## Development notes
- Skill files must be self-contained — they're the only files the user has when building
- Reference docs in docs/scout/ informed the /new-scout skill; they're not loaded
  during a build session
- Changes to the scout process should be reflected in both the skill and the reference docs
- Future book types will add: a skill in skills/ and reference docs in docs/[type]/
