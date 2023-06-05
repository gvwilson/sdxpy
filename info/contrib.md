## Formatting {: #contrib-formatting}

This material uses [Ivy][ivy] with some custom extensions;
run `make` in the root directory to get a list of available commands.
Some of these rely on scripts in the `./bin/` directory.

### Chapters and Appendices

1.  Each chapter or appendix has a unique slug such as `topic`.
    Its text lives in <code>./<em>lang</em>/src/<em>topic</em>/index.md</code>,
    and there is an entry for it in the `chapters` or `appendices` list in `./config.py`
    (which control ordering).

1.  Each `index.md` file starts with a YAML header in triple dashes.
    This header must include the key `title:` with the page's title.

1.  Each section within a page must use a heading like this:

    ```markdown
    ## Some Title {: #topic-sometitle}
    ```

    This creates an `h2`-level heading with the HTML ID `topic-sometitle`.
    Use the page's slug instead of `topic` and a single unhyphenated work
    in place of `sometitle`.

1.  To create a cross-reference to a chapter or appendix write:

    ```markdown
    [%x topic %]
    ```

    where `topic` is the slug of the chapter being referred to.
    This shortcode is converted to `Chapter N` or `Appendix N`
    or the equivalent in other languages.
    Please only refer to chapters or appendices, not to sections.

### External Links

1.  The table of external links lives in `./info/links.yml`.
    Please add entries as needed,
    or add translations of URLs to existing entries using
    a two-letter language code as a key.

1.  To refer to an external link write:

    ```markdown
    [body text][link_key]
    ```

Please do *not* add links directly with `[text](http://some.url)`:
keeping the links in `./info/links.yml` ensures consistency
and makes it easier to create a table of external links.

### Code Inclusions

1.  To include an entire file as a code sample write:

    ```markdown
    [% inc file="some_name.py" %]
    ```

    The file must be in or below the directory containing the Markdown file.

1.  To include only part of a file write:

    ```markdown
    [% inc file="some_name.py" keep="some_key" %]
    ```

    and put matching tags in the file like this:

    ```markdown
    # [some_key]
    …lines of code…
    # [/some_key]
    ```

1.  To include several files (such as a program and its output) write:

    ```markdown
    [% inc pat="some_stem.*" fill="py out" %]
    ```

    This includes `some_stem.py` and `some_stem.out` in that order.

### Figures

1.  Put the image file in the same directory as the chapter or appendix
    and use this to include it:

    ```markdown
    [% figure
       slug="topic-someword"
       img="filename.svg"
       caption="Short sentence-case caption."
       alt="Long text describing the figure for the benefit of visually impaired readers."
    %]
    ```

    Please use underscores in filenames for consistency.

1.  To refer to a figure write:

    ```markdown
    [%f topic-someword %]
    ```

    This is converted to `Figure N.K`.

1.  Use [diagrams.net][diagrams] to create SVG diagrams
    using the "sketch" style and a 12-point Comic Sans font.

1.  Avoid screenshots:
    making them display correctly in print is difficult.

### Tables

The Markdown processor used by [Ivy][ivy] doesn't support attributes on tables,
so we must do something a bit clumsy.

1.  To create a table write:

    ```markdown
    <div class="table" id="topic-someword" caption="Short sentence-case caption." markdown="1">
    | Left | Middle | Right |
    | ---- | ------ | ----- |
    | blue | orange | green |
    | mars | saturn | venus |
    </div>
    ```

1.  To refer to a table write:

    ```markdown
    [%t topic-someword %]
    ```

    This is converted to `Table N.K`.

### Bibliography

1.  The BibTeX bibliography lives in `./info/bibliography.bib`.
    Please add entries as needed;
    you may find <https://doi2bib.org> useful for creating entries.
    Please format keys as `Author1234`,
    where `Author` is the first author's family name
    and `1234` is the year of publication.
    (Use `Author1234a`, `Author1234b`, etc. to resolve conflicts.)

1.  To cite bibliography entries write:

    ```markdown
    [%b key1 key2 key3 %]
    ```

### Glossary

1.  The glossary lives in `./info/glossary.yml` and uses [Glosario][glosario] format.

1.  When translating the glossary,
    please add definitions and acronyms under a two-letter language key
    rather than duplicating entries.
    Please do *not* translate entries' `key` values.

1.  To cite glossary entries write:

    ```markdown
    [%g some_key "text for document" %]
    ```

### Index

1.  To create a simple index entry write:

    ```markdown
    [%i "index text" %]body text[%/i%]
    ```

1.  Separate multiple index entries with semi-colons:

    ```markdown
    [%i "first; second; third" %]body text[%/i%]
    ```

1.  Create sub-entries using `!`:

    ```markdown
    [%i "major!minor" %]body text[%/i%]
    ```

### Minor Formatting

1.  To continue a paragraph after a code sample write:

    ```
    text of paragraph
    which can span multiple lines
    {: .continue}
    ```

    This has no effect on the appearance of the HTML,
    but prevents an unwanted paragraph indent in the PDF version.

1.  To create a callout box, use:

    ```
    <div class="callout" markdown="1">

    ### Title of callout

    text of callout

    </div>
    ```

    Use "Sentence case" for the callout's title,
    and please put blank lines before and after the opening and closing `<div>` markers.
    You *must* include `markdown="1"` in the opening `<div>` tag
    to ensure that Markdown inside the callout is processed.

## Building the HTML

1.  Pages use the template in `lib/mccole/templates/node.ibis`,
    which includes snippets from the same directory.

1.  Our CSS is in `lib/mccole/resources/mccole.css`.
    We also use `lib/mccole/resources/tango.css` for styling code fragments.
    We do *not* rely on any JavaScript in our pages.

1.  To produce HTML, run `make build` in <code>./<em>lang</em></code>
    to update the files in <code>./<em>lang</em>/docs</code>.
    You can also run `make serve` to preview files locally
    or `make lint` to check for common errors.

## Building the PDF

We use LaTeX to build the PDF version of this book.
you will need these packages with `tlmgr` in order to build the PDF:

-   `babel-english`
-   `babel-greek`
-   `cbfonts`
-   `enumitem`
-   `greek-fontenc`
-   `keystroke`
-   `listings`
-   `textgreek`
-   `tocbibind`
