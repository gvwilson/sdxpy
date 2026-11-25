# McCole

A brief orientation for this Quarto book template.

## Build layout

- The project's root `Makefile` uses `include mccole/mccole.mk` to get common
  targets.  Project-specific variables/targets should go under the line.
- Default target in `mccole/mccole.mk` lists available commands by looking
  for comments `## command: some text`.
  - `commands`: show available commands (default)
  - `site`: render HTML with Quarto
  - `pdf`: render PDF with Quarto
  - `serve`: preview the site locally
  - `publish`: publish the site
  - `update-mccole`: refresh `mccole` from the `mcq` remote
  - `slides`: rebuild the slides using Pandoc
  - `check`: check structure, spelling, etc.
    - `check-bib`: check bibliography
    - `check-links`: check Markdown links
    - `check-glossary`: check glossary references
    - `check-formatting`: check include formatting
    - `check-typos`: check spelling
  - `clean`: remove generated and cache files
- The project's `_quarto.yml` includes `mccole/mccole.yml` to get common
  definitions, then defines the `book` section with title, chapters, and
  appendices.

## Lua scripts (in mccole/)

- Filters (`mccole.yml` → `filters:`):
  - `links.lua`: resolves `@key` links
  - `nav.lua`: topbar navigation
  - `remove-empty-h1.lua`: drops the empty H1 on the home page
- Shortcodes (`mccole.yml` → `shortcodes:`)
  - `glossary.lua` (`g`)
  - `inc-quarto.lua` (`inc`)
  - `inc-noh1.lua` (FIXME)
  - `i.lua` (FIXME)
  - `issue.lua` (FIXME)
  - `fixme.lua`, (FIXME)
  - `exercise.lua` (FIXME)
  - `linecount.lua` (FIXME)
- Include machinery
  - `inc-quarto.lua` (Quarto/site)
  - `inc-pandoc.lua` (pandoc/slides)
  - `inc-utils.lua` (shared read/scrub/language helpers)
- Checkers
  - `check-bib.lua`
  - `check-links.lua`
  - `check-glossary.lua`
  - `check-formatting.lua`
- Other:
  - `publish.lua`: used by `make publish`
  - `utils.lua`: shared helpers for the checkers

## Shortcodes

- `{{< g key "display" >}}`:
  link to the glossary entry `key` (`display` optional; defaults to `key`)
- `{{< inc file.py mark=name omit=name head="N" >}}`:
  include a code file (see "File inclusion")
- `{{< inc-noh1 file.md >}}`:
  include a Markdown file, stripping its first H1
  (used to inline `LICENSE.md` etc. under a chapter's own H1)
- `{{< i "display" "term" >}}`:
  index entry; renders `display`, the term is a no-op for now
- `{{< issue 123 >}}`:
  link to issue 123 in the book's repo
- `{{< fixme "text" >}}`:
  bold "FIXME:" label + text
- `{{< exercise FILENAME >}}`:
  include an exercise file (relative to the containing file),
  stripping its H1 and re-emitting under H3
- `{{< linecount file >}}`:
  emit the number of lines in `file` (project-root relative)

## Home page

- `index.qmd` begins with `# {.unnumbered}` (an empty heading) so the home page
  is unnumbered. `remove-empty-h1.lua` deletes the empty `<h1>` this produces.

## File inclusion

- `{{< inc … >}}` resolves the filename relative to the project root, not the
  current file
- `mark=lbl` emits only the region between `# mccole:lbl` and `# mccole:/lbl`.
- `omit=lbl` removes that region
- `head="N"` keeps the first N lines
- Lines marked as bugs are erased:
  `# BUG …`, `// BUG …`, `<!-- BUG … -->`, `/* BUG … */`, `-- BUG …`
- Language from extension:
  `py`→python, `sh`→bash, `sql`, `js`→javascript, `css`, `html`

## Divs and special elements

- `::: {.note}` … `:::` creates a note box
  (gray, "Note" heading via CSS)
  - Add `data-title="…"` to override the heading
- `::: {.syllabus}` … `:::` creates a syllabus box
  (gray, "Syllabus" heading via CSS)
- `::: {.row}` wrapping `::: {.col-N}` is a 12-column flex grid
  - E.g. three `::: {.col-4}` make three equal columns
- `.left`, `.center`, `.right` classes: text alignment
- `> quoted text` followed by `> <cite>author</cite>` creates a quotation
  - CSS puts the author on its own line with an em-dash prefix

## Boilerplate chapters

- `license/index.qmd`, `conduct/index.qmd`, etc. include `LICENSE.md`,
  `CODE_OF_CONDUCT.md`, etc. via `{{< inc-noh1 … >}}`
  - Used to inline the files GitHub conventionally expects so that
    content doesn't have to be duplicated

## Bibliography

- BibTeX in `bibliography/references.bib`
- `bibliography/index.qmd` has `nocite: @*` and `::: {#refs}` to render all entries.
- Style: `csl: mccole/book.csl`
- Cite with `[@key1,@key2]`

## Glossary

- `glossary/index.qmd` is a definition list.
  Each entry is `<span id="key">term</span>` on one line
  then `:   definition` on the next.
- Reference with `{{< g key "display" >}}`.

## Checking (`make check`)

- `check-bib`: every citation has a bibliography entry
- `check-links`: every `@key` resolves in `config/links.md`
- `check-glossary`: every glossary reference resolves
- `check-formatting`: no adjacent `{{< inc >}}` lines and no four-colon callouts
  - If `inc` shortcode is used on consecutive lines, they are interpreted as a paragraph
- `check-typos`: runs `typos -c config/typos.toml`
- `check-html`: basic accessibility checks on the built HTML
  - exercised against `fixtures/` via `make check-fixtures`

## Updating mccole/

- `make update-mccole` replaces `mccole/` with content from template repo
  - Deletes old local content rather than doing a `git merge`, so be careful

## config/ directory (project-specific)

- `config/links.md`: link definitions (`[key]: url`)
- `config/typos.toml`: spelling exceptions

## Links

- Define `[key]: url` in `config/links.md`.
- Reference `[text](@key)` in content
- `links.lua` resolves `@key` and errors on an unknown key

## Slides

- `make slides` builds `slides.qmd` and `*/slides.qmd` with pandoc, not Quarto
  - Clumsy, but simpler than trying to wedge slides files into `_quarto.yml`
- Uses `--lua-filter=mccole/inc-pandoc.lua` (so `{{< inc >}}` works),
  `--syntax-highlighting=tango`, and `--mathjax`

## PDF

- `make pdf` runs `quarto render --to pdf`
  - Document class is `scrbook` (`format.pdf.documentclass` in `mccole.yml`)

## Styling

- `mccole/mccole-book.css`: for web site
- `mccole/mccole-slides.css`: on top of reveal.js definitions
- `mccole/tango.css`: syntax highlighting
  - Used in web site; pandoc inlines content in slides
