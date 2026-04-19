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
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif"}


def find_item_thumbnail(library_path: Path, book_path: str) -> str | None:
    """Return the filename (relative to the item directory) of the first image
    file found in the item's directory, or None if there are no images.

    Filename match is case-insensitive on the extension; alphabetical order
    decides when multiple images exist.
    """
    if not book_path:
        return None
    item_dir = library_path / book_path
    if not item_dir.is_dir():
        return None
    images = [
        entry.name for entry in item_dir.iterdir()
        if entry.is_file() and entry.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images)[0] if images else None


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
        if f.suffix in (".md", ".txt"):
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


def _convert_kv_lists_to_dl(html: str) -> str:
    """Convert bullet lists of "**Label**: value" pairs to a <dl> grid.

    Markdown renders `- **Label**: value` as <li><strong>Label</strong>: value</li>.
    When every <li> in a <ul> matches that shape, rewrite the list as a <dl> so
    the stylesheet can render it as an aligned label/value grid matching the
    page's main metadata block. Lists that don't uniformly match are untouched.
    """
    import re

    UL_RE = re.compile(r'<ul>\s*(.*?)\s*</ul>', re.DOTALL)
    LI_RE = re.compile(r'<li>(.*?)</li>', re.DOTALL)
    KV_RE = re.compile(r'^\s*<strong>(.*?)</strong>\s*:\s*(.*?)\s*$', re.DOTALL)

    def replace_ul(match: "re.Match[str]") -> str:
        inner = match.group(1)
        lis = LI_RE.findall(inner)
        if not lis:
            return match.group(0)
        pairs = []
        for li in lis:
            kv = KV_RE.match(li)
            if not kv:
                return match.group(0)
            pairs.append((kv.group(1), kv.group(2)))
        dl_items = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in pairs)
        return f'<dl class="kv-grid">{dl_items}</dl>'

    return UL_RE.sub(replace_ul, html)


def _strip_description_paragraphs(html: str, description: str) -> str:
    """Remove any <p>...</p> whose text content matches the metadata
    description (after whitespace normalization and inner-tag stripping).

    The item page already renders the description separately at the top,
    so any copy inside the README body is redundant — no matter where it
    appears (first paragraph, after a photo, repeated by hand edit).
    """
    import re
    if not description:
        return html
    norm_desc = re.sub(r"\s+", " ", description).strip()
    if not norm_desc:
        return html

    def _replace(match: "re.Match[str]") -> str:
        inner = match.group(1)
        # Strip inner tags, then collapse whitespace for comparison.
        text = re.sub(r"<[^>]+>", "", inner)
        text = re.sub(r"\s+", " ", text).strip()
        return "" if text == norm_desc else match.group(0)

    return re.sub(r"<p>(.*?)</p>\s*", _replace, html, flags=re.DOTALL)


def render_readme_html(readme_md: str, md_renderer: MarkdownIt, description: str = "", book_path: str = "") -> tuple[str, bool]:
    """Render README markdown to HTML, truncating to the word limit.

    Strips redundant content that's already surfaced by the item page
    template: the first <h1> (title shown separately), the first italic
    "by ..." author line, and any <p>s whose text matches the metadata
    description. Sections that mirror the page metadata grid (Catalog
    entry, Shelf location) are stripped as whole <h2> blocks. The
    trailing "See metadata.yaml ..." paragraph is stripped because the
    template renders a styled link near the bottom of the page.

    If `book_path` is provided, relative <img src="..."> values are
    rewritten to point at the item's directory from the item-page
    location (../../{book_path}/{src}) so embedded images resolve
    correctly when the README HTML is embedded in wiki/items/{slug}.html.
    Absolute URLs and data/fragment URIs are left alone.
    """
    import re

    truncated_md, was_truncated = truncate_by_words(readme_md, README_WORD_LIMIT)
    html = md_renderer.render(truncated_md)

    # Strip the metadata-mirror block delimited by explicit HTML-comment
    # sentinels. By convention the README holds a "Catalog entry" (and
    # optional "Shelf location" / "Source") section bracketed by
    # `<!-- alexandria:metadata-start -->` and `<!-- alexandria:metadata-end -->`
    # — a human-readable mirror of metadata.yaml useful for standalone
    # browsing. The item page already renders those fields as a structured
    # grid, so we drop the entire delimited range from the wiki render.
    html = re.sub(
        r'<!--\s*alexandria:metadata-start\s*-->.*?<!--\s*alexandria:metadata-end\s*-->\s*',
        '',
        html,
        flags=re.DOTALL,
    )

    # Strip first <h1>...</h1> (the README's title is shown separately as the
    # item-page title).
    html = re.sub(r'<h1>.*?</h1>\n?', '', html, count=1)

    # Strip the first italic byline paragraph (author is shown separately on
    # the page via the metadata grid's role-aware "By" / "Directed by" / etc.
    # label). Matches both plain `<p><em>by X</em></p>` and role-aware forms
    # like `<p><em>Directed by X</em></p>` or `<p><em>Photographed by X</em></p>`.
    html = re.sub(
        r'<p><em>(?:\w+\s+)?[Bb]y\s.*?</em></p>\n?',
        '',
        html,
        count=1,
    )

    # Strip every <p> whose text matches the metadata description — handles
    # both the canonical template (description once near the top) and any
    # item whose README repeats the description (e.g., again after a photo).
    html = _strip_description_paragraphs(html, description)

    # Strip the trailing "See `metadata.yaml` ..." paragraph — the wiki template
    # renders a styled metadata link near the bottom of the page instead.
    html = re.sub(
        r'<p>See\s*<code>metadata\.yaml</code>\s*for the full catalog entry\.?</p>\n?',
        '',
        html,
    )

    html = _convert_kv_lists_to_dl(html)

    # Strip sections whose content is now surfaced in the page-level metadata
    # grid. Matches the <h2> and everything until the next <h2> or end of doc.
    for strip_h2 in ("Catalog entry", "Shelf location"):
        html = re.sub(
            rf'<h2>{re.escape(strip_h2)}</h2>.*?(?=<h2>|$)',
            '',
            html,
            flags=re.DOTALL,
        )

    # Strip the first standalone-image paragraph from the rendered README.
    # By convention, the item's README leads with `![title](photo.ext)` so
    # that the README itself reads standalone with a visual. The item page
    # already renders that image as the header-row thumbnail, so repeating
    # it inside the content block is redundant. Targets only a `<p>` whose
    # sole content is a single `<img>` so inline images (e.g., embedded in
    # a paragraph of prose) are left alone.
    html = re.sub(
        r'<p>\s*<img[^>]*>\s*</p>\n?',
        '',
        html,
        count=1,
    )

    # Rewrite relative image src values on any remaining images so they
    # resolve from the item-page location. The README lives at
    # {path}/README.md with images typically as siblings; the rendered
    # HTML is embedded in wiki/items/{slug}.html where those relative
    # paths would otherwise break. Absolute URLs, protocol-relative
    # URLs, fragments, data URIs, and root-absolute paths are left alone.
    if book_path:
        def _rewrite_img_src(match: re.Match) -> str:
            src = match.group(1)
            if src.startswith(("http://", "https://", "//", "#", "data:", "/")):
                return match.group(0)
            return f'src="../../{book_path}/{src}"'
        html = re.sub(r'src="([^"]+)"', _rewrite_img_src, html)

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
            # Attach thumbnail filename (if an image exists in the item
            # directory) so every view that renders the item can show it.
            thumb = find_item_thumbnail(library_path, book_path)
            if thumb:
                merged["thumb_filename"] = thumb
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
        "all",
        "by-author",
        "by-medium-format",
        "by-topic",
        "search",
    ]
    for sub in subdirs:
        (wiki_dir / sub).mkdir(exist_ok=True)

    # Copy stylesheet from tools/
    tools_dir = Path(__file__).parent
    css_src = tools_dir / "_wiki_style.css"
    css_dst = wiki_dir / "_assets" / "style.css"
    shutil.copy(css_src, css_dst)

    # Copy bundled fonts into wiki/_assets/fonts/ so @font-face URLs resolve
    fonts_src_dir = tools_dir / "fonts"
    fonts_dst_dir = wiki_dir / "_assets" / "fonts"
    fonts_dst_dir.mkdir(exist_ok=True)
    if fonts_src_dir.is_dir():
        for font_file in fonts_src_dir.iterdir():
            if font_file.is_file() and font_file.suffix.lower() == ".woff2":
                shutil.copy(font_file, fonts_dst_dir / font_file.name)

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
        templates.by_section_index(library, all_items, items_by_section)
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
            templates.section_page(section, sorted_books, library, all_items)
        )

    # Major-section pages (one per unique major_section value)
    major_groups: dict[str, list[dict]] = {}
    for item in all_items:
        major = item.get("major_section") or "Etc"
        major_groups.setdefault(major, []).append(item)
    for major, items in major_groups.items():
        major_slug = major.replace("/", "-").replace(" ", "-").lower()
        (wiki_dir / "by-section" / f"{major_slug}.html").write_text(
            templates.major_section_page(major, items, library, all_items)
        )

    # --- All ---
    (wiki_dir / "all" / "index.html").write_text(
        templates.all_index(library, all_items)
    )

    # --- By author/artist ---
    (wiki_dir / "by-author" / "index.html").write_text(
        templates.by_author_index(library, all_items)
    )

    # --- By medium & format ---
    (wiki_dir / "by-medium-format" / "index.html").write_text(
        templates.by_medium_format_index(library, all_items)
    )
    form_fmt_groups: dict[tuple[str, str], list[dict]] = {}
    for item in all_items:
        form = item.get("form", "digital")
        fmt = item.get("media_type", "unknown") or "unknown"
        form_fmt_groups.setdefault((form, fmt), []).append(item)
    for (form, fmt), items in form_fmt_groups.items():
        # Include removed items sorted after active items, matching section pages.
        sorted_items = sorted(
            items,
            key=lambda b: (
                b.get("status", "active") == "removed",
                b.get("title", "").lower(),
            ),
        )
        slug = templates._format_slug(form, fmt)
        (wiki_dir / "by-medium-format" / f"{slug}.html").write_text(
            templates.format_page(form, fmt, sorted_items, library, all_items)
        )

    # Form-level pages (all items of a form — physical / digital)
    form_groups_all: dict[str, list[dict]] = {}
    for item in all_items:
        form_all = item.get("form", "digital")
        form_groups_all.setdefault(form_all, []).append(item)
    for form_all, items in form_groups_all.items():
        (wiki_dir / "by-medium-format" / f"{form_all}.html").write_text(
            templates.form_page_all(form_all, items, library, all_items)
        )

    # --- By topic (Pass 2 placeholder) ---
    (wiki_dir / "by-topic" / "index.html").write_text(
        templates.topic_placeholder(library, all_items)
    )

    # --- Search page ---
    (wiki_dir / "search" / "index.html").write_text(
        templates.search_page(library, all_items)
    )

    # --- Collection journal ---
    (wiki_dir / "collection-journal").mkdir(exist_ok=True)
    journal_entries = parse_collection_context(library_path, md_renderer)
    (wiki_dir / "collection-journal" / "index.html").write_text(
        templates.collection_journal(library, all_items, journal_entries)
    )
    # Per-month filtered pages
    journal_months: dict[str, list[dict]] = {}
    for entry in journal_entries:
        date = entry.get("date", "")
        month_key = date[:7] if len(date) >= 7 else "undated"
        journal_months.setdefault(month_key, []).append(entry)
    for month_key, month_entries in journal_months.items():
        (wiki_dir / "collection-journal" / f"{month_key}.html").write_text(
            templates.collection_journal_month(library, all_items, month_key, month_entries)
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
                readme_html, readme_truncated = render_readme_html(
                    readme_md, md_renderer,
                    description=item.get("description", "") or "",
                    book_path=book_path,
                )

        # Load user notes from notes/ directory if present
        if status != "removed":
            item_notes = load_item_notes(library_path, book_path, md_renderer)

        # Thumbnail was already attached during collect_books; item_page
        # reads it from the item dict.
        thumb_filename = item.get("thumb_filename") if status != "removed" else None

        # Pass 2 hook (currently a no-op)
        narrative_enrich(item)

        (wiki_dir / "items" / f"{slug}.html").write_text(
            templates.item_page(item, readme_html, readme_truncated, library, all_items, item_notes, thumb_filename)
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
