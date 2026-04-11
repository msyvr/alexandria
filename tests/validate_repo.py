#!/usr/bin/env python3
"""Validate alexandria repo content: YAML syntax, internal links, stale references, Python syntax."""

import ast
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
    """Check for stale naming references. Skips fenced code blocks."""
    text = file.read_text()
    in_code_block = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        lower = line.lower()
        for term in STALE_TERMS:
            if term in lower:
                fail(file, f"stale reference '{term}' at line {i}")


def check_internal_links(file: Path):
    """Check that relative markdown links point to files that exist.

    Skips links inside fenced code blocks and links with template placeholders
    (containing `{` or `}` in the target).
    """
    text = file.read_text()
    link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    in_code_block = False
    for i, line in enumerate(text.splitlines(), 1):
        # Track fenced code blocks (```...```) to skip links inside them
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        for match in link_pattern.finditer(line):
            target = match.group(2)
            # Skip URLs, anchors, and mail links
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Skip template placeholders
            if "{" in target or "}" in target:
                continue
            # Strip anchor from path
            target_path = target.split("#")[0]
            if not target_path:
                continue
            # Resolve relative to the file's directory
            resolved = (file.parent / target_path).resolve()
            if not resolved.exists():
                fail(file, f"broken link [{match.group(1)}]({target}) at line {i}")


def check_python_syntax(file: Path):
    """Parse a Python file with ast to catch syntax errors."""
    try:
        source = file.read_text()
        ast.parse(source, filename=str(file))
    except SyntaxError as e:
        fail(file, f"syntax error at line {e.lineno}: {e.msg}")


def main():
    md_files = sorted(REPO_ROOT.rglob("*.md"))
    md_files = [f for f in md_files if ".git" not in f.parts]

    py_files = sorted(REPO_ROOT.rglob("*.py"))
    py_files = [
        f for f in py_files
        if ".git" not in f.parts and ".venv" not in f.parts and "__pycache__" not in f.parts
    ]

    print(f"Validating {len(md_files)} markdown files and {len(py_files)} Python files...\n")

    for f in md_files:
        check_stale_references(f)
        check_internal_links(f)
        check_yaml_blocks(f)

    for f in py_files:
        check_python_syntax(f)

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
