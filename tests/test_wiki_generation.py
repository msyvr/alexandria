#!/usr/bin/env python3
"""End-to-end test for the alexandria wiki generator.

Creates a synthetic library with all four item types plus edge cases
(removed item, settled scout, user_notes), runs the wiki generator,
and verifies the output against expectations.

Run with:
    uv run python tests/test_wiki_generation.py

Exit codes:
    0 — all checks passed
    1 — one or more checks failed (failures printed to stderr)
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATOR = REPO_ROOT / "tools" / "generate_wiki.py"

CHECKS_RUN = 0
CHECKS_FAILED = 0


def check(name: str, condition: bool, detail: str = ""):
    """Record a check result."""
    global CHECKS_RUN, CHECKS_FAILED
    CHECKS_RUN += 1
    if not condition:
        CHECKS_FAILED += 1
        msg = f"  FAIL: {name}"
        if detail:
            msg += f" — {detail}"
        print(msg, file=sys.stderr)


def check_contains(name: str, text: str, substring: str):
    """Check that text contains a substring."""
    check(name, substring in text, f"expected to find: {substring!r}")


def check_not_contains(name: str, text: str, substring: str):
    """Check that text does NOT contain a substring (regression detection)."""
    check(name, substring not in text, f"expected NOT to find: {substring!r}")


# --- Metadata validation ---

REQUIRED_FIELDS = {"slug", "title", "book_type", "section", "description", "date_added", "form", "media_type", "status"}
VALID_BOOK_TYPES = {"physical", "digital", "scout"}
VALID_FORMS = {"physical", "digital"}
VALID_STATUSES = {"active", "removed"}


def validate_metadata(metadata: dict, label: str):
    """Validate a metadata dict against the universal item shape spec."""
    for field in REQUIRED_FIELDS:
        check(f"{label}: has required field '{field}'", field in metadata)

    if "book_type" in metadata:
        check(
            f"{label}: book_type is valid",
            metadata["book_type"] in VALID_BOOK_TYPES,
            f"got {metadata['book_type']!r}",
        )
    if "form" in metadata:
        check(
            f"{label}: form is valid",
            metadata["form"] in VALID_FORMS,
            f"got {metadata['form']!r}",
        )
    if "status" in metadata:
        check(
            f"{label}: status is valid",
            metadata["status"] in VALID_STATUSES,
            f"got {metadata['status']!r}",
        )
    if "media_type" in metadata:
        check(
            f"{label}: media_type has colon separator",
            ":" in metadata["media_type"],
            f"got {metadata['media_type']!r}",
        )
    if "slug" in metadata:
        # Slug should match directory name (checked during collection creation)
        check(
            f"{label}: slug is lowercase with hyphens",
            metadata["slug"] == metadata["slug"].lower() and " " not in metadata["slug"],
        )


# --- Synthetic collection creation ---

def create_item(lib: Path, section: str, slug: str, metadata: dict, readme: str):
    """Create an item directory with metadata.yaml and README.md."""
    item_dir = lib / section / slug
    item_dir.mkdir(parents=True, exist_ok=True)

    import yaml
    (item_dir / "metadata.yaml").write_text(yaml.dump(metadata, default_flow_style=False, sort_keys=False))
    (item_dir / "README.md").write_text(readme)


def create_synthetic_library(lib: Path):
    """Build a complete synthetic library for testing."""
    import yaml

    items = []

    # --- Physical item (hardcover, with user_notes) ---
    meta_physical = {
        "slug": "the-dispossessed",
        "title": "The Dispossessed",
        "book_type": "physical",
        "section": "fiction",
        "description": "Ursula K. Le Guin's anarchist utopia novel.",
        "date_added": "2026-03-15",
        "form": "physical",
        "media_type": "text:hardcover",
        "status": "active",
        "author": "Ursula K. Le Guin",
        "user_notes": "First edition, signed. Handle with care.",
        "photo": "photo.jpg",
        "shelf_location": "Living room, top shelf",
    }
    create_item(lib, "fiction", "the-dispossessed", meta_physical,
                "# The Dispossessed\n\n*by Ursula K. Le Guin*\n\nA novel about walls.")
    items.append({"path": "fiction/the-dispossessed", **{k: meta_physical[k] for k in REQUIRED_FIELDS | {"author"}}})

    # --- Digital item (PDF import) ---
    meta_digital = {
        "slug": "causal-inference-primer",
        "title": "Causal Inference Primer",
        "book_type": "digital",
        "section": "professional",
        "description": "An introductory paper on causal inference methods.",
        "date_added": "2026-04-01",
        "form": "digital",
        "media_type": "text:pdf",
        "status": "active",
        "author": "A. Researcher",
        "provenance": {"source": "/Users/test/Downloads/ci-primer.pdf", "imported_from": "local-file"},
    }
    create_item(lib, "professional", "causal-inference-primer", meta_digital,
                "# Causal Inference Primer\n\n*by A. Researcher*\n\nContent preserved in original.pdf.")
    # Add notes/ directory with multiple notes for this item
    notes_dir = lib / "professional" / "causal-inference-primer" / "notes"
    notes_dir.mkdir()
    (notes_dir / "2026-04-14-reading-notes.md").write_text(
        "# Reading Notes\n\n"
        "## Key takeaways\n\n"
        "- The IV framework in section 3 is directly applicable to my thesis\n"
        "- The robustness checks in section 5 should be replicated\n\n"
        "## Quotes\n\n"
        "> \"The fundamental problem of causal inference is that we can never observe\n"
        "> the counterfactual outcome.\" (p. 12)\n"
    )
    (notes_dir / "2026-04-21-seminar-followup.md").write_text(
        "# Seminar Followup\n\n"
        "The presenter challenged the exclusion restriction assumption.\n"
        "Need to revisit section 4.\n"
    )
    items.append({"path": "professional/causal-inference-primer", **{k: meta_digital[k] for k in REQUIRED_FIELDS | {"author"}}})

    # --- User-authored digital item (markdown notes) ---
    meta_notes = {
        "slug": "thesis-notes",
        "title": "Thesis Notes",
        "book_type": "digital",
        "section": "research",
        "description": "Working notes for my thesis on policy evaluation.",
        "date_added": "2026-04-05",
        "form": "digital",
        "media_type": "text:markdown",
        "status": "active",
    }
    create_item(lib, "research", "thesis-notes", meta_notes,
                "# Thesis Notes\n\n## Current focus\n\nLiterature review on IV methods.\n\n## Open questions\n\n- How to handle weak instruments?")
    items.append({"path": "research/thesis-notes", **{k: meta_notes[k] for k in REQUIRED_FIELDS}})

    # --- Live scout ---
    meta_scout_live = {
        "slug": "ai-safety-scout",
        "title": "AI Safety Scout",
        "book_type": "scout",
        "section": "research",
        "description": "Living knowledge base monitoring AI safety developments.",
        "date_added": "2026-04-08",
        "form": "digital",
        "media_type": "text:markdown",
        "status": "active",
        "settled": False,
    }
    create_item(lib, "research", "ai-safety-scout", meta_scout_live,
                "# AI Safety Scout\n\nA living knowledge base with 23 entries across 5 categories.\n\n## Getting Started\n\nStart here.")
    items.append({"path": "research/ai-safety-scout", **{k: meta_scout_live[k] for k in REQUIRED_FIELDS}})

    # --- Settled scout ---
    meta_scout_settled = {
        "slug": "treatment-landscape",
        "title": "Treatment Landscape",
        "book_type": "scout",
        "section": "health",
        "description": "Settled scout — treatment options for condition X.",
        "date_added": "2026-03-01",
        "form": "digital",
        "media_type": "text:markdown",
        "status": "active",
        "settled": True,
        "settled_at": "2026-04-10",
    }
    create_item(lib, "health", "treatment-landscape", meta_scout_settled,
                "# Treatment Landscape\n\nThis scout was settled on April 10. Content is frozen.\n\n## Entries\n\n1. Treatment A\n2. Treatment B\n3. Treatment C")
    items.append({"path": "health/treatment-landscape", **{k: meta_scout_settled[k] for k in REQUIRED_FIELDS}})

    # --- Removed item ---
    meta_removed = {
        "slug": "outdated-reference",
        "title": "Outdated Reference",
        "book_type": "physical",
        "section": "fiction",
        "description": "An item that was removed from the collection.",
        "date_added": "2025-06-01",
        "form": "physical",
        "media_type": "text:paperback",
        "status": "removed",
        "removed_at": "2026-04-11",
        "removed_reason": "Superseded by a newer edition.",
        "author": "Old Author",
    }
    create_item(lib, "fiction", "outdated-reference", meta_removed,
                "# Outdated Reference\n\nThis content should not be shown — the item is removed.")
    items.append({"path": "fiction/outdated-reference", **{k: meta_removed[k] for k in REQUIRED_FIELDS | {"author", "removed_at", "removed_reason"}}})

    # --- Build .collection-index.yaml ---
    sections: dict[str, list] = {}
    for item in items:
        section = item.get("section", "unsorted")
        sections.setdefault(section, []).append(item)

    index = {
        "collection_name": "test-library",
        "created": "2026-03-01",
        "sections": {s: {"items": bks} for s, bks in sections.items()},
    }
    (lib / ".collection-index.yaml").write_text(yaml.dump(index, default_flow_style=False, sort_keys=False))

    # --- Create a collection-context.md with journal entries ---
    (lib / "collection-context.md").write_text("""# Context: test-library

## [2026-04-10 14:30] Checkpoint

**Accomplished:** Added 3 physical items from the living room shelf

**Decisions:** Used hardcover as the default media type for the shelf batch

**User preferences:** Prefers no online enrichment

**Open questions:** none

**Q&A worth keeping:** none

SESSION_NOTES_CHECKPOINT

## [2026-04-12 09:15] Checkpoint

**Accomplished:** Imported 2 research PDFs and settled the treatment landscape scout

**Decisions:** Settled the scout because treatment decision is made

**User preferences:** none new

**Open questions:** Should we add a nutrition section?

**Q&A worth keeping:** none

SESSION_NOTES_CHECKPOINT
""")

    return items


# --- Verification ---

def verify_wiki(lib: Path, items: list[dict]):
    """Run all verification checks against the generated wiki."""
    wiki = lib / "wiki"

    # --- File existence ---
    check("wiki/ directory exists", wiki.is_dir())
    check("homepage exists", (wiki / "index.html").is_file())
    check("stylesheet exists", (wiki / "_assets" / "style.css").is_file())

    expected_indexes = ["by-section", "by-date", "by-type", "by-form", "by-media-type", "by-topic", "collection-journal"]
    for idx in expected_indexes:
        check(f"{idx}/index.html exists", (wiki / idx / "index.html").is_file())

    for item in items:
        slug = item["slug"]
        check(f"items/{slug}.html exists", (wiki / "items" / f"{slug}.html").is_file())

    # --- Homepage content ---
    homepage = (wiki / "index.html").read_text()
    check_contains("homepage: library name", homepage, "test-library")
    # 6 items total, but active count is 5 (1 removed)
    check_contains("homepage: item count", homepage, "5 items")

    # --- By-section index ---
    by_section = (wiki / "by-section" / "index.html").read_text()
    check_contains("by-section: fiction section listed", by_section, "fiction")
    check_contains("by-section: research section listed", by_section, "research")
    check_contains("by-section: health section listed", by_section, "health")
    check_contains("by-section: professional section listed", by_section, "professional")

    # --- By-form index ---
    by_form = (wiki / "by-form" / "index.html").read_text()
    check_contains("by-form: physical group", by_form, "Physical")
    check_contains("by-form: digital group", by_form, "Digital")

    # --- By-media-type index ---
    by_media = (wiki / "by-media-type" / "index.html").read_text()
    check_contains("by-media-type: text content type", by_media, "text")
    check_contains("by-media-type: hardcover format", by_media, "hardcover")
    check_contains("by-media-type: pdf format", by_media, "pdf")

    # --- By-topic placeholder ---
    by_topic = (wiki / "by-topic" / "index.html").read_text()
    check_contains("by-topic: placeholder message", by_topic, "narrative layer")

    # --- Live scout: links out (does NOT render inline content) ---
    live_scout_page = (wiki / "items" / "ai-safety-scout.html").read_text()
    check_contains("live scout: has link-out", live_scout_page, "Open the scout")
    check_contains("live scout: shows Live status", live_scout_page, "Live (updates via discovery)")
    # REGRESSION CHECK: live scout should NOT have the README body rendered inline
    # (the page title in <header> is fine; it's the README content we're checking against)
    check_not_contains("live scout: no inline README body", live_scout_page, "A living knowledge base with 23 entries")
    check_not_contains("live scout: no inline README headings", live_scout_page, "<h2>Getting Started</h2>")

    # --- Settled scout: renders inline (does NOT link out) ---
    settled_page = (wiki / "items" / "treatment-landscape.html").read_text()
    check_contains("settled scout: inline content rendered", settled_page, "This scout was settled on April 10")
    check_contains("settled scout: shows Settled status", settled_page, "Settled (static reference)")
    check_contains("settled scout: shows settled_at date", settled_page, "2026-04-10")
    # REGRESSION CHECK: settled scout should NOT have the link-out
    check_not_contains("settled scout: no link-out", settled_page, "Open the scout")

    # --- Removed item: shows removal notice, NOT inline content ---
    removed_page = (wiki / "items" / "outdated-reference.html").read_text()
    check_contains("removed item: removal notice", removed_page, "Resource removed")
    check_contains("removed item: removed_at shown", removed_page, "2026-04-11")
    check_contains("removed item: removal reason shown", removed_page, "Superseded by a newer edition")
    # REGRESSION CHECK: removed item should NOT render its README content
    check_not_contains("removed item: no inline content", removed_page, "This content should not be shown")

    # --- Physical item with user_notes ---
    physical_page = (wiki / "items" / "the-dispossessed.html").read_text()
    check_contains("physical item: title shown", physical_page, "The Dispossessed")
    check_contains("physical item: author shown", physical_page, "Ursula K. Le Guin")
    check_contains("physical item: user_notes shown", physical_page, "First edition, signed")
    check_contains("physical item: user_notes in blockquote", physical_page, "user-notes")

    # --- Digital item with notes/ directory ---
    digital_page = (wiki / "items" / "causal-inference-primer.html").read_text()
    check_contains("digital item: title shown", digital_page, "Causal Inference Primer")
    check_contains("digital item: media_type shown", digital_page, "text:pdf")
    check_contains("digital item: notes section rendered", digital_page, "item-notes")
    check_contains("digital item: first note title", digital_page, "Reading Notes")
    check_contains("digital item: first note content", digital_page, "IV framework in section 3")
    check_contains("digital item: first note blockquote", digital_page, "counterfactual outcome")
    check_contains("digital item: second note title", digital_page, "Seminar Followup")
    check_contains("digital item: second note content", digital_page, "exclusion restriction")

    # --- User-authored digital item ---
    notes_page = (wiki / "items" / "thesis-notes.html").read_text()
    check_contains("digital notes: title shown", notes_page, "Thesis Notes")
    check_contains("digital notes: inline content", notes_page, "Literature review on IV methods")

    # --- Section page includes removed items ---
    fiction_section = (wiki / "by-section" / "fiction.html").read_text()
    check_contains("section page: active item listed", fiction_section, "The Dispossessed")
    check_contains("section page: removed item listed", fiction_section, "Outdated Reference")
    check_contains("section page: removed marker on removed item", fiction_section, "removed-tag")

    # --- Collection journal ---
    journal = (wiki / "collection-journal" / "index.html").read_text()
    check_contains("journal: has timeline intro", journal, "timeline of your collection")
    check_contains("journal: first entry headline", journal, "Added 3 physical items")
    check_contains("journal: second entry headline", journal, "Imported 2 research PDFs")
    check_contains("journal: month grouping 2026-04", journal, "2026-04")
    check_contains("journal: decisions rendered", journal, "Used hardcover as the default")
    check_contains("journal: open questions rendered", journal, "nutrition section")
    # REGRESSION: sentinel should NOT appear in rendered output
    check_not_contains("journal: no sentinel in output", journal, "SESSION_NOTES_CHECKPOINT")


# --- Main ---

def main():
    global CHECKS_RUN, CHECKS_FAILED

    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.exit("Error: pyyaml required. Run `uv sync` in the alexandria repo.")

    # Create temp library
    tmpdir = Path(tempfile.mkdtemp(prefix="alexandria-e2e-"))
    try:
        print(f"Creating synthetic library at {tmpdir}...")
        items = create_synthetic_library(tmpdir)

        # Validate all synthetic metadata against the spec
        print("Validating synthetic metadata...")
        for book_entry in items:
            book_path = tmpdir / book_entry["path"] / "metadata.yaml"
            if book_path.exists():
                import yaml
                with open(book_path) as f:
                    meta = yaml.safe_load(f)
                validate_metadata(meta, book_entry["slug"])

        # Run the wiki generator
        print("Running wiki generator...")
        result = subprocess.run(
            [sys.executable, str(GENERATOR), str(tmpdir)],
            capture_output=True,
            text=True,
        )
        check("generator exits successfully", result.returncode == 0, result.stderr.strip() if result.returncode != 0 else "")

        if result.returncode == 0:
            # Verify the output
            print("Verifying wiki output...")
            verify_wiki(tmpdir, [b for b in items if "slug" in b or "slug" in b.get("metadata", {})])
        else:
            print(f"Generator failed:\n{result.stderr}", file=sys.stderr)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # Report
    print(f"\n{CHECKS_RUN} checks run, {CHECKS_FAILED} failed.")
    if CHECKS_FAILED > 0:
        print(f"\nFAILED — {CHECKS_FAILED} issue(s).", file=sys.stderr)
        sys.exit(1)
    else:
        print("PASSED — all checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
