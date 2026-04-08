# Editorial Writing Prompt

Editorial content is hand-written — not generated from YAML data. It provides context, guidance, and opinion that structured data can't capture.

## Getting-Started Guide Structure

The getting-started guide (`docs/getting-started.md`) is the entry point for new readers. Structure:

### 1. What is [topic]?
One paragraph. Assume the reader found this repo via search and might not know the domain well. Define the topic without jargon.

### 2. Why does this matter?
One paragraph. What problem does the domain solve? What goes wrong without it? Ground this in concrete scenarios, not abstractions.

### 3. Quick start: picking your first option
A decision tree or short flowchart. 3-5 questions that lead to a recommendation.

```markdown
**What's your situation?**

- I need to get started quickly with minimal setup
  → [Recommended entry A]: [one sentence why]
- I need strong security isolation
  → [Recommended entry B]: [one sentence why]
- I'm building for production scale
  → [Recommended entry C]: [one sentence why]
```

**Critical**: Every recommended entry must have a risk/tradeoff callout immediately after:
```markdown
→ Recommended: Entry A
  - Good for: [specific strength]
  - Watch out for: [specific limitation or risk]
```

### 4. Going deeper
Pointer to the full comparison (the generated README sections). Explain what the reader will find there and how to use the lens tables.

### 5. For [specialized audience] (if applicable)
Pointer to audience-specific docs. "If you're specifically interested in [aspect], see [doc]."

## Writing Principles

### Lead with what the reader needs
Not what's most impressive or most popular. A reader asking "which sandbox should I use?" needs a decision tree, not a feature comparison matrix.

### Order by fit, not fame
In the decision tree, the first option should be the best *fit for that scenario*, not the most well-known. If a lesser-known tool is the right answer for a use case, lead with it.

### Risk callouts are mandatory
Every recommendation must include what it *doesn't* protect against. This is non-negotiable. Examples:

**Good**: "Docker provides process isolation via namespaces and cgroups, but containers share the host kernel. A kernel exploit in the container can compromise the host. For untrusted code execution, consider VM-based isolation."

**Bad**: "Docker is a popular containerization tool." (No risk context.)

**Bad**: "Docker has some security limitations." (Too vague to act on.)

### Be specific and sourced
Generic statements erode trust. Compare:
- Generic: "This tool has good performance."
- Specific: "Benchmarks show ~2ms cold start time for sandboxed function execution (source: [link])."

### Don't oversell
If a tool is good but has rough edges, say so. Readers trust honest assessments more than enthusiastic recommendations. "This is the most capable option, but the setup documentation is sparse and you'll likely need to read the source" is more helpful than "This is the best choice."

## Audience-Specific Docs

When Phase 5 (Critique) identifies a specialized audience, create a separate doc in `docs/`.

Structure:
1. Who this doc is for (one sentence)
2. How this doc differs from the getting-started guide
3. The specialized content (research overview, deep comparison, risk analysis, etc.)
4. Pointers back to the main content for general context

## Common Pitfalls

- **Generating editorial from data**: The getting-started guide should read like it was written by someone who understands the reader's problem, not like a summary of the YAML entries.
- **Missing risk callouts**: This is the most common editorial failure. Check every recommendation.
- **Jargon in getting-started**: If the getting-started guide uses domain terms without definition, the least-technical audience is lost.
- **Stale editorial**: When entries change (especially recommended ones), the editorial must be updated to match. Generated content updates automatically; editorial doesn't.
