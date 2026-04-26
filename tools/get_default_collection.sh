#!/bin/bash
# Quickly retrieve the stored default collection for the
# /coll-update-from-latest-alexandria skill. Consolidates the state-file
# read, path verification, and collection_name lookup into one call so
# the skill doesn't have to issue three separate tool invocations.
#
# Output on success (exit 0) — two lines on stdout:
#   line 1: absolute path to the collection
#   line 2: collection_name (from the collection's .collection-index.yaml)
#
# Exit non-zero:
#   1 = no state file
#   2 = state file empty or path no longer a directory
#   3 = directory exists but has no .collection-index.yaml
#
# Must be run from the alexandria repo root (cwd-relative state path).

set -euo pipefail

STATE_FILE=".claude/state/default-collection"

if [ ! -f "$STATE_FILE" ]; then
    exit 1
fi

COLLECTION_PATH=$(cat "$STATE_FILE")

if [ -z "$COLLECTION_PATH" ] || [ ! -d "$COLLECTION_PATH" ]; then
    exit 2
fi

INDEX_FILE="$COLLECTION_PATH/.collection-index.yaml"

if [ ! -f "$INDEX_FILE" ]; then
    exit 3
fi

# Pull the collection_name line and strip the key + optional surrounding quotes.
COLLECTION_NAME=$(grep -E '^collection_name:' "$INDEX_FILE" | head -1 \
    | sed -E 's/^collection_name:[[:space:]]*//; s/^"(.*)"$/\1/; s/^'\''(.*)'\''$/\1/' \
    | tr -d '\r')

if [ -z "$COLLECTION_NAME" ]; then
    COLLECTION_NAME="(unnamed)"
fi

printf "%s\n%s\n" "$COLLECTION_PATH" "$COLLECTION_NAME"
