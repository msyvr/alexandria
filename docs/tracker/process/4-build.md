# Phase 4: Build

**Driver**: Claude Code
**Goal**: Create the repo — YAML data, editorial content, generate script, README.

## Process

### 1. Create YAML data file
Populate `data/entries.yaml` with all entries from the research dump, using the agreed schema from Phase 3.

```yaml
entries:
  - name: "Example Tool"
    category: "Category Name"
    url: "https://example.com"
    description: "One-sentence description."
    # ... domain-specific fields from schema
    # ... lens tags
    notes: "Editorial context — why this matters, caveats, notable discussions."
```

### 2. Write hand-crafted editorial content
Create `docs/getting-started.md` and any audience-specific docs.

See [editorial-writing.md](../prompts/editorial-writing.md) for structure and tone guidance.

**Critical**: Editorial content is hand-written, not generated from the YAML data. The getting-started guide, decision trees, and risk callouts are crafted with intent. This was a key lesson from awesome-agent-sandboxes — generated editorial reads like a data dump, not a guide.

### 3. Build the generate script
Create `scripts/generate_readme.py` with:
- Schema validation (catch malformed entries before they hit the README)
- Lens table generation (one table per lens, auto-generated from YAML + lens definitions)
- Category section generation (entries grouped by category with descriptions)
- Concatenation (editorial + generated sections → final README)

**Design principle**: Schema and lens definitions are Python constants in the script, not a separate config file. This keeps the repo simple — one file to understand, not a config system to learn.

```python
# Schema as Python constants
REQUIRED_FIELDS = ["name", "category", "url", "description"]
VALID_CATEGORIES = ["Category A", "Category B", ...]
LENS_DEFINITIONS = {
    "lens_name": {
        "display": "Lens Display Name",
        "values": ["value1", "value2", ...],
        "description": "What this lens helps you triage"
    }
}
```

### 4. Generate and verify
Run the generate script, review the output README, verify:
- Schema validation passes
- All entries appear in the correct category section
- Lens tables are accurate
- Editorial content reads naturally before and after generated sections

## Key Guidance

### Self-contained repo
The scaffolded repo has no dependencies beyond pyyaml (for YAML parsing) and requests (for discovery script in Phase 6). No frameworks, no build systems, no CI config beyond a simple GitHub Actions workflow.

### File structure
Follow the conventions in [file-structure.md](../conventions/file-structure.md):
```
repo/
├── README.md              # Generated output (do not edit directly)
├── CLAUDE.md              # Process state tracker
├── data/
│   └── entries.yaml       # Canonical structured data
├── docs/
│   ├── getting-started.md # Hand-written editorial
│   └── [audience].md      # Audience-specific docs (if needed)
├── scripts/
│   ├── generate_readme.py # Schema validation + README generation
│   └── discover.py        # Automated discovery (Phase 6)
└── references/            # Reading lists, related resources
```

### Notes field
The `notes` field in YAML entries is where editorial context lives per-entry. It's nullable — not every entry needs notes. But entries with important caveats, tradeoffs, or context should have them. This is where "this tool requires a commercial license for production use" or "active development, API may change" belongs.

## Common Pitfalls

- **Generating editorial content**: Resist the urge to template getting-started content from the data. Write it by hand with the audience in mind.
- **Over-engineering the generate script**: It concatenates files and generates tables. It doesn't need a plugin system, templating engine, or config parser.
- **Forgetting schema validation**: Without validation, malformed entries silently produce broken output. Validate early, fail loudly.
- **Missing notes on recommended entries**: If an entry appears in a decision tree or getting-started guide, its notes should explain tradeoffs. Every recommendation needs a "what this doesn't protect against" callout.
