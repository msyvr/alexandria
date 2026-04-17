## Schema Design Prompt

Use after Phase 2 (Research) to design the YAML schema for Phase 3 (Structure).

### Process

#### 1. Review the research dump
Read all entries. Identify:
- What information is available for most entries?
- What information varies meaningfully between entries?
- What information is the same for most entries (and therefore not useful as a field)?

#### 2. Identify core fields
Every entry needs these regardless of domain:
- `name`: Display name
- `category`: Which section it belongs in
- `url`: Primary link
- `description`: One-sentence summary

#### 3. Identify domain fields
Fields specific to the landscape type. Ask:
- What does a reader need to compare entries?
- What would a reader filter by?
- What information is hard to find without this repo?

**Test**: For each proposed field, check 5 entries from the research dump. Can you fill it in with meaningful, varying values? If not, the field doesn't earn its place.

#### 4. Identify lens fields
Controlled-vocabulary fields for cross-cutting views. See [lens-design.md](lens-design.md).

#### 5. Decide on notes
The `notes` field is free text, nullable. It holds per-entry editorial context that doesn't fit structured fields. Not every entry needs notes, but entries with important caveats should have them.

### Schema Patterns

See [yaml-schema-patterns.md](../conventions/yaml-schema-patterns.md) for detailed patterns by domain type.

#### Tool landscape
```yaml
entries:
  - name: string (required)
    category: string (required, from controlled list)
    url: string (required)
    description: string (required)
    maintainer: string (required)
    open_source: boolean (required)
    license: string (optional, null if not open source)
    # domain-specific fields
    capabilities: list[string] (optional)
    requirements: list[string] (optional)
    limitations: list[string] (optional)
    # lens tags
    lens_1: string (required, from controlled vocabulary)
    lens_2: string (required, from controlled vocabulary)
    # editorial
    notes: string (optional)
```

#### Research tracking
```yaml
papers:
  - title: string (required)
    authors: string (required, "First Author et al." for >3)
    org: string (required)
    year: integer (required)
    url: string (required)
    venue: string (optional)
    area: string (required, from controlled list)
    method_type: string (required, from controlled vocabulary)
    key_finding: string (required)
    notes: string (optional)
```

### Presenting to the User

When proposing the schema in Phase 3:
1. Show the schema with one example entry fully populated
2. Explain each field in one sentence
3. Highlight which fields are lens tags and what they enable
4. Ask: "Any fields that seem unnecessary? Any information you'd want that's missing?"

Don't ask about YAML formatting, field naming conventions, or Python implementation. Ask about whether the schema captures the right information.
