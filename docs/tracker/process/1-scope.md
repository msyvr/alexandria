# Phase 1: Scope

**Driver**: User
**Goal**: Establish what the repo covers and who it's for.

## Why This Phase Matters

Scope drift mid-build is expensive. The awesome-agent-sandboxes repo started as "coding agent sandboxes" and broadened to "any agent type" after user clarification. That shift affected categories, entries, and editorial framing. Getting scope right early saves rework.

## Dialog with the User

Ask about direction, not details. The user shouldn't need to think about YAML fields or Python code structure — they should think about what the repo covers and who reads it.

### Questions to ask:

1. **Topic**: What's the landscape? What's in scope, what's out?
   - "Agent sandboxes" vs "coding agent sandboxes" vs "secure execution environments" are very different scopes
   - Explicit exclusions help as much as inclusions

2. **Audiences**: Who will use this repo? Different audiences need different content.
   - awesome-agent-sandboxes had two: beginners (need a getting-started guide) and technical users (need comparison data)
   - A research tracker might serve practitioners, policymakers, and journalists differently

3. **Perspectives**: What questions does a reader bring?
   - Not "what are the YAML fields" but "what does someone want to triage by?"
   - Examples: "Is this open source?", "Does it run locally?", "What's the security model?", "How mature is this?"

4. **Seed entries**: Any known entries to start the research?
   - Seed entries anchor the research and help calibrate scope
   - "I know about Docker, Firecracker, and E2B" immediately tells you the scope level

## Output

A scope document — can be informal, in a temp file — that anchors all subsequent work:

```markdown
# Scope: [topic]

## Coverage
- In scope: ...
- Out of scope: ...

## Audiences
- [Audience 1]: needs ...
- [Audience 2]: needs ...

## Triage questions
- [Question 1]
- [Question 2]
- ...

## Seed entries
- [Entry 1]
- [Entry 2]
- ...
```

## Common Pitfalls

- **Scope too broad**: "AI tools" is a repo that never ships. Narrow to something a reader can scan in one sitting.
- **Scope too narrow**: "Python sandboxes for coding agents on macOS" might have three entries. Broaden if the landscape is thin.
- **Missing audience**: If you can't name who reads this, the editorial content will lack direction.
- **Skipping this phase**: Jumping straight to research feels productive but leads to rework when the user says "that's not what I meant."
