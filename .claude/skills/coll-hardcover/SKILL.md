# /coll-hardcover

A shortcut for cataloging a hardcover item. Invokes `/coll-physical` with
`media_type` pre-set to `text:hardcover`, so you don't need to answer the media type
question during acquisition.

## What this skill does

Invoke `/coll-physical` and, when generating `metadata.yaml` for each confirmed item,
set `media_type: text:hardcover` automatically. Skip the media type question for
single-item photos. For shelf photos, use `text:hardcover` as the shelf-level default
without prompting (users can still override per item during confirmation if some
items on the shelf aren't actually hardcovers).

Everything else — library context detection, photo workflow, manual entry, confirmation,
enrichment, section classification, directory creation, index update, /coll-notes
invocation — is handled by `/coll-physical`. This skill is a thin wrapper for users
who know they're adding hardcover items and want to skip one question.

## When to use this

- You're cataloging a shelf of hardcover items and want to skip the media type
  question for the whole batch
- You want a predictable shortcut instead of the more general `/coll-physical` prompt

For any other physical media type, use `/coll-physical` directly and answer the media
type question with your preferred value.

## What this does not do

- Does not bypass any of `/coll-physical`'s other behavior (photos are still taken,
  candidates still confirmed, enrichment still opt-in)
- Does not assume every item on a shelf is a hardcover — per-item override still
  available during confirmation
