# Tracker Process Overview

A seven-phase process for building curated landscape and research-tracking repos. The process encodes when to ask the user for direction, what to critique, and how to iterate — so the output is consistently better than a single-pass generation.

## Roles

- **User**: Drives direction — scope, audience, perspectives, category groupings, editorial tone
- **Claude Code**: Drives implementation — research, schema design, code, self-critique

The process is designed so that user input happens at decision points (scope, structure, critique resolution) and Claude Code handles the volume work (research gathering, YAML population, script writing, systematic critique).

## The Seven Phases

| Phase | Driver | Goal |
|-------|--------|------|
| [1. Scope](1-scope.md) | User | Define topic, audiences, perspectives |
| [2. Research](2-research.md) | Claude Code | Gather comprehensive landscape data |
| [3. Structure](3-structure.md) | Collaborative | Design schema, lenses, categories |
| [4. Build](4-build.md) | Claude Code | Create YAML, editorial content, generate pipeline |
| [5. Critique](5-critique.md) | Claude Code | Systematic self-critique and fixes |
| [6. Automate](6-automate.md) | Claude Code | Discovery + staleness automation |
| [7. Maintain](7-maintain.md) | User | Ongoing updates via automation + manual review |

## Process Flow

```
Scope → Research → Structure → Build → Critique → Automate → Maintain
  ↑                   ↑                   |
  |                   |                   |
  └── user decision   └── user decision   └── iterate until clean pass
```

## Key Principles

1. **Critique is the core differentiator.** A single-pass generation misses category misassignments, brand-recognition bias, missing risk callouts, and bundled entries that should be split. The critique phase catches these systematically.

2. **Editorial content is hand-written, not generated.** Getting-started guides, decision trees, and risk callouts are crafted with intent — not templated from the data.

3. **Order by quality, not brand.** Recommendations are ordered by security properties, fit for purpose, and technical merit — not by GitHub stars or name recognition.

4. **Cast wide, then tighten.** Research gathers broadly; structure and critique narrow to what belongs.

5. **The repo is self-contained.** No dependencies beyond pyyaml/requests. The generate script, discovery script, and all data live in one repo.
