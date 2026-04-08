# Critique Checklist

Run this checklist after Phase 4 (Build). For each finding, decide: fix mechanically, or ask the user for direction. Iterate until a clean pass.

## Category Integrity

- [ ] **Write inclusion tests**: For each category, write a one-sentence test: "An entry belongs in [Category] if and only if [criterion]."

- [ ] **Test entries against definitions, not names**: Read each entry's description, then check it against the category's inclusion test. Ignore the category name — names mislead. This is the single most common error. In awesome-agent-sandboxes, "Docker Sandboxes" entries were miscategorized because entries matched the category *name* (they used Docker) but not the *definition* (purpose-built sandbox environments).

- [ ] **Flag debatable assignments**: If an entry could reasonably go in two categories, flag it for the user. Don't silently pick one.

- [ ] **Check for single-entry categories**: A category with one entry usually means: the entry belongs elsewhere, or the category definition is too narrow, or you're missing entries. Investigate.

- [ ] **Check for mixed classification axes**: Are categories grouping by the same principle? Mixing "by technology" (containers, VMs, WASM) with "by use case" (CI/CD, development, production) creates entries that belong in two categories.

## Perspective Bias

- [ ] **Check ordering**: Are recommendations and prominent entries ordered by quality, security properties, or fit for purpose? Or by brand recognition and GitHub stars? In awesome-agent-sandboxes, Docker-based solutions were listed first despite not being the most secure option — because Docker is the most recognized brand.

- [ ] **Check adoption-as-quality bias**: In early or niche fields, low adoption doesn't mean low quality. A tool with 50 GitHub stars might be the best technical solution. Don't treat star count as a quality signal.

- [ ] **Distinguish general-purpose from purpose-built**: Is it clear which entries are purpose-built for the domain vs. general-purpose tools with incidental applicability? Koyeb is a general cloud platform; NanoClaw is purpose-built for agent sandboxing. A reader needs to know this to make a decision.

- [ ] **Check risk callouts for recommended options**: Every entry that appears in a getting-started guide, decision tree, or "recommended for X" section must have risk/tradeoff callouts. "We recommend X" without "X doesn't protect against Y" is irresponsible.

- [ ] **Check risk specificity**: Are risk callouts specific and sourced? "Containers share a kernel" is generic. "Docker's default seccomp profile allows ~300 of 435 syscalls; see [documentation link] for which calls are permitted" is actionable.

## Completeness

- [ ] **Check for entries that should be split**: Are any entries actually multiple distinct projects bundled together? Different maintainers, different architectures, different use cases = different entries. Wasmtime, WasmEdge, and wasmCloud are three projects, not one "WASM runtimes" entry.

- [ ] **Check for entries that don't fit scope**: Re-read the scope document from Phase 1. Are there entries that were included during research but don't actually fit? A framework with incidental sandbox support isn't a sandbox tool.

- [ ] **Check for underrepresented entries**: Are there entries that are technically strong but received less attention because they're less well-known? In awesome-agent-sandboxes, nono (a lightweight container alternative) was initially underrepresented despite being highly relevant for the security-conscious audience.

- [ ] **Check for missing specialized docs**: Is there an audience segment that deserves its own document? The safety research doc in awesome-agent-sandboxes emerged from recognizing that security-focused readers needed a different framing than the getting-started guide provided.

## Schema Hygiene

- [ ] **Check for low-variance fields**: Any field where >80% of entries have the same value? That field isn't helping anyone triage. Drop it, fold it into notes, or rethink the vocabulary. In awesome-agent-sandboxes, `status: active` was true for nearly every entry.

- [ ] **Check for hollow required fields**: Any required field that's frequently null, "N/A", or "see repo"? Either make it optional, or research the actual values. Hollow fields signal that the schema doesn't match the available data.

- [ ] **Check lens tag accuracy**: Were lens tags assigned thoughtfully per-entry, or bulk-assigned based on category? Read 5 random entries and verify their lens tags are correct for that specific entry, not just plausible for its category.

## Editorial Quality

- [ ] **Test getting-started for least-technical audience**: Read the getting-started guide as if you know nothing about the domain. Does it explain what the domain is, why it matters, and how to pick a first option? Or does it assume knowledge?

- [ ] **Check decision tree coverage**: Does the decision tree cover the major use cases identified in Phase 1? Are there common reader questions that aren't addressed?

- [ ] **Check signposting**: Is it clear where beginners should read vs. where technical users should read? In awesome-agent-sandboxes, this was an explicit section break with guidance.

- [ ] **Check notes on recommended entries**: Every entry mentioned in editorial content should have notes in the YAML that explain its tradeoffs. If the getting-started guide says "start with X," the YAML notes for X should explain what X is good at and what it's not.

## Running the Checklist

1. Go through each item systematically. Don't skip items that "seem fine" — the point is to check.
2. For each finding, categorize:
   - **Mechanical fix**: Reorder, split entry, add missing field, correct lens tag. Do it.
   - **User direction needed**: Category reassignment, scope decision, new doc. Flag it.
3. After fixing, re-run from the top. First-pass fixes often reveal second-pass issues.
4. A clean pass (no new findings) means you're done. Typically takes 2-3 passes.
