# /new-paperback

A shortcut for cataloging a paperback book. Invokes `/new-physical` with
`media_type` pre-set to `text:paperback`, so you don't need to answer the media type
question during acquisition.

## What this skill does

Invoke `/new-physical` and, when generating `metadata.yaml` for each confirmed book,
set `media_type: text:paperback` automatically. Skip the media type question for
single-book photos. For shelf photos, use `text:paperback` as the shelf-level default
without prompting (users can still override per book during confirmation).

Everything else — library context detection, photo workflow, manual entry, confirmation,
enrichment, section classification, directory creation, index update, /take-notes
invocation — is handled by `/new-physical`. This skill is a thin wrapper for users
who know they're adding paperback books.

## When to use this

- You're cataloging a shelf of paperbacks and want to skip the media type question
- You want a predictable shortcut for the common case

For any other physical media type, use `/new-physical` directly.

## What this does not do

- Does not bypass any of `/new-physical`'s other behavior
- Does not assume every book on a shelf is a paperback — per-book override still
  available during confirmation
