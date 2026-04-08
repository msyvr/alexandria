# Research Gathering Prompts

Templates for systematic research in Phase 2. Adapt to the specific domain.

## Tool/Product Landscape Research

### Initial broad search
```
Search for [topic] tools, products, and services. For each, capture:
- Name
- URL (primary: official site or GitHub repo)
- One-sentence description
- Open source? License?
- Who maintains it? (company, community, individual)
- Notable: any standout feature, limitation, or controversy

Sources to check:
1. GitHub: search "[topic]", "[topic] tool", "awesome-[topic]"
2. Product Hunt: search "[topic]"
3. Blog posts: "[topic] comparison", "best [topic] tools [year]"
4. HN: search "[topic]" on hn.algolia.com, sort by points
5. Reddit: r/[relevant-subreddit], search "[topic]"
```

### Gap-filling search
```
Given these existing entries: [list entries found so far]

Search for alternatives and competitors that might be missing:
1. "alternatives to [top entry]"
2. "[topic] for [specific use case not well covered]"
3. Check dependency graphs: what do existing entries depend on or integrate with?
4. Check adjacent spaces: [list 2-3 adjacent domains]
5. Non-English sources: are there tools popular in non-English-speaking communities?
```

### Sentiment and real-world usage
```
For each entry in [list], search for real-world usage reports:
1. GitHub issues: what do users complain about? What do they praise?
2. HN/Reddit comments: what's the community sentiment?
3. Blog posts: are there "I tried X and here's what happened" posts?
4. Stack Overflow: what problems do users hit?

Capture: common praise, common complaints, known limitations not in docs
```

## Research Domain Research

### Paper search
```
Search for papers on [topic]. For each, capture:
- Title
- Authors (first author + "et al." if >3)
- Organization
- Year
- Venue (conference/journal) or arXiv category
- URL (prefer DOI, then arXiv, then institutional page)
- Key finding in one sentence
- Method type: [define categories relevant to the domain]

Sources:
1. arXiv: search [relevant categories], keywords "[topic keywords]"
2. Semantic Scholar: search "[topic]", filter by year, sort by citations
3. Google Scholar: search "[topic]", check "cited by" for seminal papers
4. Conference proceedings: [list relevant venues]
5. Survey papers: search "survey [topic]", "review [topic]" — these map the landscape
```

### Organization and group tracking
```
Identify research groups and organizations active in [topic]:
1. Who published the most-cited papers?
2. Which orgs fund research in this area?
3. Are there dedicated research labs or centers?
4. Which companies have published in this space?

For each org: name, type (academic/industry/nonprofit/government), key publications, URL
```

### Area mapping
```
Map the sub-areas within [topic]:
1. What are the main research threads?
2. How do they relate to each other?
3. Which are active vs. dormant?
4. Which are converging or diverging?
5. Are there key open problems in each sub-area?

For each sub-area: name, description, key questions, active groups, seminal papers, current state
```

## Output Format

Use this consistent format for the research dump:

```markdown
# Research Dump: [Topic]
Date: [date]
Scope: [reference to scope document]

## Entries

### [Entry Name]
- URL: ...
- Type: tool | paper | org | method | area
- Category (tentative): ...
- Description: ...
- Notes: ...
- Source: where you found this

### [Entry Name]
...

## Gaps and Uncertainties
- [Things you couldn't find or verify]
- [Areas that seem underrepresented]
- [Entries you're unsure about including]
```
