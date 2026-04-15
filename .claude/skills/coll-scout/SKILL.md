# /coll-scout

Import an existing scout into the collection. Use this when you have a scout that was
built independently (outside any collection) and you want to add it to your collection
as a cataloged item.

To create a new scout from scratch inside the collection, use `/coll-new-scout` instead.

## Before starting

Detect the collection context by walking up from the current directory looking for
`.collection-index.yaml`. If not found, explain that /coll-scout must run inside a
collection and offer to help create one with /coll-build-new-collection.

## The workflow

1. **Ask for the scout's location.** The user provides the path to an existing scout
   directory. Verify it exists and looks like a scout (has `data/entries.yaml` or
   similar scout structure).

2. **Check for metadata.yaml.** If the scout already has a `metadata.yaml` with
   universal fields (it was built by `/coll-new-scout` and may have been in a
   different collection), read it and use those fields as defaults. If it doesn't
   have one (it was built before the universal shape existed, or manually), gather
   the required fields from the user or extract them from the scout's files.

3. **Build or update metadata.yaml.** Ensure all required universal fields are
   present:

   ```yaml
   slug: "{generated or existing}"
   title: "{from the scout's README or user-provided}"
   book_type: "scout"
   section: "{propose based on the scout's topic}"
   description: "{from existing metadata or the scout's scope}"
   date_added: "{today — when it enters THIS collection}"
   form: "digital"
   media_type: "text:markdown"
   status: "active"
   settled: false   # or true if the user says it's already settled
   ```

4. **Determine placement.** Propose a section based on existing collection sections
   and the scout's topic. Confirm with the user.

5. **Move or copy the scout directory** into the collection at
   `{collection}/{section}/{slug}/`. Ask the user: move (relocates the original)
   or copy (keeps the original in place)? Default recommendation: move, since
   having two copies of a live scout creates confusion about which one is
   authoritative.

6. **Generate slug.** If the scout doesn't already have a slug, generate one from
   the title. Check uniqueness within the collection.

7. **Update `.collection-index.yaml`** with the scout's universal fields.

8. **Regenerate the wiki** so the scout appears in all views.

9. **Invoke `/coll-notes`** to log the import.

10. **Tell the user about scout maintenance.** Since the scout is now in the
    collection, explain:

    > Your scout is now at `{section}/{slug}/`. For quick operations (checking
    > status, settling, adding a single entry), you can work from the collection
    > directory. For substantive work (running critique, adding many entries,
    > restructuring categories), it works best to open a separate Claude Code
    > session from the scout's own directory:
    >
    > ```
    > cd ~/my-collection/{section}/{slug}
    > claude
    > ```
    >
    > The collection's `/coll-*` commands are available from inside the scout
    > directory because it's inside the collection.

## What /coll-scout does NOT do

- Does not create a new scout (that's `/coll-new-scout`)
- Does not modify the scout's content or structure (only adds/updates metadata.yaml
  and places it in the collection)
- Does not duplicate the scout if "move" is chosen — the original location is emptied

## Adapting to the user

If the user says something like "I have a scout I built earlier" or "I want to add
an existing scout to my collection," this is the right skill. If they say "I want to
build a new scout" or "create a scout about [topic]," redirect to `/coll-new-scout`.
