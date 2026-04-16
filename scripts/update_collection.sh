#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "usage: $0 <collection_path>" >&2
    exit 1
fi

COLLECTION="$1"
REPO="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -f "$COLLECTION/.collection-index.yaml" ]; then
    echo "error: $COLLECTION does not contain .collection-index.yaml" >&2
    exit 1
fi

mkdir -p "$COLLECTION/.claude/skills" "$COLLECTION/tools"

echo "Copying skills..."
cp -R "$REPO/.claude/skills/." "$COLLECTION/.claude/skills/"

echo "Copying tools..."
cp -R "$REPO/tools/." "$COLLECTION/tools/"

echo "Copying pyproject.toml..."
cp "$REPO/pyproject.toml" "$COLLECTION/pyproject.toml"

echo "Syncing dependencies..."
( cd "$COLLECTION" && uv sync )

echo "Regenerating wiki..."
( cd "$COLLECTION" && uv run python tools/generate_wiki.py . )

echo "Done."
