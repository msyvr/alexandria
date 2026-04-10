# /new-scout

Create a scout — a curated, living knowledge base that monitors a topic for you. Built
through a seven-phase process that produces a resource you own, understand, and can maintain.

## Adapting to the user

Gauge the user's technical comfort early. Use plain language by default — "categories,"
"comparison angles," "structured data" rather than "YAML schema," "lenses," "controlled
vocabulary." Introduce technical terms naturally when the user is ready, not upfront.

Ask about direction, not implementation:
- "What should this scout cover? What's out of scope?"
- "Who is this for? What questions will they bring?"
- "How would you want to compare entries — by cost, by evidence quality, by ease of access?"

Don't ask about YAML field names, Python code structure, or API configuration.

## Process principles
- User drives direction and preferences. Claude Code drives implementation and self-critique.
- After building, run the critique checklist (Phase 5 below) before declaring done.
  Category misassignment, bias in recommendations, and missing risk callouts
  are the most common issues.
- Order recommendations by quality/fit, not brand recognition or popularity.
- Editorial content is hand-written with the reader in mind. Risk callouts are mandatory for
  recommended options.

## The seven phases

### Phase 1: Scope (user-driven)
Define what the scout covers, who it's for, and what questions readers bring.

Ask the user:
1. **Topic**: What's the landscape? What's in, what's out?
2. **Audiences**: Who will use this? What do they need?
3. **Triage questions**: What does someone want to compare or filter by?
4. **Seed entries**: Any known entries to start from?

Output: A scope document (informal, in `temp/scope.md`) that anchors all later work.

Pitfalls: scope too broad ("AI tools" never ships), scope too narrow (3 entries), skipping
this phase (leads to rework).

### Phase 2: Research (Claude Code-driven, user reviews)
Gather comprehensive data on the landscape.

**Web access required**: This phase needs web search and web fetch tools to find current
information. If web tools are not available, tell the user: "I can research from my training
data, but I may miss recent developments. You can help by sharing URLs or pasting content
from recent sources you've found." Work with whatever access is available — training data
research is better than no research, but be explicit about its currency limitations.

Process:
1. Systematically search relevant sources (GitHub, product pages, arXiv, blogs, forums —
   whatever fits the domain)
2. Output a raw research dump to `temp/research-dump.md`
3. User reviews for gaps: "what about X?" / "you missed Y"

For each entry found, capture: name, URL, one-sentence description, editorial notes (why it
matters, caveats), and source.

Pitfalls: brand-recognition bias (you'll find the famous options first — actively search for
alternatives), stopping too early (8 entries for a 20+ landscape means search more broadly),
missing adjacent spaces.

### Phase 3: Structure (collaborative — most user dialog here)
Design the schema, perspectives, and categories.

1. **Propose a schema**: Present research and suggest fields. User pushes back on fields
   that don't earn their keep. Test: can you fill each field with meaningful, varying values
   for 5 entries? If not, drop it.

2. **Propose comparison angles** (lenses): 2-4 controlled-vocabulary fields that let readers
   triage from different perspectives. Each must answer a real reader question and have
   meaningful variation. If >80% of entries share one value, the lens is useless.

3. **Propose categories**: Group entries into sections. Write a one-sentence inclusion test
   for each category, then test every entry against the *definition*, not the *name*.

Built-in checkpoint — before leaving this phase, verify:
- [ ] Entries tested against category definitions, not just names
- [ ] Categories don't mix classification axes (e.g., "by technology" and "by use case")
- [ ] No single-entry categories
- [ ] General-purpose tools distinguished from purpose-built ones
- [ ] Bundled entries split (different maintainers/architectures = different entries)
- [ ] Lens value distributions checked

### Phase 4: Build (Claude Code-driven)
Create the repo: YAML data, editorial content, generate script, README.

File structure:
```
data/entries.yaml          — all structured data (single source of truth)
docs/getting-started.md    — hand-written editorial (Part 1 of README)
docs/[audience].md         — audience-specific docs as needed
scripts/generate_readme.py — schema validation + README generation
scripts/discover.py        — automated discovery (Phase 6)
references/                — reading lists, related resources
README.md                  — generated output (do not edit directly)
```

The generate script defines schema and lens definitions as Python constants (not a config
file), validates entries.yaml, generates lens tables and category sections, and concatenates
editorial + generated content into README.md.

**Critical**: Editorial content (getting-started guide, decision trees, risk callouts) is
hand-written, not generated from data. Every recommended option must include a risk/tradeoff
callout: what it's good for and what it doesn't cover.

**Generate CLAUDE.md and context.md** in the built scout for persistent context:

**CLAUDE.md** uses this template (operational facts only, lean enough not to waste session
context). Auto-loaded by Claude Code on return visits:

```markdown
# {scout-name}

A scout monitoring {topic in one sentence}.

## Scope
{2-3 sentences: what's in, what's out}

## Schema
- Categories: {list}
- Lenses: {list with one-line descriptions}
- Required fields: {list}

## Files
- `data/entries.yaml` — all structured entries
- `docs/getting-started.md` — orientation guide
- `scripts/generate_readme.py` — regenerate README from data
- `scripts/discover.py` — find new candidates
- `context.md` — full interaction history and decisions

## Updating
- Add entries: edit `data/entries.yaml`, then `python scripts/generate_readme.py`
- Find new entries: `python scripts/discover.py`
- Re-run critique: ask Claude Code to "run the critique checklist on this scout"

## Recent context

(updated automatically by /take-notes after each significant work session)

For full decision history and user preferences, see `context.md`.
```

**context.md** is initialized empty (the /take-notes skill creates the initial file
structure on its first invocation). After generating it, immediately invoke /take-notes
to log the build's decisions: scope, schema choices, lens definitions, category rationale,
and any notable user preferences observed during the build dialog.

**Generate index.html** alongside README.md. The HTML is self-contained: wrap the README
content in the alexandria HTML template (inline CSS, no JavaScript, no external files).
Use Python's `markdown` library to convert the generated README.md content to HTML. The
HTML uses the same inline stylesheet as the library-level pages so all pages in the
library have a consistent reading experience. Links within the HTML point to other `.html`
files (not `.md`) so browser navigation works over `file://`.

### Phase 5: Critique (the core differentiator)
Systematically find and fix problems before declaring done.

Run this checklist. For each finding: fix mechanically, or ask the user for direction.
Iterate until a clean pass (typically 2-3 passes).

**Category integrity:**
- [ ] One-sentence inclusion test written for each category
- [ ] Every entry tested against the definition, not the name
- [ ] Debatable assignments flagged for user
- [ ] No single-entry categories
- [ ] No mixed classification axes

**Bias:**
- [ ] Ordered by quality/fit, not brand recognition
- [ ] Low adoption not treated as low quality (especially in niche fields)
- [ ] General-purpose vs. purpose-built clearly distinguished
- [ ] Risk callouts present for every recommended option
- [ ] Risks are specific and sourced, not generic

**Completeness:**
- [ ] No entries that should be split into separate entries
- [ ] No entries that don't fit the scope
- [ ] No technically strong but underrepresented entries (brand-bias check)
- [ ] Specialized audience needs identified (may need dedicated docs)

**Schema hygiene:**
- [ ] No field with >80% same value
- [ ] No required field frequently null or "N/A"
- [ ] Lens tags assigned per-entry, not bulk-assigned by category

**Editorial:**
- [ ] Getting-started readable for least-technical audience
- [ ] Decision tree covers major use cases
- [ ] Clear signposting between beginner and technical content
- [ ] Every recommended entry has notes explaining tradeoffs

After critique completes, invoke /take-notes to log the critique findings and resolutions.

### Phase 6: Automate (Claude Code-driven)
Set up discovery so the scout stays current.

Build `scripts/discover.py` to search configured sources for new candidates. It surfaces
candidates for human review — never auto-adds. Optionally add a GitHub Actions workflow
to run discovery on a schedule.

Add staleness checking for existing entries (last commit date, archive status, URL health).
Add a quarterly review nudge (are categories still right? have lenses collapsed?).

### Phase 7: Maintain (user-driven, automation-assisted)
Keep the scout useful over time.

- Review discovery candidates (weekly or when convenient)
- Handle staleness flags
- Re-run critique after significant changes (10+ entries added)
- Update editorial when recommended entries change
- Add specialized docs as audience needs emerge

After significant maintenance work (10+ entries added, schema migration, re-categorization,
re-running critique), invoke /take-notes to log what was done and any decisions made.

## Library integration

If this scout is being created within a library (detected by `.library-index.yaml` in a
parent directory), update the library index after Phase 4 (Build) completes:
- Add the book entry with name, path, type ("scout"), creation date, and a one-line
  description derived from the scope document.

If invoked standalone (no library context), skip this step — the scout works independently.
