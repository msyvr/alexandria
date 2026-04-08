# Phase 6: Automate

**Driver**: Claude Code
**Goal**: Set up discovery automation so the repo stays current without ongoing effort.

## Components

### 1. Discovery script (`scripts/discover.py`)
Searches configured sources for new entries that might belong in the repo. Outputs candidates for human review — never auto-adds entries.

See [discovery-patterns.md](../conventions/discovery-patterns.md) for source-specific patterns.

### 2. GitHub Actions workflow
Runs the discovery script on a schedule. Creates issues or PRs with candidates.

```yaml
# .github/workflows/discover.yml
name: Discover new entries
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday
  workflow_dispatch: {}

jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install pyyaml requests
      - id: discover
        run: python scripts/discover.py
      - name: Create issue if candidates found
        if: steps.discover.outputs.found == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            // Create issue with discovery candidates
```

### 3. Staleness checking
For existing entries, check signals of staleness:
- GitHub repos: last commit date, archive status, maintenance mode
- Products: HTTP status of URL, deprecation notices
- Papers: retraction notices (rare but important)

Flag stale entries for review — don't auto-remove.

### 4. Quarterly review nudge
A scheduled issue that prompts manual review:
- Are categories still the right groupings?
- Have any lenses become uninformative (>80% same value)?
- Are there new audiences that need specialized docs?
- Has the scope shifted in practice?

## Discovery Sources

### GitHub
- Search queries: topic keywords, `topic:` filter, language filters
- Minimum thresholds: star count (calibrate to the landscape — 10 stars means different things in different domains)
- Staleness: last commit >12 months + no releases = flag for review

### arXiv
- Category-based search (e.g., `cs.AI`, `cs.CR`, `cs.LG`)
- Keyword search within title/abstract
- Date-range filtering (last 30 days for weekly runs)

### Semantic Scholar
- Citation-based discovery: papers citing key entries
- Author tracking: new papers from prolific researchers in the space
- Venue filtering: specific conferences/journals

### General web
- Product Hunt, HN launches for tools
- Blog posts mentioning entries (backlink discovery)

## Key Guidance

- **Surface, don't decide**: Discovery outputs candidates. A human decides if they belong.
- **Start daily, move to weekly**: Daily catches things fast during initial setup. Once the landscape stabilizes, weekly is sufficient.
- **Tune thresholds**: Star minimums, citation counts, and date ranges should be calibrated to the specific landscape. A niche field with 5 relevant tools has different thresholds than a broad ecosystem.
- **Rate limits**: GitHub API has rate limits. Use authenticated requests and respect pagination. arXiv has a 3-second delay requirement between requests.
