# Phase 2: Research

**Driver**: Claude Code (user reviews for gaps)
**Goal**: Gather comprehensive data on the landscape.

## Prerequisites

**Web access**: This phase works best when Claude Code has web search and web fetch tools
available. With web access, the research covers current information — recent releases, new
papers, community discussions.

**Without web access**: Research draws on training data only. This still produces a useful
landscape but may miss recent developments. Be explicit with the user: "I'm researching from
my training knowledge, which has a cutoff. You can help by sharing URLs or pasting content
from recent sources you've found." The user providing seed URLs and recent articles
significantly improves coverage.

## Process

1. Use [research prompt templates](../prompts/research-gathering.md) to systematically search
2. Output a raw research dump (a temp file, like `temp/research-dump.md`)
3. User reviews for gaps: "what about X?" / "you missed Y"

## Research Sources by Domain Type

### Tool/product landscapes
- GitHub: search by topic, keyword, awesome-lists in adjacent spaces
- Product pages and documentation
- Blog posts, benchmarks, comparisons
- HN/Reddit/Discord discussions (surface sentiment and real-world usage reports)
- Conference talks and demos

### Research domains
- arXiv: category-based and keyword search
- Semantic Scholar: citation graphs, author tracking, venue filtering
- Conference proceedings (NeurIPS, ICML, ACL, USENIX, etc.)
- Org publications (research labs, policy institutes)
- Survey papers (these are gold — they've already done landscape mapping)

## Key Guidance

### Cast wide initially
Inclusion criteria tighten in Phase 3 (Structure). At this stage, include anything that *might* belong. It's cheaper to cut entries during structure than to re-research during build.

### Capture editorial context during research
Don't just list entries — capture *why* something matters while you're reading about it. Notes like "this is the only option that runs on bare metal" or "controversial due to [CVE]" are hard to reconstruct later.

### Record sources
Every entry should have a URL. For research papers, capture DOI/arXiv ID. These become the `url` field and support verification.

### Structured output format
Use a consistent format for the research dump so it's parseable in Phase 3:

```markdown
## [Entry Name]
- URL: ...
- Type: tool / paper / org / method
- Description: 1-2 sentences
- Notes: editorial context, why it matters, caveats
- Source: where you found this
```

## Common Pitfalls

- **Brand-recognition bias in research**: You'll find Docker and AWS first because they're mentioned most. Actively search for smaller/newer alternatives. In awesome-agent-sandboxes, nono (a lightweight container alternative) was initially missed despite being highly relevant.
- **Recency bias**: Don't dismiss older tools/papers that are still actively used. Don't privilege newer entries just because they have recent blog posts.
- **Stopping too early**: If your first search pass returns 8 entries for a landscape that should have 20+, you haven't searched broadly enough. Try different keywords, check "alternatives to X" pages, look at dependency graphs.
- **Missing adjacent spaces**: Agent sandboxes overlaps with container runtimes, VM managers, and WASM runtimes. Research adjacent categories — some entries will belong, others won't, but you need to check.
