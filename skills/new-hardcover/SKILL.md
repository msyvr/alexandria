# /new-hardcover

A shortcut for cataloging a hardcover book. Invokes `/new-physical` with
`media_type` pre-set to `text:hardcover`, so you don't need to answer the media type
question during acquisition.

## What this skill does

Invoke `/new-physical` and, when generating `metadata.yaml` for each confirmed book,
set `media_type: text:hardcover` automatically. Skip the media type question for
single-book photos. For shelf photos, use `text:hardcover` as the shelf-level default
without prompting (users can still override per book during confirmation if some
books on the shelf aren't actually hardcovers).

Everything else — library context detection, photo workflow, manual entry, confirmation,
enrichment, section classification, directory creation, index update, /take-notes
invocation — is handled by `/new-physical`. This skill is a thin wrapper for users
who know they're adding hardcover books and want to skip one question.

## When to use this

- You're cataloging a shelf of hardcover books and want to skip the media type
  question for the whole batch
- You want a predictable shortcut instead of the more general `/new-physical` prompt

For any other physical media type, use `/new-physical` directly and answer the media
type question with your preferred value.

## What this does not do

- Does not bypass any of `/new-physical`'s other behavior (photos are still taken,
  candidates still confirmed, enrichment still opt-in)
- Does not assume every book on a shelf is a hardcover — per-book override still
  available during confirmation
