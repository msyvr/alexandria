## Example: Building awesome-agent-sandboxes

An honest walkthrough of how the awesome-agent-sandboxes repo was built using this process — including the mistakes and what the critique cycles caught.

### Phase 1: Scope

**Initial scope**: "Coding agent sandboxes" — environments that isolate AI coding agents from the host system.

**Scope broadened**: After user discussion, expanded to "any agent type," not just coding agents. This was the right call — the sandbox landscape doesn't split cleanly along agent-type lines. A Firecracker microVM works for coding agents and RL training agents alike.

**Audiences identified**:
1. Beginners: "I have an AI agent and I need it to run code safely. Where do I start?"
2. Technical users: "I know about containers and VMs. I need to compare options by isolation strength, deployment model, and setup effort."

**Triage questions**:
- How strong is the isolation? (process-level vs. container vs. VM vs. hardware)
- How much work to get started? (zero-config vs. install a tool vs. assemble from parts)
- Where does it run? (built into an agent vs. cloud vs. local vs. self-hosted)

**Seed entries**: Docker, Firecracker, E2B, gVisor, Modal

### Phase 2: Research

Research gathered 48 entries across the sandbox landscape. Sources included GitHub topic searches, product pages, blog posts, HN discussions, and academic references for VM/container isolation.

**What went well**: Casting wide caught entries like nono (lightweight container alternative), Seatbelt and Landlock (OS primitives), and several WASM runtimes that wouldn't appear in a narrow "coding sandbox" search.

**What was initially missed**: nono was found but initially given less attention than better-known alternatives. The gap-filling search ("alternatives to Docker for lightweight isolation") helped surface it properly.

### Phase 3: Structure

#### Schema
```yaml
entries:
  - name: string
    category: string
    maintainer: string
    open_source: boolean
    isolation_type: list[string]      # What isolation mechanisms it uses
    capabilities: list[string]
    requirements: list[string]
    limitations: list[string]
    isolation_tier: string            # Lens: strength of isolation
    adoption_effort: string           # Lens: how hard to get started
    deployment_model: string          # Lens: where it runs
    notes: string (nullable)
```

#### Lenses (3 cross-cutting views)
1. **Isolation Tier**: hardware-vm → microvm → container/user-space-kernel → process-level → wasm/language-runtime
2. **Adoption Effort**: zero-config → sign-up-for-service → install-a-tool → compose-building-blocks
3. **Deployment Model**: built-into-agent → cloud-managed → local → self-hosted → kubernetes

#### Categories (9, in two groups)

**Products & Services**: cloud-managed, agent-integrated, standalone, kubernetes, dev-environment

**Building Blocks**: abstraction, vm-runtime, os-primitive, wasm-runtime

#### What the critique checkpoint caught (before leaving Phase 3)

**Mixed classification axes**: The initial category proposal mixed "by technology" and "by deployment model." The final taxonomy separated Products & Services (by how you access them) from Building Blocks (by what they are). This was a significant restructure that happened *during* Phase 3, not after.

**General vs. purpose-built**: Koyeb (general cloud platform) and NanoClaw (purpose-built for agent sandboxing) were initially in the same category. The `agent-integrated` vs. `cloud-managed` distinction resolved this.

### Phase 4: Build

Built `data/sandboxes.yaml` (48 entries), `docs/getting-started.md`, `docs/safety-research.md`, `scripts/generate_readme.py`, and the discovery pipeline.

**Key design decisions**:
- Schema and lens definitions are Python constants in generate_readme.py, not a config file
- getting-started.md leads with "what sandboxing protects against" (5 threat categories), not with a product comparison
- safety-research.md was created for a specialized audience (security researchers, RL safety teams)

### Phase 5: Critique

Three critique passes, each producing material improvements.

#### Pass 1: Category misassignment and brand bias

**Finding**: "Docker Sandboxes" entries were categorized based on the category *name* (they use Docker), not the category *definition* (purpose-built sandbox environments using Docker as a runtime). Some entries were Docker-based tools that happened to provide isolation, not purpose-built sandboxes.

**Fix**: Retested every entry against a one-sentence inclusion test for its category. Moved misassigned entries.

**Finding**: Docker-based solutions were listed prominently in recommendations despite not being the strongest isolation option — because Docker is the most recognized brand.

**Fix**: Reordered getting-started recommendations by isolation strength and fit for purpose, not brand recognition.

#### Pass 2: Bundled entries and missing distinctions

**Finding**: Wasmtime, WasmEdge, and wasmCloud were treated as a single "WASM runtimes" entry. But they're separate projects with different maintainers, different architectures, and different capabilities.

**Fix**: Split into three separate entries, each with its own description, notes, and lens tags.

**Finding**: General-purpose tools (Koyeb, Railway) sat alongside purpose-built sandbox tools without distinction. A reader couldn't tell which was designed for sandboxing vs. adapted from a general platform.

**Fix**: Notes field for general-purpose entries explicitly states "general-purpose platform with sandbox capabilities, not purpose-built for agent isolation."

#### Pass 3: Underpromotion and missing docs

**Finding**: nono (a lightweight, security-focused container alternative) was buried in a long category list despite being highly relevant for users who prioritize security and simplicity. Brand-recognition bias in ordering.

**Fix**: Promoted nono in the getting-started guide's security-focused recommendation path.

**Finding**: Security-focused readers needed a different framing than the getting-started guide provided. The threat model for RL training sandboxes is different from the threat model for coding agent sandboxes.

**Fix**: Created `docs/safety-research.md` — a dedicated doc covering three research contexts (RL training, capability evaluation, adversarial red-teaming) with threat models and sandbox recommendations per context.

### Phase 6: Automate

Discovery script searches GitHub for new sandbox tools (topic search, keyword search, "awesome-sandbox" list mining). Staleness checking flags repos with no commits in 18+ months.

### Lessons Encoded in the Tracker Process

| Lesson | Where it's encoded |
|--------|-------------------|
| Test entries against category definitions, not names | critique-checklist.md, process/3-structure.md |
| Don't order by brand recognition | critique-checklist.md, editorial-writing.md |
| Split bundled entries | critique-checklist.md |
| Distinguish general-purpose from purpose-built | critique-checklist.md |
| Check lens value distribution | lens-design.md, critique-checklist.md |
| Create specialized docs when audience needs differ | critique-checklist.md, process/5-critique.md |
| Risk callouts for every recommendation | editorial-writing.md, critique-checklist.md |
| Editorial content is hand-written | process/4-build.md, editorial-writing.md |
