## Working with scouts

A scout is a living knowledge base that monitors a domain — it's the one item type in your collection that actively updates itself. This guide covers the scout lifecycle: creating one, maintaining it, and eventually settling it into a static reference when you're done.

### When to use a scout

Scouts are useful when:
- A topic is **complex** enough to need careful organization (many entries, categories, comparisons)
- The topic is **personal** enough that no generic tool fits (your specific questions, your specific constraints)
- The landscape is **evolving** fast enough that a static reference goes stale

Most items in your collection are static (physical items, imported digital content). Scouts are the moving ones — more effort to create and maintain, and the fullest expression of what the collection enables: a resource on a subject you care about, built and owned by you rather than subscribed to from someone else.

### Creating a scout

From your collection directory:

```
cd ~/my-collection
claude
```

Then type `/coll-new-scout` and describe what you want to monitor. Claude guides you through a seven-phase process:

1. **Scope** — what's in, what's out, who is this for
2. **Research** — Claude gathers data on the landscape
3. **Structure** — design the schema, categories, and comparison angles
4. **Build** — create the data files, editorial content, and scripts
5. **Critique** — systematic self-review for errors and bias
6. **Automate** — set up discovery of new developments
7. **Maintain** — ongoing updates (this phase continues after the build)

The first build takes one session for a small topic (10-20 entries) or a few sessions for a larger one (40+).

### Where the scout lives

After creation, the scout is a directory inside your collection:

```
my-collection/
└── research/
    └── ai-safety-scout/       ← the scout
        ├── metadata.yaml       ← catalog entry
        ├── README.md           ← generated overview
        ├── CLAUDE.md           ← operational context for Claude
        ├── data/
        │   └── entries.yaml    ← all structured data
        ├── docs/
        │   └── getting-started.md
        ├── scripts/
        │   ├── generate_readme.py
        │   └── discover.py
        └── context.md          ← interaction history (created after first use)
```

The scout is its own git repo — it tracks its changes independently from the rest of your collection.

### Working on a scout

#### Quick operations (from the collection directory)

For brief tasks, you can work on the scout from your collection directory. Claude can read and write any file in the scout's directory from there. Examples:

- Check how many entries the scout has
- Add a single new entry
- Ask a question about the scout's data ("what does my scout say about treatment X?")
- Settle the scout (freeze it as a static reference)

#### Focused work (from the scout's directory)

For substantial work, it's better to start Claude Code from the scout's own directory. This gives Claude the scout's operational context automatically:

```
cd ~/my-collection/research/ai-safety-scout
claude
```

From here, Claude automatically loads the scout's `CLAUDE.md` (which describes the schema, update commands, and file locations). This makes focused work smoother:

- Running the critique checklist
- Adding many new entries at once
- Restructuring categories or lenses
- Running discovery and reviewing candidates
- Updating editorial content

**Tip**: use terminal tabs to keep both sessions open. One tab for the collection, one for the scout. See the [terminal basics guide](terminal-basics.md) for how to use tabs.

#### The /coll-* commands work from inside the scout

Because the scout directory is inside the collection, and Claude Code looks in parent directories for skills, all `/coll-*` commands are available even when you start from the scout directory. You can run `/coll-menu`, `/coll-notes`, or any other collection command without switching back to the collection root.

### Maintaining a scout

#### Discovery

If the scout has a discovery script (`scripts/discover.py`), it searches configured sources for new entries that might belong in the scout. Run it:

```
python scripts/discover.py
```

Discovery outputs **candidates** — it never auto-adds entries. You review each candidate and decide whether to include it.

If the scout has a GitHub Actions workflow set up, discovery runs automatically on a schedule and creates issues or PRs with candidates for your review.

#### Adding entries

To add new entries to the scout, edit `data/entries.yaml` (or ask Claude to add them). After adding entries, regenerate the README:

```
python scripts/generate_readme.py
```

#### Re-running critique

After significant changes (10+ entries added, categories restructured), it's worth re-running the critique checklist. From the scout's directory, ask Claude to "run the critique checklist on this scout." The checklist catches:

- Entries that match a category name but not its definition
- Brand-recognition bias in ordering
- Missing risk/tradeoff callouts
- Entries that should be split or don't fit the scope
- Schema fields that aren't carrying useful information

### Settling a scout

At some point, a scout may have served its purpose. The landscape has stabilized, or you've made the decisions you needed to make, or you've moved on to other priorities. **Settling** freezes the scout as a static reference.

From your collection directory, use `/coll-menu` → settle-scout (or ask Claude directly). Settling:

- Sets `settled: true` in the scout's `metadata.yaml`
- Stops any discovery automation
- Preserves all content as-is
- Changes the wiki rendering: settled scouts show their content inline (like other static items) instead of linking out

A settled scout is just another static item in your collection from that point forward. If you later want to resume updates, you can edit `metadata.yaml` to set `settled: false` and re-enable discovery.

#### Short-lived vs. long-lived scouts

Some scouts are **short-lived**: built for an immediate decision (choosing a treatment, evaluating tools for a project), updated for a few weeks, then settled once the decision is made.

Some scouts are **long-lived**: monitoring an evolving field indefinitely (AI safety research, regulatory changes, emerging treatments for a chronic condition).

Both are valid. The decision to settle is yours — the scout keeps working until you say stop.

### Importing an existing scout

If you built a scout independently (outside any collection), you can import it:

```
/coll-scout
```

This imports the scout into your collection: moves or copies the directory, ensures it has the right metadata, updates the collection index, and regenerates the wiki. See the skill for details.
