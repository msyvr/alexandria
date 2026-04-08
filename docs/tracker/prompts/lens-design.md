# Lens Design Prompt

Lenses are controlled-vocabulary fields that enable cross-cutting views of the data. They answer the triage questions identified in Phase 1.

## What Makes a Good Lens

A good lens:
1. **Answers a reader's question**: "Is this open source?" → `open_source: yes/no`. "How mature is this?" → `maturity: experimental/stable/production`.
2. **Has meaningful variation**: If 90% of entries share the same value, the lens doesn't help triage. (The `status: active` lesson from awesome-agent-sandboxes.)
3. **Has a small, clear vocabulary**: 3-6 values. If you need more, the lens is probably two lenses or a free-text field.
4. **Is objective or clearly defined**: "quality: high/medium/low" is subjective and will cause arguments. "isolation_level: process/container/vm/hardware" is objective and verifiable.

## Designing Lenses

### Step 1: Start from triage questions
Pull from the Phase 1 scope document. For each triage question, ask: can this be answered with a controlled vocabulary?

| Triage question | Lens? | Why / why not |
|----------------|-------|---------------|
| "Is it open source?" | Yes: `open_source: yes/no` | Binary, objective, varies |
| "Can it run locally?" | Yes: `deployment: local/cloud/both` | Small vocabulary, objective |
| "How secure is it?" | No — too subjective | Use specific fields instead (isolation_level, etc.) |
| "Is it actively maintained?" | Maybe — check variance | If most entries are active, this is the `status` trap |

### Step 2: Check value distribution
For each proposed lens, mentally assign values to all entries from the research dump. If the distribution is:
- **Roughly even** (30/30/40): Good lens.
- **Skewed but useful** (60/30/10): Acceptable if the minority values are important to surface.
- **Dominated** (90/10): Drop it. The minority is better served by a notes callout.

### Step 3: Define vocabulary precisely
For each lens value, write a one-sentence definition. This prevents bulk-assignment errors where entries get tagged based on category rather than individual assessment.

```yaml
maturity:
  experimental: "Pre-1.0 or explicitly labeled experimental by maintainers. API may change."
  stable: "1.0+ release with documented API. Used in production by at least some users."
  production: "Widely deployed in production. Established track record and support."
```

### Step 4: Validate with 5 entries
Pick 5 entries from different categories. Assign lens values. Check:
- Did you hesitate? The vocabulary might need adjustment.
- Did two entries get the same value for all lenses? The lenses might not differentiate enough.
- Did you want a value that doesn't exist? The vocabulary might be missing an option.

## Presenting to the User

Propose 2-4 lenses with:
1. The triage question each lens answers
2. The vocabulary with definitions
3. An example: "Entry X would be tagged [value] because [reason]"

Ask: "Would you actually filter by this? Is there a perspective you'd want that's missing?"

## Common Pitfalls

- **Too many lenses**: 2-4 is the sweet spot. More than 4 and the lens tables become walls of text that nobody reads.
- **Subjective vocabularies**: "good/bad", "easy/hard", "recommended/not recommended" invite disagreement. Stick to observable properties.
- **Forgetting to check variance**: Every lens looks useful in theory. Check the actual distribution before committing.
- **Bulk-assigning by category**: "All container tools are `isolation: container`" might be wrong. Some container tools add VM-level isolation. Assign per-entry.
