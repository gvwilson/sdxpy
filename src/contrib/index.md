Contributions are very welcome;
please contact us by email or by filing an issue on this site.
All contributors must abide by our Code of Conduct.

## Editing Content {: #contrib-edit}

1.  Clone the GitHub repository at [%config repo %].

1.  Create a new Python virtual environment.

1.  `pip install -r lib/mccole/requirements.txt`.

1.  `pip install -r ./requirements.txt`.

1.  `make` will show a list of available commands.

1.  `make build` to regenerate HTML from Markdown.
    -   The generated HTML can be found in `./docs`.
    -   You must have [draw.io][draw_io] installed and on your path to regenerate diagrams.

1.  `make serve` to regenerate HTML and preview it locally.
    -   The preview appears at `http://localhost:4000/`.
    -   [Ark][ark] will regenerate the HTML as the Markdown files are edited and saved.

1.  To change a code example and its output:
    1.  `cd ./src/chapter`.
    1.  Edit the Python file(s) you wish to change.
    1.  Run `make` in the chapter directory to rebuild the corresponding output files.

Please see `CONTRIBUTING.md` in the root directory of [our GitHub repository][book_repo]
for a complete description of our formatting rules.

## FAQ {: #contrib-faq}

Why is this book free to read online?

:   Because only a tiny minority of technical books make enough money
    to pay back the time required to create them,
    and because I would rather be able to fix errata
    than have people pirating out-of-date PDFs.

Why are the royalties going to charity?

:   The [Red Door Family Shelter][red_door] and places like it
    have always been short of money and resources,
    and the COVID-19 pandemic only made matters worse.
    They do more good on the average Tuesday than most of us do in a year
    (or a lifetime);
    I'm glad to be able to help however I can.

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

Why don't the examples connect with each other? For example, why don't they build toward a complete minimal IDE?

:   It was tempting, but attempts to do this in the past have not gone well.
    First, it makes maintenance much more difficult
    because a change in an early chapter may have knock-on effects on several subsequent chapters.
    Second, it constrains what is taught and in what order:
    if the examples are independent of each other,
    instructors can pick and choose the pieces that are most relevant to their audience and goals.

How did you settle on these particular topics?

:   I started with a list of tools programmers use that can be implemented in the small
    (like version control systems and debuggers).
    I added a few things that programmers rely on (like page layout and object persistence),
    then went back and filled in gaps,
    which is why there are chapters on functions and closures, protocols, and binary data.

Will there be a sequel?

:   If enough people want to write chapters I would be happy to organize and edit a second volume.
    Some things I'd particularly like to see are:

    -   An object-relational mapper to show people how tools like [SQLAlchemy][sqlalchemy] work
        ([% issue 45 %]).
    -   A discrete event simulator to show people how tools like [SimPy][simpy] work
        and to explore co-operative concurrency using generators
        ([% issue 56 %]).
    -   An issue-tracking system, mostly to show how workflow management and authentication work
        ([% issue 82 %]).
    -   Another build system that uses publish/subscribe instead of the top-down approach of [%x build %]
        ([% issue 83 %]).
    -   A fuzz tester that uses some of the ideas from [%b Zeller2023 %]
        ([% issue 84 %]).
    -   A package installer to complement the package manager of [%x pack %]
        ([% issue 121 %]).
    -   A file compression tool like `zip`
        ([% issue 144 %]).
    -   A database that uses B-trees instead of a log for storage
        ([% issue 151 %]).

Why did you build your own production pipeline instead of using [GitBook][gitbook], [Quarto][quarto], [Jupyter Book][jupybook], or some other existing tool?

:   I've written or edited books with those tools and others like them,
    and found them more frustrating than helpful.
    For example,
    the code samples in this book often show one or two methods from a class
    rather than the whole class;
    there is no straightforward way to achieve that with tools built on computational notebooks.
    That said,
    I'm sure the authors of those systems would find this book's tooling
    just as frustrating as I find theirs.

## Making Decisions {: #contrib-decisions}

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
