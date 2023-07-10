# Contributing

Contributions are very welcome;
please contact us by email or by filing an issue on this site.
All contributors must abide by our Code of Conduct.

## FAQ

Why don't the examples connect with each other? For example, why don't they build toward a complete minimal IDE?

:   It was tempting, but my attempts to do this in the past have never gone well.
    First, it makes maintenance much more difficult
    because a change in an early chapter may have knock-on effects on several subsequent chapters.
    Second, it constraints what is taught and in what order:
    if the examples are independent of each other,
    instructors can pick and choose the pieces that are most relevant to their audience and goals.

Can I contribute a chapter?

:   Absolutely, and if enough people do that we will publish a second volume.
    Some things I'd particularly like to see are:

    -   An object-relational mapper to show people how tools like [SQLAlchemy][sqlalchemy] work
        (#45).
    -   A discrete event simulator to show people how tools like [SimPy][simpy] work
        and to explore co-operative concurrency using generators
        (#56).
    -   An issue-tracking system, mostly to show how workflow management and authentication work
        (#82).
    -   Another build system that uses publish/subscribe instead of the top-down approach of [%x build %]
        (#83).
    -   A fuzz tester that uses some of the ideas from [Zeller2023]
        (#84).
    -   A package installer to complement the package manager of [%x pack %]
        (#121).
    -   A file compression tool like `zip`
        (#144).
    -   A database that uses B-trees instead of a log for storage
        (#151).

## Making Decisions

This project uses [Martha's Rules][marthas_rules] for consensus decision making:

1.  Before each meeting, anyone who wishes may sponsor a proposal by filing an
    issue in the GitHub repository tagged "proposal".  People must file proposals
    at least 24 hours before a meeting in order for them to be considered at that
    meeting, and must include:
    -   a one-line summary (the subject line of the issue)
    -   the full text of the proposal
    -   any required background information
    -   pros and cons
    -   possible alternatives

2.  A quorum is established in a meeting if half or more of voting members are
    present.

3.  Once a person has sponsored a proposal, they are responsible for it.  The
    group may not discuss or vote on the issue unless the sponsor or their
    delegate is present.  The sponsor is also responsible for presenting the
    item to the group.

4.  After the sponsor presents the proposal, a "sense" vote is cast for the
    proposal before any discussion:
    -   Who likes the proposal?
    -   Who can live with the proposal?
    -   Who is uncomfortable with the proposal?

5.  If everyone likes or can live with the proposal, it passes immediately.

6.  If most of the group is uncomfortable with the proposal, it is postponed for
    further rework by the sponsor.

7.  Otherwise, members who are uncomfortable can briefly state their objections.
    A timer is then set for a brief discussion moderated by the facilitator.
    After 10 minutes or when no one has anything further to add (whichever comes
    first), the facilitator calls for a yes-or-no vote on the question: "Should
    we implement this decision over the stated objections?"  If a majority votes
    "yes" the proposal is implemented.  Otherwise, the proposal is returned to
    the sponsor for further work.

## Formatting

This material uses [Ark][ark] with some custom extensions;
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

The Markdown processor used by [Ark][ark] doesn't support attributes on tables,
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
    [key1 key2 key3]
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

[ark]: https://www.dmulholl.com/docs/ark/main/
[glosario]: https://glosario.carpentries.org/
[marthas_rules]: https://journals.sagepub.com/doi/10.1177/088610998600100206
[simpy]: https://simpy.readthedocs.io/
[sqlalchemy]: https://www.sqlalchemy.org/
