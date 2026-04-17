## Discovery Patterns

Patterns for automated discovery of new entries and staleness detection. Used in Phase 6 (Automate) to build `scripts/discover.py`.

### GitHub Discovery

#### Search queries
```python
GITHUB_QUERIES = [
    # Direct topic search
    "topic:{topic}",
    # Keyword search
    "{keyword1} {keyword2}",
    # Awesome list mining
    "awesome-{topic}",
]
```

#### Filtering
- **Minimum stars**: Calibrate to the landscape. A niche domain might use 5 stars; a broad ecosystem might use 100. Start low, adjust upward if too many candidates surface.
- **Last updated**: Filter out repos with no commits in 24+ months (configurable). These are candidates for staleness, not discovery.
- **Language filter**: Optional. Some landscapes are language-specific.
- **Exclude forks**: Forks clutter results. Filter with `fork:false` in the GitHub search API.

#### Staleness signals
```python
STALE_THRESHOLDS = {
    "no_commits_months": 18,      # No commits in 18 months
    "archived": True,              # Repo archived
    "no_releases_months": 24,      # No releases in 24 months
}
```

#### Rate limits
- Unauthenticated: 10 requests/minute
- Authenticated: 30 requests/minute
- Use a personal access token. Store in environment variable, not in code.
- Paginate results (30 per page default, 100 max)

### arXiv Discovery

#### Category-based search
```python
ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CR"]  # Adapt to domain
ARXIV_KEYWORDS = ["keyword1", "keyword2"]
```

#### API usage
- Base URL: `http://export.arxiv.org/api/query`
- Respect the 3-second delay between requests
- Use `sortBy=submittedDate&sortOrder=descending` for recent papers
- Date range: `submittedDate:[YYYYMMDD TO YYYYMMDD]`

#### Filtering
- Keyword match in title or abstract
- Date range (last 30 days for weekly runs, last 7 for daily)
- Exclude papers already in the dataset (match by arXiv ID)

### Semantic Scholar Discovery

#### Citation-based discovery
Find papers that cite entries already in the dataset:
```python
# For each paper in entries.yaml with a Semantic Scholar ID or DOI
# GET /paper/{paper_id}/citations
# Filter by date, venue, and citation count
```

#### Author tracking
Track prolific authors in the space:
```python
# GET /author/{author_id}/papers
# Filter by date range
```

#### Venue filtering
Restrict to specific conferences/journals:
```python
VENUES = ["NeurIPS", "ICML", "ICLR", "ACL", "USENIX Security"]
```

#### Rate limits
- 100 requests per 5 minutes without API key
- 1000 requests per 5 minutes with API key
- Request a key at semanticscholar.org for production use

### General Web Discovery

#### Product Hunt
- Search by topic keyword
- Filter by launch date (recent)
- Useful for tool/product landscapes, not research

#### Hacker News
- Use hn.algolia.com API: `http://hn.algolia.com/api/v1/search`
- Search `Show HN` posts for new tools
- Filter by points (>10 for niche topics, >50 for broad topics)
- Filter by date

### Discovery Script Structure

```python
#!/usr/bin/env python3
"""Discover new candidates for [repo name]."""

import json
import os
import sys
from datetime import datetime, timedelta

import requests
import yaml

# --- Configuration ---
ENTRIES_FILE = "data/entries.yaml"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# ... source-specific config ...

def load_existing_entries():
    """Load current entries to avoid re-surfacing known items."""
    with open(ENTRIES_FILE) as f:
        data = yaml.safe_load(f)
    return {e["url"] for e in data["entries"]}

def search_github(existing_urls):
    """Search GitHub for new candidates."""
    candidates = []
    # ... implementation ...
    return candidates

def search_arxiv(existing_urls):
    """Search arXiv for new papers."""
    candidates = []
    # ... implementation ...
    return candidates

def check_staleness(entries):
    """Check existing entries for staleness signals."""
    stale = []
    # ... implementation ...
    return stale

def main():
    existing = load_existing_entries()
    
    candidates = []
    candidates.extend(search_github(existing))
    candidates.extend(search_arxiv(existing))
    
    stale = check_staleness(...)
    
    if candidates or stale:
        # Output for GitHub Actions to create an issue
        print(json.dumps({"candidates": candidates, "stale": stale}))
        # Set output for workflow
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("found=true\n")
    else:
        print("No new candidates or stale entries found.")
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("found=false\n")

if __name__ == "__main__":
    main()
```

### Key Principles

1. **Surface, don't decide**: Output candidates. A human reviews and accepts/rejects.
2. **Deduplicate against existing**: Always check if a candidate is already in entries.yaml.
3. **Respect rate limits**: Use authenticated requests, add delays, handle pagination.
4. **Fail gracefully**: If an API is down, log the error and continue with other sources. Don't let one broken source block all discovery.
5. **Configurable thresholds**: Star counts, date ranges, and keyword lists should be easy to adjust at the top of the file.
