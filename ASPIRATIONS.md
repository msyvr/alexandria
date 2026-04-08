# Project Aspirations

## The core idea

alexandria helps people build and organize personal curated libraries — collections of structured, living resources on topics that matter to them. A health condition they're navigating. A professional field they're entering. A fast-moving situation they need to monitor. Their own creative and professional output.

The tool is AI-assisted — Claude Code does the research, organization, and self-critique work. The user drives direction: what to cover, who it's for, what questions matter. The result is a library the user owns, understands, and controls.

## The gap this fills

There's a growing spectrum of AI-assisted tools, but a meaningful gap in the middle:

| Approach | What you get | What's missing |
|----------|-------------|----------------|
| Download an app | Convenience | No control, no understanding, no ownership of your data |
| "Vibe code" with AI | A working artifact | You can't evaluate, maintain, or trust what was built |
| Learn to program | Full control | Unrealistic time investment for most professionals |

The gap is between "AI builds it for me" (where you have an artifact you don't understand) and "I build it myself" (where the barrier is years of skill acquisition). alexandria occupies the middle: **AI does the technical implementation, but the process is designed so the user understands every part of the result.**

The user doesn't need to learn how to build the tool. They need to learn how to evaluate and direct — enough technical literacy to know what matters (security, data ownership, correctness) without needing to know how to implement it. That's a much smaller surface area than "learn to code" and a much more valuable one for a busy professional.

## Who this is for

The target user is thorough, motivated, and has a real need. They might be a clinician, a graduate student, an economist, a journalist, an engineer — or someone navigating a complex personal situation. What they have in common: they'll follow a thorough process, they're motivated by a specific need, and they'd maintain a resource if they understood how.

Some users are software engineers who don't want to build the scaffolding from scratch. Some have never opened a terminal. Both want the same thing: a structured, living resource they own and understand — without having to trust someone else's app or platform with their data and decisions.

The tool needs to meet people where they are technically. For users new to working in a terminal, the process builds practical skills as a side effect. For technical users, it skips the hand-holding and gets to the result.

## Technical minimalism as a skill

The core upskilling goal isn't "learn to program." It's **learn to be technically minimalist**: know what's absolutely necessary for security and essential capabilities, and know what isn't. This is the expertise that lets a busy professional create a technically robust tool without getting into the technical weeds that would normally support such a tool.

This is a disproportionately valuable skill set. Someone who can:
- Open a terminal and direct an AI assistant
- Read structured data and verify it makes sense
- Understand what "you own this data" means technically (local files vs. cloud services)
- Evaluate whether a tool does what they think it does

...can accomplish things that previously required hiring a developer. Not because they learned to code, but because they learned what to ask for, what to check, and what matters. AI assistants handle the implementation; the user handles the judgment.

alexandria is designed so this learning happens as a side effect of building something you actually need. Real motivation, immediate feedback, a useful result — the ideal context for acquiring skills that transfer far beyond this tool.

## Book types

A library contains books of different types. Each type has its own creation process and its own skill.

### Tracker (available)
A curated, structured knowledge base on a domain. Researched, organized, systematically critiqued, and kept current with automated discovery. Built through a seven-phase process that catches the errors a single-pass AI generation misses.

### Import (planned)
A curated collection of external content — papers, articles, books. Organized, annotated, and cross-referenced. For the reader who needs to make sense of a body of work, not just store it.

### Author (planned)
The user's own creative and professional output — notes, research, projects, task lists. Structured and searchable. For turning scattered work into an organized body of work.

## The broader vision

alexandria is a first step toward a larger goal: **infrastructure for people to build high-quality, personalized resources using AI agents — regardless of technical background.** Starting with personal curated libraries, the aim is to establish patterns that generalize:

- A guided process that produces understanding alongside the artifact
- User ownership of the resource and its data
- Technical onboarding woven into real work, not separated into tutorials
- Quality from encoded process knowledge (critique cycles, bias checks), not from programming ability

## Where this is headed

### Near-term
- The /library skill creates and organizes libraries
- The /build-tracker skill produces tracker books via a seven-phase process
- Claude Code skills as the primary delivery mechanism

### Medium-term
- Technical onboarding guidance woven into the process: terminal basics, reading structured data, running scripts, version control — each introduced when needed, not upfront
- Personalization support: relating entries to the user's specific context
- Plugin packaging for streamlined installation
- Import and author book types

### Long-term
- Additional book types as needs emerge
- A community of people sharing and building on each other's curated libraries
- The technical minimalism path proven out: people building and maintaining sophisticated tools regardless of starting technical level, and applying those skills to new problems
