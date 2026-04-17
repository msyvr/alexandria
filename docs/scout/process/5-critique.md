## Phase 5: Critique

**Driver**: Claude Code (user resolves ambiguous findings)
**Goal**: Systematically find and fix problems before the repo ships.

### Why This Phase Exists

This phase is the core differentiator of the scout build process. A single-pass generation misses problems that only surface through systematic review. The awesome-agent-sandboxes repo had three critique cycles that each materially improved the output:

1. **First critique**: Caught Docker Sandboxes category misassignment, brand-recognition bias in ordering, missing risk callouts
2. **Second critique**: Found bundled entries (Wasmtime/WasmEdge/wasmCloud) that should be split, general-purpose tools mixed with purpose-built ones
3. **Third critique**: Identified that nono was underpromoted despite being highly relevant, prompted the safety research doc

### Process

1. Run the [critique checklist](../prompts/critique-checklist.md)
2. For each finding: fix mechanically, or flag for user direction
3. Iterate until a pass finds nothing new

### The Critique Checklist (summary)

Full checklist with details: [prompts/critique-checklist.md](../prompts/critique-checklist.md)

#### Category integrity
- Write a one-sentence inclusion test per category
- Test every entry against the *definition*, not the *name*
- Flag debatable assignments for user
- Check for single-entry categories
- Check for mixed classification axes

#### Perspective bias
- Ordered by quality/security properties, not brand recognition?
- Low adoption treated fairly in early fields?
- General-purpose vs. purpose-built clearly distinguished?
- Risk/tradeoff callouts for every recommended option?
- Risks specific and sourced, not generic?

#### Completeness
- Entries that should be split?
- Entries that don't fit scope?
- Specialized audience that needs its own doc?

#### Schema hygiene
- Any field >80% same value? Drop it.
- Any required field frequently null? Make optional or research properly.
- Lens tags accurately assigned, not bulk-assigned?

#### Editorial
- Getting-started readable for least-technical audience?
- Decision tree covers major use cases?
- Signpost between beginner and technical content clear?

### Fixing Findings

#### Mechanical fixes (do immediately)
- Reordering entries by properties instead of brand
- Splitting bundled entries into separate entries
- Adding missing required fields
- Correcting lens tag values

#### User-direction fixes (flag and ask)
- Category reassignment where the right category is debatable
- Adding a new category vs. broadening an existing one
- Whether a borderline entry belongs in scope
- Whether to create a specialized doc for a new audience

### Iteration

Keep running the checklist until a pass produces no new findings. Typically this takes 2-3 passes. If you're on pass 5+, you're probably oscillating between two valid choices — pick one and note the tradeoff.

### Common Pitfalls

- **Skipping this phase**: "It looks good" is not a critique. Run the checklist.
- **Fixing everything silently**: Flag ambiguous findings for the user. The point of the process is that the user drives direction.
- **Generic risk callouts**: "Containers share a kernel" is true but unhelpful. "Docker's default configuration exposes the host filesystem via volume mounts; see [CVE-XXXX]" is actionable.
- **Stopping after one pass**: The first pass catches the obvious issues. The second pass catches what the first-pass fixes revealed. The third pass is usually clean.
