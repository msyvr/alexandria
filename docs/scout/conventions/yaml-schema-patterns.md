# YAML Schema Patterns

Reusable schema patterns for different domain types. Choose and adapt based on the landscape.

## Tool/Product Landscape

For repos tracking tools, products, services, or libraries.

```yaml
entries:
  - name: "Tool Name"                    # Required. Display name.
    category: "Category Name"            # Required. From controlled list.
    url: "https://..."                   # Required. Primary link.
    description: "One sentence."         # Required. What it is.
    maintainer: "Org or person"          # Required. Who maintains it.
    open_source: true                    # Required. Boolean.
    license: "Apache-2.0"               # Optional. Null if not open source.
    # Domain-specific (choose what fits)
    capabilities:                        # Optional. What it can do.
      - "capability 1"
      - "capability 2"
    requirements:                        # Optional. What it needs.
      - "requirement 1"
    limitations:                         # Optional. What it can't do.
      - "limitation 1"
    # Lens tags (2-4 controlled vocabulary fields)
    isolation_level: "container"         # Example lens.
    deployment: "local"                  # Example lens.
    # Editorial
    notes: "Context about this entry."   # Optional. Free text.
```

### When to use
- Comparing tools that solve similar problems
- "Awesome list" style repos with structured data
- Decision-support repos ("which X should I use?")

### Common domain fields
| Field | Type | Use when |
|-------|------|----------|
| `capabilities` | list[string] | Entries do different things |
| `requirements` | list[string] | Setup varies between entries |
| `limitations` | list[string] | Readers need to know constraints |
| `language` | string | Implementation language matters |
| `pricing` | string | Mix of free and paid options |
| `last_release` | string (date) | Maintenance status matters |

## Research/Paper Tracking

For repos tracking academic papers, methods, or research areas.

### Paper-centric schema
```yaml
papers:
  - title: "Paper Title"                # Required.
    authors: "First Author et al."      # Required. Abbreviate if >3.
    org: "Organization"                 # Required. Primary affiliation.
    year: 2025                          # Required.
    url: "https://arxiv.org/..."        # Required. Prefer DOI > arXiv > institutional.
    venue: "NeurIPS 2025"              # Optional. Conference/journal.
    area: "Area Name"                   # Required. From controlled list.
    method_type: "Type"                 # Required. From controlled vocabulary.
    key_finding: "One sentence."        # Required. Main result.
    notes: "Why this matters."          # Optional.
```

### Area-centric schema
```yaml
areas:
  - name: "Area Name"                   # Required.
    description: "What this area is."   # Required. 2-3 sentences.
    key_questions:                       # Required. Open research questions.
      - "Question 1"
      - "Question 2"
    active_orgs:                         # Optional. Who's working on this.
      - "Org 1"
    seminal_papers:                      # Optional. Foundational references.
      - title: "Paper"
        url: "https://..."
    current_state: "Active/Dormant/Converging"  # Required. From vocabulary.
    notes: null                          # Optional.
```

### Hybrid schema
When you need both papers and areas, use separate top-level keys with cross-references:

```yaml
areas:
  - id: "area-safety"
    name: "AI Safety"
    # ...

papers:
  - id: "paper-constitutional-ai"
    title: "Constitutional AI"
    area_id: "area-safety"             # Cross-reference to area
    # ...
```

### When to use which
- **Paper-centric**: The landscape is defined by publications. Readers want to find papers.
- **Area-centric**: The landscape is defined by research threads. Readers want to understand the field.
- **Hybrid**: Both — readers want to navigate areas and find specific papers within them.

## Schema Design Principles

### Every field must earn its place
If a field has the same value for >80% of entries, it's noise. Drop it or fold it into notes.

### Required vs. optional
A field is required only if *every* entry can reasonably have a meaningful value. If you'd frequently write "N/A" or "unknown," make it optional.

### Controlled vocabularies are small
3-6 values for lens fields. If you need more, the field is probably a free-text field or two separate fields.

### Lists over booleans for capabilities
`capabilities: ["gpu", "networking", "filesystem"]` is more informative and extensible than `has_gpu: true, has_networking: true, has_filesystem: true`.

### Notes are nullable free text
Not every entry needs notes. But entries with important context — caveats, controversies, tradeoffs — should use them. Don't force notes on entries that don't need them.
