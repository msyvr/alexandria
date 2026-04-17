## Example: Building an AI Safety Research Scout

A hypothetical walkthrough showing how the scout process adapts for research-domain monitoring (as opposed to tool/product landscapes).

### How This Differs from a Tool Landscape

| Aspect | Tool landscape | Research scout |
|--------|---------------|-----------------|
| Entity type | Tools, products, services | Papers, methods, areas, orgs |
| Primary source | GitHub, product pages | arXiv, Semantic Scholar, conferences |
| Schema focus | Capabilities, requirements | Findings, methods, citations |
| Lenses | Isolation strength, deployment | Research area, method type, maturity |
| Discovery | GitHub stars, new repos | New papers, citation alerts |
| Maintenance | URL staleness, archive status | Retraction notices, follow-up papers |

### Phase 1: Scope

**Scope dialog**:
- Topic: AI safety research — the study of risks from advanced AI systems and techniques for making AI systems safer
- In scope: Technical research (alignment, interpretability, robustness, evaluation). Policy-relevant technical work.
- Out of scope: AI ethics broadly (too wide), AI governance policy (different audience), AI capabilities research (unless directly safety-relevant)

**Audiences**:
1. Researchers entering the field: "What are the active research threads? Where should I start reading?"
2. Practitioners: "What safety techniques can I apply to my models today?"
3. Research managers: "Which organizations are active? What's the state of each sub-area?"

**Triage questions**:
- What area of safety does this relate to? (alignment, interpretability, robustness, evaluation, governance-adjacent)
- What type of contribution is it? (theoretical framework, empirical result, benchmark/dataset, survey)
- How mature is this line of work? (emerging, active, established)

### Phase 2: Research

#### Sources
- **arXiv**: cs.AI, cs.LG, cs.CL with safety-related keywords
- **Semantic Scholar**: Citation graphs from seminal papers (Constitutional AI, RLHF, etc.)
- **Conference proceedings**: NeurIPS, ICML, ICLR safety workshops; AAAI AI Safety workshop
- **Org publications**: Anthropic, DeepMind, OpenAI, MIRI, ARC, Redwood Research, Alignment Forum
- **Survey papers**: "Survey of AI alignment" type papers that map the landscape

#### Research dump structure
```markdown
### Constitutional AI: Harmlessness from AI Feedback
- URL: https://arxiv.org/abs/2212.08073
- Type: paper
- Area (tentative): alignment
- Method type: training technique
- Key finding: AI feedback can replace human feedback for harmlessness training
- Notes: Foundational for RLHF alternatives. Heavily cited. From Anthropic.
- Source: arXiv, cited by multiple survey papers
```

### Phase 3: Structure

#### Schema decision: Hybrid (areas + papers)

The user wants both "navigate the field" (area-centric) and "find specific papers" (paper-centric). Hybrid schema:

```yaml
areas:
  - id: "alignment"
    name: "Alignment"
    description: "Techniques for ensuring AI systems pursue intended goals."
    key_questions:
      - "Can we specify human values precisely enough for optimization?"
      - "Does RLHF scale to superhuman systems?"
    active_orgs: ["Anthropic", "DeepMind", "OpenAI", "MIRI"]
    current_state: "active"
    notes: "The broadest and most active sub-area."

papers:
  - id: "constitutional-ai"
    title: "Constitutional AI: Harmlessness from AI Feedback"
    authors: "Bai et al."
    org: "Anthropic"
    year: 2022
    url: "https://arxiv.org/abs/2212.08073"
    venue: "arXiv"
    area_id: "alignment"
    method_type: "training-technique"
    contribution_type: "empirical"
    maturity: "established"
    key_finding: "AI feedback can replace human feedback for harmlessness training."
    notes: "Foundational paper for RLAIF approaches."
```

#### Lenses
1. **Area**: alignment, interpretability, robustness, evaluation, governance-adjacent
2. **Contribution type**: theoretical, empirical, benchmark-dataset, survey
3. **Maturity**: emerging (< 2 years, few follow-ups), active (ongoing work, growing citations), established (widely adopted, foundational)

#### Critique checkpoint findings

**Mixed entity types**: Initial proposal had papers and methods as a single entity. Split: papers describe methods, but a method (like RLHF) can span many papers. Track both, cross-reference.

**Area overlap**: "Alignment" was too broad — nearly half the papers fell into it. Split into "alignment-training" (RLHF, Constitutional AI) and "alignment-theory" (value specification, corrigibility). Checked distribution: now roughly even.

**Maturity lens variance**: Initially proposed "established" for papers with >100 citations. But citation counts vary wildly by sub-area and year. Redefined: "established" means the idea is widely adopted in practice or subsequent research, not just cited.

### Phase 4: Build

#### Generate script adaptations
- Two entity types (areas and papers) means two validation passes and two sets of generated tables
- Area pages link to their papers; paper tables link back to areas
- Lens tables work on papers (not areas — areas don't have method_type or contribution_type)

#### Editorial content
- Getting-started: "What is AI safety research?" → "Active research threads" → "Where to start reading" → "For practitioners: techniques you can apply today"
- Decision tree: "What's your background?" (ML researcher → area overview; practitioner → applied techniques; new to the field → survey papers and primers)

#### Risk callouts (adapted for research)
Instead of "what this tool doesn't protect against," risk callouts for research are:
- "This technique has been demonstrated at scale X but not scale Y"
- "This result assumes [assumption] which may not hold for [context]"
- "No independent replication yet"

### Phase 5: Critique

#### Likely findings (based on common patterns)

**Org bias**: Research from well-known labs (Anthropic, DeepMind) will be overrepresented because they publish more and are cited more. Actively search for work from smaller labs, academic groups, and independent researchers.

**Recency bias**: Recent papers are easier to find. Seminal older work (pre-2020) may be underrepresented. Include foundational papers even if they predate the current publication wave.

**Method hype**: New techniques (e.g., a novel interpretability method) get attention before they're validated. The maturity lens should accurately reflect this — "emerging" is not a negative, but readers should know.

**Missing practitioners**: If the audience includes practitioners, check: does the editorial content actually point to *applicable* techniques, or just to research papers? A practitioner needs "how to apply RLHF" pointers, not just the original paper.

### Phase 6: Automate

#### Discovery sources
- **arXiv**: Daily search for new papers in cs.AI, cs.LG with safety keywords
- **Semantic Scholar**: Weekly citation alerts for papers already in the dataset
- **Author tracking**: New papers from researchers who've published 3+ papers in the dataset

#### Staleness
- Papers don't go stale the way tools do. But areas can shift:
  - "Current state" field may need updating (active → dormant, or split into sub-areas)
  - Quarterly review nudge focuses on area accuracy, not individual papers

### Key Differences from Tool Landscapes

1. **Schema is hybrid** (multiple entity types, cross-referenced) rather than flat
2. **Discovery leans on citation graphs** rather than GitHub searches
3. **Staleness is about field evolution**, not project maintenance
4. **Risk callouts are about research validity**, not security properties
5. **Editorial leads with "how to navigate the field"**, not "which tool to pick"
