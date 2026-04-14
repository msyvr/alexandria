#!/usr/bin/env python3
"""Generate a browseable wiki view of an alexandria collection.

Reads the collection's .collection-index.yaml and each book's metadata.yaml, produces
static HTML in the collection's wiki/ directory. Works over file:// — no server
needed. Includes multi-axis index pages (by section, date, type, form, media_type)
and individual book pages.

Run from the command line:

    uv run python tools/generate_wiki.py /path/to/alexandria-library

Or invoked by the /coll skill after library-modifying actions.
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Error: pyyaml is required. Run `uv sync` in the alexandria repo.")

try:
    from markdown_it import MarkdownIt
except ImportError:
    sys.exit("Error: markdown-it-py is required. Run `uv sync` in the alexandria repo.")

# Local imports — the templates module is co-located
sys.path.insert(0, str(Path(__file__).parent))
import _wiki_templates as templates

# Configuration
README_WORD_LIMIT = 2000


def narrative_enrich(book_data: dict) -> dict:
    """Pass 2 hook: LLM-assisted topic extraction and cross-references.

    Currently a no-op stub. When Pass 2 is built, this returns per-book topics
    and related-book links that the templates inject into pages.

    Default model when Pass 2 lands: Claude. Local model support deferred until
    there's a clear path and non-technical setup instructions.
    """
    return {"topics": [], "related_books": []}


def load_library(library_path: Path) -> dict:
    """Load the collection index from .collection-index.yaml."""
    index_path = library_path / ".collection-index.yaml"
    if not index_path.exists():
        sys.exit(
            f"Error: {index_path} not found.\n"
            f"Is {library_path} an alexandria collection? Run /coll to create one."
        )
    with open(index_path) as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        sys.exit(f"Error: {index_path} has unexpected format.")
    return data


def load_book_metadata(library_path: Path, book_path: str) -> dict | None:
    """Read a book's metadata.yaml. Returns None if missing."""
    if not book_path:
        return None
    full_path = library_path / book_path / "metadata.yaml"
    if not full_path.exists():
        return None
    try:
        with open(full_path) as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


def load_book_readme(library_path: Path, book_path: str) -> str | None:
    """Read a book's README.md. Returns None if missing."""
    if not book_path:
        return None
    full_path = library_path / book_path / "README.md"
    if not full_path.exists():
        return None
    return full_path.read_text()


def truncate_by_words(text: str, limit: int) -> tuple[str, bool]:
    """Truncate text to roughly `limit` words. Returns (truncated, was_truncated)."""
    words = text.split()
    if len(words) <= limit:
        return text, False
    truncated = " ".join(words[:limit])
    # Try to end at a paragraph boundary
    last_para = truncated.rfind("\n\n")
    if last_para > len(truncated) * 0.7:
        truncated = truncated[:last_para]
    return truncated, True


def render_readme_html(readme_md: str, md_renderer: MarkdownIt) -> tuple[str, bool]:
    """Render README markdown to HTML, truncating to the word limit."""
    truncated_md, was_truncated = truncate_by_words(readme_md, README_WORD_LIMIT)
    html = md_renderer.render(truncated_md)
    return html, was_truncated


def collect_books(library_path: Path, library: dict) -> list[dict]:
    """Build the list of all books, merging index cache with full metadata.

    The index cache contains universal fields; metadata.yaml may have more
    (type-specific fields, provenance details). Metadata.yaml wins when there's
    a conflict, since it's the source of truth.
    """
    all_books: list[dict] = []
    sections = library.get("sections", {})
    if not isinstance(sections, dict):
        return all_books

    for section_name, section_data in sections.items():
        if not isinstance(section_data, dict):
            continue
        books_list = section_data.get("books", [])
        if not isinstance(books_list, list):
            continue
        for book_entry in books_list:
            if not isinstance(book_entry, dict):
                continue
            book_path = book_entry.get("path", "")
            metadata = load_book_metadata(library_path, book_path)
            # Merge: start with index entry, overlay with full metadata
            merged = dict(book_entry)
            if metadata:
                merged.update(metadata)
            # Ensure required fields have defaults
            merged.setdefault("slug", book_entry.get("slug", "unknown"))
            merged.setdefault("section", section_name)
            merged.setdefault("path", book_path)
            all_books.append(merged)
    return all_books


def slugify_section(section: str) -> str:
    """Generate a URL-safe slug from a section name."""
    return section.lower().replace("/", "-").replace(" ", "-")


def generate_wiki(library_path: Path) -> None:
    """Generate the complete wiki for a collection."""
    library = load_library(library_path)
    all_books = collect_books(library_path, library)

    wiki_dir = library_path / "wiki"
    wiki_dir.mkdir(exist_ok=True)

    # Subdirectories for each index axis and for individual books
    subdirs = [
        "_assets",
        "books",
        "by-section",
        "by-date",
        "by-type",
        "by-form",
        "by-media-type",
        "by-topic",
    ]
    for sub in subdirs:
        (wiki_dir / sub).mkdir(exist_ok=True)

    # Copy stylesheet from tools/
    tools_dir = Path(__file__).parent
    css_src = tools_dir / "_wiki_style.css"
    css_dst = wiki_dir / "_assets" / "style.css"
    shutil.copy(css_src, css_dst)

    md_renderer = MarkdownIt("commonmark", {"breaks": True, "html": False})

    # Group books by section (used by homepage and by-section pages)
    books_by_section: dict[str, list[dict]] = {}
    for book in all_books:
        section = book.get("section", "unsorted")
        books_by_section.setdefault(section, []).append(book)

    # --- Homepage ---
    (wiki_dir / "index.html").write_text(templates.homepage(library, all_books))

    # --- By section ---
    (wiki_dir / "by-section" / "index.html").write_text(
        templates.by_section_index(library, books_by_section)
    )
    for section, books in books_by_section.items():
        section_slug = slugify_section(section)
        # Include removed books on section pages (rendered with "removed" marker);
        # they're part of the historical record the collection keeps. Sort active books
        # first, then removed books, both alphabetically within their group.
        sorted_books = sorted(
            books,
            key=lambda b: (
                b.get("status", "active") == "removed",
                b.get("title", "").lower(),
            ),
        )
        (wiki_dir / "by-section" / f"{section_slug}.html").write_text(
            templates.section_page(section, sorted_books)
        )

    # --- By date ---
    (wiki_dir / "by-date" / "index.html").write_text(
        templates.by_date_index(library, all_books)
    )

    # --- By type ---
    (wiki_dir / "by-type" / "index.html").write_text(
        templates.by_type_index(library, all_books)
    )

    # --- By form ---
    (wiki_dir / "by-form" / "index.html").write_text(
        templates.by_form_index(library, all_books)
    )

    # --- By media type ---
    (wiki_dir / "by-media-type" / "index.html").write_text(
        templates.by_media_type_index(library, all_books)
    )

    # --- By topic (Pass 2 placeholder) ---
    (wiki_dir / "by-topic" / "index.html").write_text(
        templates.topic_placeholder(library)
    )

    # --- Individual book pages ---
    for book in all_books:
        slug = book.get("slug", "unknown")
        book_path = book.get("path", "")
        status = book.get("status", "active")
        book_type = book.get("book_type", "unknown")
        settled = bool(book.get("settled", False))

        readme_html = ""
        readme_truncated = False

        # Live scouts link out to their own presentation; settled scouts and other
        # book types render their README inline. Removed books show the removal
        # notice instead of content.
        is_live_scout = book_type == "scout" and not settled
        if status != "removed" and not is_live_scout:
            readme_md = load_book_readme(library_path, book_path)
            if readme_md:
                readme_html, readme_truncated = render_readme_html(readme_md, md_renderer)

        # Pass 2 hook (currently a no-op)
        narrative_enrich(book)

        (wiki_dir / "books" / f"{slug}.html").write_text(
            templates.book_page(book, readme_html, readme_truncated)
        )

    n_books = len(all_books)
    print(f"Generated wiki at {wiki_dir} ({n_books} book{'s' if n_books != 1 else ''})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate alexandria collection wiki")
    parser.add_argument(
        "library_path",
        type=Path,
        help="Path to the alexandria collection root (contains .collection-index.yaml)",
    )
    args = parser.parse_args()

    library_path = args.library_path.expanduser().resolve()
    if not library_path.is_dir():
        sys.exit(f"Error: {library_path} is not a directory")

    generate_wiki(library_path)


if __name__ == "__main__":
    main()
