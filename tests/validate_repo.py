#!/usr/bin/env python3
"""Validate alexandria repo content: YAML syntax, internal links, stale references."""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STALE_TERMS = ["sota-tracker", "build-tracker", "tracker book"]
FAILURES = []


def fail(file: Path, message: str):
    rel = file.relative_to(REPO_ROOT)
    FAILURES.append(f"  {rel}: {message}")


def extract_yaml_blocks(text: str) -> list[tuple[int, str]]:
    """Return (line_number, content) for each ```yaml code block."""
    blocks = []
    in_block = False
    block_lines = []
    block_start = 0
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```yaml"):
            in_block = True
            block_start = i
            block_lines = []
        elif in_block and line.strip().startswith("```"):
            in_block = False
            blocks.append((block_start, "\n".join(block_lines)))
        elif in_block:
            block_lines.append(line)
    return blocks


def check_yaml_blocks(file: Path):
    """Validate YAML code blocks parse without errors."""
    try:
        import yaml
    except ImportError:
        return  # skip if pyyaml not installed

    text = file.read_text()
    for line_num, block in extract_yaml_blocks(text):
        # Skip blocks with template placeholders
        if "{" in block and "}" in block:
            continue
        try:
            yaml.safe_load(block)
        except yaml.YAMLError as e:
            fail(file, f"invalid YAML in code block at line {line_num}: {e}")


def check_stale_references(file: Path):
    """Check for stale naming references."""
    text = file.read_text()
    for term in STALE_TERMS:
        for i, line in enumerate(text.splitlines(), 1):
            if term in line.lower():
                fail(file, f"stale reference '{term}' at line {i}")


def check_internal_links(file: Path):
    """Check that relative markdown links point to files that exist."""
    text = file.read_text()
    # Match [text](path) but skip http/https URLs and anchors
    link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    for i, line in enumerate(text.splitlines(), 1):
        for match in link_pattern.finditer(line):
            target = match.group(2)
            # Skip URLs, anchors, and mail links
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Strip anchor from path
            target_path = target.split("#")[0]
            if not target_path:
                continue
            # Resolve relative to the file's directory
            resolved = (file.parent / target_path).resolve()
            if not resolved.exists():
                fail(file, f"broken link [{match.group(1)}]({target}) at line {i}")


def main():
    md_files = sorted(REPO_ROOT.rglob("*.md"))
    md_files = [f for f in md_files if ".git" not in f.parts]

    print(f"Validating {len(md_files)} markdown files...\n")

    for f in md_files:
        check_stale_references(f)
        check_internal_links(f)
        check_yaml_blocks(f)

    if FAILURES:
        print(f"FAILED — {len(FAILURES)} issue(s):\n")
        for msg in FAILURES:
            print(msg)
        sys.exit(1)
    else:
        print("PASSED — no issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
