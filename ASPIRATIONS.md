# Project Aspirations

## The core idea

alexandria is a self-contained personal library — a place to organize, reference, and maintain any digital content that matters to you. Notes you write. Papers and articles you collect. Knowledge bases an AI builds for you on demand. Projects you're working on. Reference material you don't want to lose. The library is yours: files on your machine, organized however suits you, browseable in any markdown viewer or browser.

The library is the foundation. "Books" are the things that go in it — distinct units of content, each a self-contained directory. Different book types serve different purposes, but they share a common shape: each one is a project the user owns and can inspect in its entirety.

The tool is AI-assisted. Claude Code helps create and maintain books, organizes the library, and remembers context across sessions through user-visible files. The user drives direction; the AI handles the implementation work that would otherwise require programming skill.

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

Anyone who would benefit from an organized, personal collection of structured digital content — and wants to own the result rather than depend on someone else's platform. The target user is thorough, motivated, and has a real need. Some are software engineers who don't want to build the scaffolding from scratch. Some have never opened a terminal. Both want the same thing: a structured, living resource they own and understand.

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

## Library architecture

The library is a directory containing books, organized into sections. Each book is a self-contained project (its own git repo). The library has lightweight infrastructure that applies regardless of book type:

- **An index** (`.library-index.yaml`) — maps the library's structure
- **An organizational layer** — sections, subdivision when sections grow, cross-book queries
- **Persistent context** — every book has user-visible files (`CLAUDE.md`, `context.md`) that capture decisions, user preferences, and interaction history. These survive across sessions and tool changes.
- **Browseable views** — interlinked README.md files and pre-rendered HTML, viewable in any markdown viewer or browser without a server

This infrastructure is shared. New book types plug into it without redesigning the foundation.

## Book types

A book type defines how content of a particular kind gets created, organized, and maintained within a library. Each type has its own creation skill and its own conventions, but all book types share the library's infrastructure (index, persistent context, browseable views).

### Scout (available)
A curated, structured knowledge base that monitors a domain. Created by AI through a seven-phase process with built-in self-critique. Once built, automated discovery keeps it current. Useful when the user needs to understand and stay current on a topic that's complex, personal, and evolving.

### Import (planned)
A curated collection of content the user has gathered from elsewhere — papers, articles, web pages, downloaded files, screenshots, anything with provenance. Organized, annotated, and cross-referenced. For when the user has accumulated material and needs to make sense of it, not just store it.

### Author (planned)
A book for content the user produces themselves — notes, research, drafts, project plans, task lists, journal entries. Structured enough to be searchable and maintainable, flexible enough to accommodate freeform writing. For turning scattered personal work into an organized body of work.

### Future types
The architecture is designed to accommodate book types we haven't thought of yet. The constraint is the shared infrastructure: a book type must produce a self-contained directory with user-visible files, fit into the library's organizational layer, and use the persistent context mechanism. Beyond that, book types are free to define their own creation processes and structures.

## The broader vision

alexandria is a first step toward a larger goal: **infrastructure for people to build high-quality, personalized resources using AI agents — regardless of technical background.** Starting with personal libraries, the aim is to establish patterns that generalize:

- A guided process that produces understanding alongside the artifact
- User ownership of the resource and its data
- Technical onboarding woven into real work, not separated into tutorials
- Quality from encoded process knowledge (critique cycles, bias checks), not from programming ability
- Persistence and continuity through user-visible files, not opaque tool state

## Where this is headed

### Near-term
- The /library skill creates and organizes libraries
- The /new-scout skill provides the first book type
- Persistent context (CLAUDE.md, context.md, take-notes skill) is in place
- Claude Code skills as the primary delivery mechanism

### Medium-term
- Technical onboarding guidance woven into the process: terminal basics, reading structured data, running scripts, version control — each introduced when needed, not upfront
- Import book type: bringing in external content with provenance and annotation
- Author book type: structuring user-produced content
- Personalization support: relating book content to the user's specific context
- Plugin packaging for streamlined installation

### Long-term
- Additional book types as needs emerge
- Q&A as a first-class interaction with books and the library as a whole
- Compounding exploration: questions and answers feed back into the library
- A community of people sharing and building on each other's curated libraries
- The technical minimalism path proven out: people building and maintaining sophisticated personal tools regardless of starting technical level, and applying those skills to new problems
