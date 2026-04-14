#!/usr/bin/env python3
"""End-to-end test for the alexandria wiki generator.

Creates a synthetic library with all four book types plus edge cases
(removed book, settled scout, user_notes), runs the wiki generator,
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
    """Validate a metadata dict against the universal book shape spec."""
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

def create_book(lib: Path, section: str, slug: str, metadata: dict, readme: str):
    """Create a book directory with metadata.yaml and README.md."""
    book_dir = lib / section / slug
    book_dir.mkdir(parents=True, exist_ok=True)

    import yaml
    (book_dir / "metadata.yaml").write_text(yaml.dump(metadata, default_flow_style=False, sort_keys=False))
    (book_dir / "README.md").write_text(readme)


def create_synthetic_library(lib: Path):
    """Build a complete synthetic library for testing."""
    import yaml

    books = []

    # --- Physical book (hardcover, with user_notes) ---
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
    create_book(lib, "fiction", "the-dispossessed", meta_physical,
                "# The Dispossessed\n\n*by Ursula K. Le Guin*\n\nA novel about walls.")
    books.append({"path": "fiction/the-dispossessed", **{k: meta_physical[k] for k in REQUIRED_FIELDS | {"author"}}})

    # --- Digital book (PDF import) ---
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
    create_book(lib, "professional", "causal-inference-primer", meta_digital,
                "# Causal Inference Primer\n\n*by A. Researcher*\n\nContent preserved in original.pdf.")
    books.append({"path": "professional/causal-inference-primer", **{k: meta_digital[k] for k in REQUIRED_FIELDS | {"author"}}})

    # --- User-authored digital book (markdown notes) ---
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
    create_book(lib, "research", "thesis-notes", meta_notes,
                "# Thesis Notes\n\n## Current focus\n\nLiterature review on IV methods.\n\n## Open questions\n\n- How to handle weak instruments?")
    books.append({"path": "research/thesis-notes", **{k: meta_notes[k] for k in REQUIRED_FIELDS}})

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
    create_book(lib, "research", "ai-safety-scout", meta_scout_live,
                "# AI Safety Scout\n\nA living knowledge base with 23 entries across 5 categories.\n\n## Getting Started\n\nStart here.")
    books.append({"path": "research/ai-safety-scout", **{k: meta_scout_live[k] for k in REQUIRED_FIELDS}})

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
    create_book(lib, "health", "treatment-landscape", meta_scout_settled,
                "# Treatment Landscape\n\nThis scout was settled on April 10. Content is frozen.\n\n## Entries\n\n1. Treatment A\n2. Treatment B\n3. Treatment C")
    books.append({"path": "health/treatment-landscape", **{k: meta_scout_settled[k] for k in REQUIRED_FIELDS}})

    # --- Removed book ---
    meta_removed = {
        "slug": "outdated-reference",
        "title": "Outdated Reference",
        "book_type": "physical",
        "section": "fiction",
        "description": "A book that was removed from the collection.",
        "date_added": "2025-06-01",
        "form": "physical",
        "media_type": "text:paperback",
        "status": "removed",
        "removed_at": "2026-04-11",
        "removed_reason": "Superseded by a newer edition.",
        "author": "Old Author",
    }
    create_book(lib, "fiction", "outdated-reference", meta_removed,
                "# Outdated Reference\n\nThis content should not be shown — the book is removed.")
    books.append({"path": "fiction/outdated-reference", **{k: meta_removed[k] for k in REQUIRED_FIELDS | {"author", "removed_at", "removed_reason"}}})

    # --- Build .collection-index.yaml ---
    sections: dict[str, list] = {}
    for book in books:
        section = book.get("section", "unsorted")
        sections.setdefault(section, []).append(book)

    index = {
        "collection_name": "test-library",
        "created": "2026-03-01",
        "sections": {s: {"books": bks} for s, bks in sections.items()},
    }
    (lib / ".collection-index.yaml").write_text(yaml.dump(index, default_flow_style=False, sort_keys=False))

    return books


# --- Verification ---

def verify_wiki(lib: Path, books: list[dict]):
    """Run all verification checks against the generated wiki."""
    wiki = lib / "wiki"

    # --- File existence ---
    check("wiki/ directory exists", wiki.is_dir())
    check("homepage exists", (wiki / "index.html").is_file())
    check("stylesheet exists", (wiki / "_assets" / "style.css").is_file())

    expected_indexes = ["by-section", "by-date", "by-type", "by-form", "by-media-type", "by-topic"]
    for idx in expected_indexes:
        check(f"{idx}/index.html exists", (wiki / idx / "index.html").is_file())

    for book in books:
        slug = book["slug"]
        check(f"books/{slug}.html exists", (wiki / "books" / f"{slug}.html").is_file())

    # --- Homepage content ---
    homepage = (wiki / "index.html").read_text()
    check_contains("homepage: library name", homepage, "test-library")
    # 6 books total, but active count is 5 (1 removed)
    check_contains("homepage: book count", homepage, "<strong>5</strong>")

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
    live_scout_page = (wiki / "books" / "ai-safety-scout.html").read_text()
    check_contains("live scout: has link-out", live_scout_page, "Open the scout")
    check_contains("live scout: shows Live status", live_scout_page, "Live (updates via discovery)")
    # REGRESSION CHECK: live scout should NOT have the README body rendered inline
    # (the page title in <header> is fine; it's the README content we're checking against)
    check_not_contains("live scout: no inline README body", live_scout_page, "A living knowledge base with 23 entries")
    check_not_contains("live scout: no inline README headings", live_scout_page, "<h2>Getting Started</h2>")

    # --- Settled scout: renders inline (does NOT link out) ---
    settled_page = (wiki / "books" / "treatment-landscape.html").read_text()
    check_contains("settled scout: inline content rendered", settled_page, "This scout was settled on April 10")
    check_contains("settled scout: shows Settled status", settled_page, "Settled (static reference)")
    check_contains("settled scout: shows settled_at date", settled_page, "2026-04-10")
    # REGRESSION CHECK: settled scout should NOT have the link-out
    check_not_contains("settled scout: no link-out", settled_page, "Open the scout")

    # --- Removed book: shows removal notice, NOT inline content ---
    removed_page = (wiki / "books" / "outdated-reference.html").read_text()
    check_contains("removed book: removal notice", removed_page, "Resource removed")
    check_contains("removed book: removed_at shown", removed_page, "2026-04-11")
    check_contains("removed book: removal reason shown", removed_page, "Superseded by a newer edition")
    # REGRESSION CHECK: removed book should NOT render its README content
    check_not_contains("removed book: no inline content", removed_page, "This content should not be shown")

    # --- Physical book with user_notes ---
    physical_page = (wiki / "books" / "the-dispossessed.html").read_text()
    check_contains("physical book: title shown", physical_page, "The Dispossessed")
    check_contains("physical book: author shown", physical_page, "Ursula K. Le Guin")
    check_contains("physical book: user_notes shown", physical_page, "First edition, signed")
    check_contains("physical book: user_notes in blockquote", physical_page, "user-notes")

    # --- Digital book ---
    digital_page = (wiki / "books" / "causal-inference-primer.html").read_text()
    check_contains("digital book: title shown", digital_page, "Causal Inference Primer")
    check_contains("digital book: media_type shown", digital_page, "text:pdf")

    # --- User-authored digital book ---
    notes_page = (wiki / "books" / "thesis-notes.html").read_text()
    check_contains("digital notes: title shown", notes_page, "Thesis Notes")
    check_contains("digital notes: inline content", notes_page, "Literature review on IV methods")

    # --- Section page includes removed books ---
    fiction_section = (wiki / "by-section" / "fiction.html").read_text()
    check_contains("section page: active book listed", fiction_section, "The Dispossessed")
    check_contains("section page: removed book listed", fiction_section, "Outdated Reference")
    check_contains("section page: removed marker on removed book", fiction_section, "removed-tag")


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
        books = create_synthetic_library(tmpdir)

        # Validate all synthetic metadata against the spec
        print("Validating synthetic metadata...")
        for book_entry in books:
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
            verify_wiki(tmpdir, [b for b in books if "slug" in b or "slug" in b.get("metadata", {})])
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
