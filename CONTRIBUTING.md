# Contributing

Contributions are very welcome;
please contact us by email or by filing an issue on this site.
All contributors must abide by our Code of Conduct.

## FAQ

What sort of feedback would be useful?

:   Everything is welcome, but what would help most is:

    1.  Fixes for mistakes in the code, the descriptions, or the formatting.
        All of the examples run and all of the tests pass,
	but that doesn't guarantee they're correct.
    1.  Reports of continuity errors,
        e.g.,
	places where a concept is used before it is explained.
    1.  Suggestions for new diagrams, or for ways to improve existing ones.
    1.  New or clearer summary points for each chapter's syllabus.
    1.  More or better exercises.
        "This is too hard" or "this is unclear" helps as well.

Why don't the examples connect with each other?
For example, why don't they build toward a complete minimal IDE?

:   It was tempting, but attempts to do this in the past have not gone well.
    First, it makes maintenance much more difficult
    because a change in an early chapter may have knock-on effects on several subsequent chapters.
    Second, it constrains what is taught and in what order:
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

Do you need any programming assistance?

:   Yes—please see the [issue tracker][book_issues].

Why did you build your own production pipeline instead of using
[GitBook][gitbook], [Quarto][quarto], [Jupyter Book][jupybook],
or some other existing tool?

:   I've written or edited books with those tools and others like them,
    and found them more frustrating than helpful.
    For example,
    the code samples in this book often show one or two methods from a class
    rather than the whole class;
    there is no easy way to do this with tools built on computational notebooks.
    That said,
    I'm sure other people will find this book's tooling frustrating,
    and suggestions for improving it are welcome.

Why is this book free to read online?

:   Because I would rather be able to fix errata
    than have people torrenting out-of-date pirated PDFs.

Why are the royalties going to charity?

:   The [Red Door Family Shelter][red_door] and places like it
    have always been short of money and resources,
    and the COVID-19 pandemic only made matters worse.
    They do more good on the average Tuesday than most of us do in a year
    (or a lifetime);
    I'm glad to be able to help however I can.

## Making Decisions

This project uses [Martha's Rules][marthas_rules] for consensus decision making:

1.  Before each meeting, anyone who wishes may sponsor a proposal by filing an
    issue in the GitHub repository tagged "comm-proposal".  People must file proposals
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

This material uses [Ark][ark] with some custom extensions in `./lib/mccole/extensions`.
Please run `make` in the root directory to get a list of available commands,
several of which on scripts in the `./lib/mccole/bin/` directory.

### Chapters and Appendices

1.  Each chapter or appendix has a unique slug such as `topic`.
    Its text lives in <code>./src/<em>topic</em>/index.md</code>,
    and there is an entry for it in the `chapters` or `appendices` dictionary
    in Ark's configuration file `./config.py`.
    The order of entries in these two dictionaries
    determines the order of the chapters and appendices.

1.  The `index.md` files do *not* have YAML headers;
    their titles are taken from `./config.py`.

1.  Each section within a page must use a heading like this:

    ```markdown
    ## Some Title {: #topic-sometitle}
    ```

    This creates an `h2`-level heading with the HTML ID `topic-sometitle`.
    Use the page's slug instead of `topic`
    and hyphenate the words in the ID.

1.  To create a cross-reference to a chapter or appendix write:

    ```markdown
    [%x topic %]
    ```

    where `topic` is the slug of the chapter being referred to.
    This shortcode is converted to `Chapter N` or `Appendix N`
    or the equivalent in other languages.
    Please only refer to chapters or appendices, not to sections.

### Slides

1.  Each chapter directory also has a `slides.html` file
    containing slides formatted with [remark][remark].
    Each `slides.html` file must have a YAML header
    containing `template: slides` to specify the correct template.
    While the `index.md` file becomes `./docs/topic/index.html`,
    the `slides.html` file becomes `./docs/topic/slides/index.html`.

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

1.  To *omit* part of a file, use:

    ```markdown
    [% inc file="some_name.py" omit="some_key" %]
    ```

    If both the `keep` and `omit` keys are present, the former takes precedence,
    i.e., the `keep` section is included and the `omit` section within it omitted.

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
       slug="topic-some-key"
       img="some_file.svg"
       caption="Short sentence-case caption."
       alt="Long text describing the figure for the benefit of visually impaired readers."
    %]
    ```

    Please use underscores in filenames rather than hyphens:
    Python source files' names have to be underscored so that they can be imported,
    so all other filenames are also underscored for consistency.
    (Internal keys are hyphenated to avoid problems with LaTeX during PDF generation.)

1.  To refer to a figure write:

    ```markdown
    [%f topic-some-key %]
    ```

    This is converted to `Figure N.K`.

1.  Use [diagrams.net][diagrams] to create SVG diagrams
    using the "sketch" style and a 12-point Verdana font for all text.
    (`make fonts` will report diagrams that use other fonts.)

1.  Please avoid screenshots or other pixellated images:
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
    [%t topic-some-key %]
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
    [%i "index text" %]
    ```

    This puts `index text` in both the document and the index.

1.  If the indexing text and the body text are different, use:

    ```markdown
    [%i "index text" "body text" %]
    ```

1.  Finally, either kind of index entry may optionally include a `url` key
    to wrap the body text in a hyperlink:

    ```markdown
    [%i "index text" url=some_link %]
    ```

    `some_link` must be a key in the `./info/links.yml` links file.

### Minor Formatting

1.  To continue a paragraph after a code sample write:

    ```
    text of paragraph
    which can span multiple lines
    {: .continue}
    ```

    This has no effect on the appearance of the HTML,
    but prevents unwanted paragraph indentation in the PDF version.

1.  To create a callout box, use:

    ```
    <div class="callout" markdown="1">

    ### Title of Callout

    text of callout

    </div>
    ```

    Use "Sentence Case" for the callout's title,
    and put blank lines before and after the opening and closing `<div>` markers.
    You *must* include `markdown="1"` in the opening `<div>` tag
    to ensure that Markdown inside the callout is processed.

## Building the HTML

1.  Pages use the template in `./lib/mccole/templates/node.ibis`,
    which includes snippets from the same directory.

1.  Our CSS is in `./lib/mccole/resources/mccole.css`.
    We also use `./lib/mccole/resources/tango.css` for styling code fragments.
    We do *not* rely on any JavaScript in our pages.

1.  To produce HTML, run `make build` in the root directory,
    which updates the files in <code>./docs</code>.
    You can also run `make serve` to preview files locally.

## Building the PDF

We use LaTeX to build the PDF version of this book.
You will need to install these packages with `tlmgr`
or some other LaTeX package manager:

-   `babel-english`
-   `babel-greek`
-   `cbfonts`
-   `enumitem`
-   `greek-fontenc`
-   `keystroke`
-   `listings`
-   `textgreek`
-   `tocbibind`

## Other Commands

Use <code>make <em>target</em></code> to run a command.

| command | action |
| ------------- | ------ |
| style | check source code style |
| --- | --- |
| commands | show available commands |
| build | rebuild site without running server |
| serve | build site and run server |
| pdf | create PDF version of material |
| --- | --- |
| lint | check project structure |
| headings | show problematic headings (many false positives) |
| inclusions | compare inclusions in prose and slides |
| examples | re-run examples |
| check-examples | check which examples would re-run |
| fonts | check fonts in diagrams |
| spelling | check spelling against known words |
| index | show all index entries |
| --- | --- |
| html | create single-page HTML |
| latex | create LaTeX document |
| pdf-once | create PDF document with a single compilation |
| syllabus | remake syllabus diagrams |
| diagrams | convert diagrams from SVG to PDF |
| --- | --- |
| github | make root pages for GitHub |
| check | check source code |
| fix | fix source code |
| profile | profile compilation |
| clean | clean up stray files |
| --- | --- |
| status | status of chapters |
| valid | run html5validator on generated files |
| vars | show variables |

[ark]: https://www.dmulholl.com/docs/ark/main/
[book_issues]: https://github.com/gvwilson/sdxpy/issues
[gitbook]: https://www.gitbook.com/
[glosario]: https://glosario.carpentries.org/
[jupybook]: https://jupyterbook.org/
[marthas_rules]: https://journals.sagepub.com/doi/10.1177/088610998600100206
[quarto]: https://quarto.org/
[red_door]: https://www.reddoorshelter.ca/
[remark]: https://remarkjs.com/
[simpy]: https://simpy.readthedocs.io/
[sqlalchemy]: https://www.sqlalchemy.org/
