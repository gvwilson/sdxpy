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

    -   An object-relational mapper to show people how tools like [SQLAlchemy][sqlalchemy] work.
    -   A discrete event simulator to show people how tools like [SimPy][simpy] work
        and to explore co-operative concurrency using generators.
    -   An issue-tracking system, mostly to show how workflow management and authentication work.
    -   Another build system that uses publish/subscribe instead of the top-down approach of [A Build Manager](@/build/).
    -   A fuzz tester that uses some of the ideas from [Zeller2023].
    -   A package installer to complement the package manager of [A Package Manager](@/pack/).
    -   A file compression tool like `zip`.
    -   A database that uses B-trees instead of a log for storage.

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

## Formatting

This material uses [mccole][mccole].
Please run `make` in the root directory to get a list of available commands.

[mccole]: https://github.com/gvwilson/mccole/
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
