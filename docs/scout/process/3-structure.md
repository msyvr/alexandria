## Phase 3: Structure

**Driver**: Collaborative (this is where most user dialog happens)
**Goal**: Design the schema, perspectives (lenses), and categories.

### Process

#### 1. Propose a schema
Present the research dump and propose a YAML schema. The user pushes back on fields that don't earn their keep.

See [yaml-schema-patterns.md](../conventions/yaml-schema-patterns.md) for schema patterns by domain type.

#### 2. Propose cross-cutting perspectives (lenses)
Lenses are controlled-vocabulary fields that enable readers to triage entries from different angles. Propose 2-4 lenses based on the triage questions from Phase 1.

See [lens-design.md](../prompts/lens-design.md) for guidance.

**Key test**: Would a reader actually filter by this? If a lens tag has >80% of entries sharing the same value, it's not useful. (In awesome-agent-sandboxes, `status: active` was true for nearly every entry — it didn't help anyone triage.)

#### 3. Propose categories
Categories group entries into sections. The user tests: "does this grouping match how I think about the landscape?"

**Key test**: Write a one-sentence inclusion test for each category, then test every entry against the *definition*, not the *name*.

### Built-in Critique Checkpoint

Before leaving this phase, check:

- [ ] **Definition vs. name**: Test every entry against its category's one-sentence definition. In awesome-agent-sandboxes, "Docker Sandboxes" entries were miscategorized because the category *name* suggested Docker-based tools, but the *definition* was broader. Entries matched the name but not the definition.

- [ ] **Mixed classification axes**: Do categories mix different grouping principles? E.g., grouping by technology (containers, VMs) and by use case (CI/CD, development) in the same taxonomy creates ambiguity.

- [ ] **Single-entry categories**: A category with one entry is usually a classification smell. Either the entry belongs elsewhere or the category needs a broader definition.

- [ ] **General vs. domain-specific**: Are general-purpose tools clearly distinguished from domain-specific ones? In awesome-agent-sandboxes, Koyeb (a general cloud platform with sandbox features) sat alongside NanoClaw (purpose-built for agent sandboxing). Readers need to know the difference.

- [ ] **Bundled entries**: Should any entry be split? Wasmtime, WasmEdge, and wasmCloud are separate projects with different maintainers and architectures — they shouldn't be a single entry just because they all use WASM.

- [ ] **Lens value distribution**: Any lens where >80% of entries share one value? Drop the lens or rethink the vocabulary.

### Dialog with the User

Present your proposed schema, lenses, and categories together. Ask for feedback on:
- "Are these the right categories? Does this match how you'd group these?"
- "Would you actually triage by [lens]? Is [lens] missing?"
- "Any fields that seem unnecessary? Any missing?"

Don't ask about implementation details (field naming conventions, YAML formatting). Do ask about whether the structure captures the right information and groupings.

### Output

Agreed schema, lens definitions, and category taxonomy — documented clearly enough that Phase 4 can build from them without ambiguity.
