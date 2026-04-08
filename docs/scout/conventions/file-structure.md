# File Structure Convention

Standard layout for repos built with the scout build process.

## Structure

```
repo-name/
├── README.md                 # Generated output — do not edit directly
├── CLAUDE.md                 # Process state and operational context
├── data/
│   └── entries.yaml          # Canonical structured data
├── docs/
│   ├── getting-started.md    # Hand-written editorial (Part 1 of README)
│   └── [audience].md         # Audience-specific docs as needed
├── scripts/
│   ├── generate_readme.py    # Schema validation + README generation
│   └── discover.py           # Automated discovery
├── references/               # Reading lists, related resources
├── .github/
│   └── workflows/
│       └── discover.yml      # Discovery automation schedule
└── temp/                     # Working files (gitignored)
    └── research-dump.md      # Raw research output
```

## File Purposes

### `data/entries.yaml`
The single source of truth for all structured data. Every entry lives here. The generate script reads this file to produce the README.

Schema is defined and validated in `scripts/generate_readme.py`, not in a separate schema file. This keeps the repo simple.

### `docs/getting-started.md`
Hand-written editorial content. This is concatenated as Part 1 of the README by the generate script. It should read naturally standalone and as part of the README.

### `docs/[audience].md`
Audience-specific docs created when Phase 5 (Critique) identifies specialized needs. These are linked from the README but not concatenated into it.

### `scripts/generate_readme.py`
Does three things:
1. Validates `data/entries.yaml` against the schema (required fields, controlled vocabularies)
2. Generates lens tables and category sections from the data
3. Concatenates editorial + generated content → `README.md`

Run with: `python scripts/generate_readme.py`

### `scripts/discover.py`
Searches configured sources for new candidates. Outputs results to stdout or creates GitHub issues.

Run with: `python scripts/discover.py`

### `references/`
Optional directory for reading lists, link collections, or other reference material that supports the landscape but isn't structured data.

### `temp/`
Working directory for intermediate files during the build process. Add to `.gitignore`. The research dump lives here during Phases 2-3.

## What Goes Where

| Content type | Location | Generated? |
|-------------|----------|------------|
| Structured entry data | `data/entries.yaml` | No — hand-curated |
| Getting-started guide | `docs/getting-started.md` | No — hand-written |
| Audience-specific docs | `docs/[name].md` | No — hand-written |
| Lens comparison tables | In README.md | Yes — from entries.yaml |
| Category sections | In README.md | Yes — from entries.yaml |
| Final README | `README.md` | Yes — concatenated |
| Schema definition | In generate_readme.py | No — Python constants |
| Discovery config | In discover.py | No — Python constants |

## Conventions

- **README.md is generated**: Never edit it directly. Edit the source (entries.yaml or docs/) and regenerate.
- **One YAML file**: All entries in one file. Don't split by category — that creates merge conflicts and makes the schema harder to validate.
- **No config files**: Schema, lens definitions, and discovery config are Python constants in their respective scripts. Config files add indirection without value at this scale.
- **Dependencies**: Only pyyaml and requests. Pin versions in a requirements.txt if using CI.
