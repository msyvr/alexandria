## Fonts and typography

The wiki ships with its own fonts. Alexandria copies them into every
collection's `wiki/_assets/fonts/` directory on regeneration, and the
stylesheet loads them via `@font-face`. This keeps the rendering identical
on every machine — Mac, Linux, Windows, old browsers, new browsers — and
keeps the collection fully offline: no CDN lookups, no network calls, no
dependency on whatever fonts the user happens to have installed.

### What ships with the wiki

Five [WOFF2](https://en.wikipedia.org/wiki/Web_Open_Font_Format) files,
~120 KB in total, under `tools/fonts/` in the alexandria repo:

| Family | Weights included | Role in the wiki |
| ------ | ---------------- | ---------------- |
| **Source Serif 4** | 300 (light), 300 italic, 700 (bold) | Body text, descriptions, titles on the item-detail page — the long-form serif |
| **Inter**       | 300 (light), 400 (regular), 600 (semibold) | Small caps labels (nav, sort labels, major-group headings, item-card titles, format lines, "FROM THE ITEM DIRECTORY" links) |

Both families are distributed under the
[SIL Open Font License 1.1](https://scripts.sil.org/OFL) — free to use,
bundle, and redistribute, no tracking, no subscription. The specific files
are the
[@fontsource](https://fontsource.org/) builds of each family, which are
just repackaged Google Fonts source files optimized for self-hosting.

### Why self-host

A few reasons, roughly in order of how much they matter:

1. **Consistency.** System fonts vary across operating systems. Playfair
   Display on a Mac renders differently than Source Serif 4 on a
   Windows box, and a Linux box may not have Playfair at all and fall
   back to a generic serif. Self-hosting pins the exact glyphs so your
   collection looks the same everywhere.
2. **Offline / ownership.** Loading fonts from a CDN means every visit
   phones home to Google or wherever. You lose the ability to browse
   without internet, and someone else knows when you're reading your
   collection. Self-hosting is the ownership-consistent choice.
3. **No surprise breakage.** A font URL can change or go away. A font
   file sitting in your collection directory does not.

### How the stylesheet uses them

`tools/_wiki_style.css` declares the fonts with `@font-face` and then
falls back to system fonts if the WOFF2 files are missing or corrupt:

```css
body {
  font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
}
.axes-nav a, h2.major-heading, .back-link, .sort-control {
  font-family: "Inter", system-ui, -apple-system, sans-serif;
}
```

If a visitor's browser somehow can't load `source-serif-4-300.woff2`,
the stack falls through to `Georgia` (installed on almost every system),
then `Times New Roman`, then a generic serif. The rendering degrades
but stays readable.

### Swapping a font

If you want to use different fonts:

1. **Pick two fonts** licensed for self-hosting. Fontsource's
   [fontsource.org](https://fontsource.org/) is the easiest source —
   every family listed there is OFL-licensed and ready to copy.
2. **Download WOFF2 files** for each weight you want to ship. Most
   families expose a `latin-400-normal.woff2`, `latin-400-italic.woff2`,
   and a heavier weight (e.g. `latin-600-normal.woff2` or `-700-`).
3. **Drop them into `tools/fonts/`** using short, descriptive names —
   e.g. `my-serif-400.woff2`, `my-serif-700.woff2`.
4. **Update the `@font-face` block at the top of
   `tools/_wiki_style.css`** — change the `font-family` names and the
   `url()` paths.
5. **Update the font stacks further down the same stylesheet** so the
   new families are first, with the old fallbacks after.
6. **Regenerate the wiki** via `/coll-menu` → regenerate or
   `uv run python tools/generate_wiki.py <collection-path>`. The
   generator copies the new files into every collection's
   `wiki/_assets/fonts/` directory.

The whole change is ~10 lines of CSS and a directory of files. No code
changes.

### If you just want to tweak rather than swap

Each `font-size`, `letter-spacing`, and `font-weight` in
`tools/_wiki_style.css` is a one-line edit. Anchor sizes in `em` (relative
to the root `html` font-size) so a single change to `html { font-size: … }`
scales the whole wiki proportionally. The root size is `100%` by default
(matching the browser default — typically 16 px) — bumping it to e.g.
`90%` makes everything about 10% smaller, `110%` about 10% larger.

### Why these two families specifically

Source Serif 4 is Adobe's humanist serif, designed by Frank Grießhammer
for on-screen reading at a wide weight range (200–900). The bundled
Light (300) weight gives the catalog a softer, lower-contrast
reading feel than a Regular-weight serif would; it pairs cleanly with
Inter Light in the sans-serif role for labels and content, keeping the
whole page tonally consistent.

Inter was designed for screens at small sizes. It's the dominant
"modern clean sans" on the web because it stays legible down to 11 px
and is available in many weights. In alexandria it's used in small caps
for axes nav, sort labels, major-group headings, item-card titles, and
format-line text — anywhere a structural label wants to read as
informational rather than literary.

### Further reading

- [fontsource.org](https://fontsource.org/) — self-hostable open-source
  fonts, packaged for download.
- [SIL Open Font License](https://scripts.sil.org/OFL) — the license
  almost every bundled open font ships under. Short and readable.
- [CSS @font-face](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face)
  — MDN reference for the CSS mechanism the wiki uses.
- [Font-display strategies](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)
  — why the wiki uses `font-display: swap` (fall back to system fonts
  during the moment it takes to load the bundled file).
