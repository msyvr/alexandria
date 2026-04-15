#!/usr/bin/env python3
"""Generate a browseable wiki view of an alexandria collection.

Reads the collection's .collection-index.yaml and each item's metadata.yaml, produces
static HTML in the collection's wiki/ directory. Works over file:// — no server
needed. Includes multi-axis index pages (by section, date, type, form, media_type)
and individual item pages.

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

    Currently a no-op stub. When Pass 2 is built, this returns per-item topics
    and related-item links that the templates inject into pages.

    Default model when Pass 2 lands: Claude. Local model support deferred until
    there's a clear path and non-technical setup instructions.
    """
    return {"topics": [], "related_items": []}


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


def load_item_metadata(library_path: Path, book_path: str) -> dict | None:
    """Read an item's metadata.yaml. Returns None if missing."""
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


def load_item_readme(library_path: Path, book_path: str) -> str | None:
    """Read an item's README.md. Returns None if missing."""
    if not book_path:
        return None
    full_path = library_path / book_path / "README.md"
    if not full_path.exists():
        return None
    return full_path.read_text()


def load_item_notes(library_path: Path, book_path: str, md_renderer) -> list[dict]:
    """Load all notes from an item's notes/ directory.

    Returns a list of dicts sorted by filename (date-prefixed), each with:
      - filename: str
      - title: str (extracted from first heading or derived from filename)
      - html: str (rendered markdown)
      - is_pdf: bool
    """
    if not book_path:
        return []
    notes_dir = library_path / book_path / "notes"
    if not notes_dir.is_dir():
        return []

    notes = []
    for f in sorted(notes_dir.iterdir()):
        if f.name.startswith("."):
            continue
        if f.suffix == ".pdf":
            notes.append({
                "filename": f.name,
                "title": f.stem.replace("-", " ").lstrip("0123456789 "),
                "html": "",
                "is_pdf": True,
            })
        elif f.suffix in (".md", ".txt"):
            content = f.read_text()
            # Extract title from first heading if present
            title = f.stem.replace("-", " ").lstrip("0123456789 ")
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            html = md_renderer.render(content)
            notes.append({
                "filename": f.name,
                "title": title,
                "html": html,
                "is_pdf": False,
            })
    return notes


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
    """Build the list of all items, merging index cache with full metadata.

    The index cache contains universal fields; metadata.yaml may have more
    (type-specific fields, provenance details). Metadata.yaml wins when there's
    a conflict, since it's the source of truth.
    """
    all_items: list[dict] = []
    sections = library.get("sections", {})
    if not isinstance(sections, dict):
        return all_items

    for section_name, section_data in sections.items():
        if not isinstance(section_data, dict):
            continue
        books_list = section_data.get("items", [])
        if not isinstance(books_list, list):
            continue
        for book_entry in books_list:
            if not isinstance(book_entry, dict):
                continue
            book_path = book_entry.get("path", "")
            metadata = load_item_metadata(library_path, book_path)
            # Merge: start with index entry, overlay with full metadata
            merged = dict(book_entry)
            if metadata:
                merged.update(metadata)
            # Ensure required fields have defaults
            merged.setdefault("slug", book_entry.get("slug", "unknown"))
            merged.setdefault("section", section_name)
            merged.setdefault("path", book_path)
            all_items.append(merged)
    return all_items


def slugify_section(section: str) -> str:
    """Generate a URL-safe slug from a section name."""
    return section.lower().replace("/", "-").replace(" ", "-")


def parse_collection_context(library_path: Path, md_renderer) -> list[dict]:
    """Parse collection-context.md into a list of journal entries.

    Each entry is a dict with:
      - date: str (YYYY-MM-DD)
      - time: str (HH:MM)
      - accomplished: str (the headline extracted from the Accomplished section)
      - full_html: str (the full checkpoint content rendered as HTML)
    """
    import re

    context_path = library_path / "collection-context.md"
    if not context_path.exists():
        return []

    text = context_path.read_text()

    # Split on checkpoint headers: ## [YYYY-MM-DD HH:MM] Checkpoint
    # or ## [YYYY-MM-DD HH:MM] Checkpoint — description
    checkpoint_pattern = re.compile(
        r"^## \[(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\]\s*(?:Checkpoint|.*?)$",
        re.MULTILINE,
    )

    entries = []
    matches = list(checkpoint_pattern.finditer(text))

    for i, match in enumerate(matches):
        date = match.group(1)
        time = match.group(2)

        # Extract the content between this header and the next (or end of file)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # Remove the SESSION_NOTES_CHECKPOINT sentinel if present
        content = content.replace("SESSION_NOTES_CHECKPOINT", "").strip()

        # Extract the "Accomplished" line for the headline
        accomplished = ""
        for line in content.splitlines():
            if line.startswith("**Accomplished:**"):
                accomplished = line.replace("**Accomplished:**", "").strip()
                break

        # Render the content as HTML
        full_html = md_renderer.render(content) if content else ""

        entries.append({
            "date": date,
            "time": time,
            "accomplished": accomplished,
            "full_html": full_html,
        })

    return entries


def generate_wiki(library_path: Path) -> None:
    """Generate the complete wiki for a collection."""
    library = load_library(library_path)
    all_items = collect_books(library_path, library)

    wiki_dir = library_path / "wiki"
    wiki_dir.mkdir(exist_ok=True)

    # Subdirectories for each index axis and for individual items
    subdirs = [
        "_assets",
        "items",
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

    # Group items by section (used by homepage and by-section pages)
    items_by_section: dict[str, list[dict]] = {}
    for item in all_items:
        section = item.get("section", "unsorted")
        items_by_section.setdefault(section, []).append(item)

    # --- Homepage ---
    (wiki_dir / "index.html").write_text(templates.homepage(library, all_items))

    # --- By section ---
    (wiki_dir / "by-section" / "index.html").write_text(
        templates.by_section_index(library, items_by_section)
    )
    for section, items in items_by_section.items():
        section_slug = slugify_section(section)
        # Include removed items on section pages (rendered with "removed" marker);
        # they're part of the historical record the collection keeps. Sort active items
        # first, then removed items, both alphabetically within their group.
        sorted_books = sorted(
            items,
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
        templates.by_date_index(library, all_items)
    )

    # --- By type ---
    (wiki_dir / "by-type" / "index.html").write_text(
        templates.by_type_index(library, all_items)
    )

    # --- By form ---
    (wiki_dir / "by-form" / "index.html").write_text(
        templates.by_form_index(library, all_items)
    )

    # --- By media type ---
    (wiki_dir / "by-media-type" / "index.html").write_text(
        templates.by_media_type_index(library, all_items)
    )

    # --- By topic (Pass 2 placeholder) ---
    (wiki_dir / "by-topic" / "index.html").write_text(
        templates.topic_placeholder(library)
    )

    # --- Collection journal ---
    (wiki_dir / "collection-journal").mkdir(exist_ok=True)
    journal_entries = parse_collection_context(library_path, md_renderer)
    (wiki_dir / "collection-journal" / "index.html").write_text(
        templates.collection_journal(library, journal_entries)
    )

    # --- Individual item pages ---
    for item in all_items:
        slug = item.get("slug", "unknown")
        book_path = item.get("path", "")
        status = item.get("status", "active")
        book_type = item.get("book_type", "unknown")
        settled = bool(item.get("settled", False))

        readme_html = ""
        readme_truncated = False
        item_notes: list[dict] = []

        # Live scouts link out to their own presentation; settled scouts and other
        # item types render their README inline. Removed items show the removal
        # notice instead of content.
        is_live_scout = book_type == "scout" and not settled
        if status != "removed" and not is_live_scout:
            readme_md = load_item_readme(library_path, book_path)
            if readme_md:
                readme_html, readme_truncated = render_readme_html(readme_md, md_renderer)

        # Load user notes from notes/ directory if present
        if status != "removed":
            item_notes = load_item_notes(library_path, book_path, md_renderer)

        # Pass 2 hook (currently a no-op)
        narrative_enrich(item)

        (wiki_dir / "items" / f"{slug}.html").write_text(
            templates.item_page(item, readme_html, readme_truncated, item_notes)
        )

    n_books = len(all_items)
    print(f"Generated wiki at {wiki_dir} ({n_books} item{'s' if n_books != 1 else ''})")


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
