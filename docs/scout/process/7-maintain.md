# Phase 7: Maintain

**Driver**: User (automation-assisted)
**Goal**: Keep the repo useful over time.

## Ongoing Activities

### Weekly (or when convenient)
- **Review discovery candidates**: Check issues/PRs created by the discovery workflow. Accept, reject, or defer.
- **Handle community contributions**: If the repo is public, PRs may come in. Evaluate against the scope and schema.

### Quarterly (or when the nudge issue appears)
- **Lens review**: Are the lenses still useful? Has any lens collapsed to mostly one value? Should a new perspective be added?
- **Category review**: Has the landscape shifted enough that categories need restructuring?
- **Staleness review**: Are flagged entries actually stale, or just stable? Remove archived/dead projects, update descriptions for those that have evolved.
- **Audience review**: Has a new audience emerged that needs a specialized doc?

### As-needed
- **Add specialized docs**: The safety research doc in awesome-agent-sandboxes came from a user question, not upfront planning. Let audience needs drive new docs.
- **Re-run critique**: After significant changes (10+ entries added, category restructure), re-run the [critique checklist](../prompts/critique-checklist.md).
- **Update editorial**: If the getting-started guide recommends tools that have been superseded, update it. Editorial content is hand-maintained, not auto-generated.

## The Repo Stays Useful Without Active Maintenance

The automation in Phase 6 handles discovery and staleness detection. If the maintainer goes quiet for a few months:
- Discovery issues accumulate but don't break anything
- The README remains accurate for existing entries
- Staleness flags surface but don't auto-remove

The worst case for neglect is "slightly outdated," not "broken." This is intentional — a curated repo should degrade gracefully.

## When to Archive

A landscape repo has run its course when:
- The domain has consolidated to 1-2 dominant options (no need for a comparison)
- The domain has become so broad that a single repo can't cover it (time to split)
- The maintainer has moved on and no successor is interested

Archive clearly: add a note to the README, stop the discovery workflow, leave the content up. Stale-but-readable is better than deleted.
