---
title: "Introduction"
---

> We shape our tools, and thereafter our tools shape us.
>
> — Marshall McLuhan

The best way to learn software design is to study examples,
and the best examples can be found in
the tools programmers use themselves.
These lessons therefore build small versions of file backup systems,
testing frameworks,
and regular expression matchers
in order to shed light on how experienced programmers think.
We also hope that if you know how these tools work,
you will be more likely to use them
and better able to use them well.

## Audience {: #introduction-audience}

These [personas][t3_personas] describe who this book is for [%b Wilson2019 %]:

-   Aïsha has a master's degree in genomics
    and does very complicated science things in a wet lab.
    She has taught herself enough Python to do some sophisticated data analysis,
    but is constantly frustrated by what she *doesn't* know about how software actually works.
    This material will take away some of the mystery.

-   Rupinder is studying computer science at college.
    He uses Git and style checkers in his assignments
    and wants to know how they work.
    This material will take away some of the mystery
    and show him how to build new tools of his own.

-   Yim teaches two college courses on web programming.
    They are frustrated that so many books talk about algorithms but not about design
    and use examples that their students can't relate to.
    This material will give them material they can use in class
    and starting points for course projects.

Like these three personas, readers should be able to:

-   Write Python programs using dictionaries, exceptions, and classes.
    (We assume that if you can use these,
    you can also use lists, loops, conditionals, and functions.)

-   Create static web pages using HTML and CSS.

-   Use [Git][git] to save and share files.
    (It's OK not to know [the more obscure commands][git_man_page_generator].)

-   Process a tree's nodes recursively.
    (Trees and recursion are the most complicated things we *don't* explain.)

You can read this book on its own or use it as a classroom resource.
If you need projects for a software design course,
adding a tool to those covered here would be fun as well as educational:
please email [% config email %] if you'd like to chat.

## Topics {: #introduction-contents}

Programmers have invented [a lot of tools][programming_tools] over the years.
This book focuses on those that people use while building code,
but includes a few things (like databases and web servers)
that are primarily used in finished applications.

[%x glossary %] defines the terms these lessons introduce,
which in turn define this book's big ideas:

-   How to process a program like any other piece of text.

-   How to turn a program into a data structure that can be analyzed and modified.

-   What design patterns are and which ones are used most often.

-   How programs are executed and how we can control and inspect their execution.

-   How we can analyze programs' performance in order to make sensible design tradeoffs.

-   How to find and run code modules on the fly.

## Layout {: #introduction-layout}

We display Python source code like this:

[% inc file="python_sample.py" %]

and Unix shell commands like this:
{: .continue}

[% inc file="shell_sample.sh" %]

Data files and program output are shown in italics:
{: .continue}

[% inc file="output_sample.out" %]

[% inc file="data_sample.yml" %]

We use `...` to show where lines have been omitted,
and occasionally wrap lines in unnatural ways to make them fit on the page.
Where we need to break lines for the same reason,
we end all but the last line with a single backslash `\`.
The full listings are all available in [our Git repository][sdxpy_repo]
and [on our website][sdxpy_site].

Finally,
we write functions as `function_name` rather than `function_name()`.
The latter is more common,
but people don't use `array_name[]` for arrays,
and the empty parentheses makes it hard to tell
whether we're talking about "the function itself" or "a call to the function with no parameters".

## Contributing {: #introduction-use}

All of the written material in this book
is available under the [Creative Commons - Attribution - NonCommercial 4.0 International license][cc_by_nc]
(CC-BY-NC-4.0),
while the software is available under the [Hippocratic License][hippocratic_license].
The first allows you to use and remix this material for non-commercial purposes,
as-is or in adapted form,
provided you cite its original source.
The second allows you to use and remix the software on this site
provided you do not violate international agreements governing human rights;
please see [%x license %] for details.

If you would like to improve what we have,
add new material,
or ask questions,
please file an issue in [our GitHub repository][sdxpy_repo]
or email [% config email %].
Please note that all contributors are required to abide by our Code of Conduct
([%x conduct %]).

## Acknowledgments {: #introduction-acknowledgments}

This book was inspired by
classics like [%b Kernighan1979 Kernighan1981 Kernighan1983 Kernighan1988 Petre2016 %],
and by:

-   the entries in the [*Architecture of Open Source Applications*][aosa] series [%b Brown2011 Brown2012 Armstrong2013 Brown2016 %];
-   [Mary Rose Cook][cook_mary_rose]'s [Gitlet][gitlet];
-   [Matt Brubeck][brubeck_matt]'s [browser engine tutorial][browser_engine_tutorial];
-   [Pavel Panchekha][panchekha_pavel] and [Chris Harrelson][harrelson_chris]'s [*Web Browser Engineering*][browser_engineering]
-   [Connor Stack][stack_connor]'s [database tutorial][db_tutorial];
-   [Maël Nison][nison_mael]'s [package manager tutorial][package_manager_tutorial];
-   [Paige Ruten][ruten_paige]'s [kilo text editor][kilo_editor]
    and [Wasim Lorgat][lorgat_wasim]'s [editor tutorial][lorgat_editor];
-   [Bob Nystrom][nystrom_bob]'s [*Crafting Interpreters*][crafting_interpreters] [%b Nystrom2021 %];
    and 
-   [Julia Evans][evans_julia]' posts and [zines][evans_zines].

I am grateful for feedback from [Julia Evans][evans_julia].
I am also grateful to the creators of
[Black][black],
[flake8][flake8],
[Glosario][glosario],
[GNU Make][gnu_make],
[isort][isort],
[ivy][ivy],
[LaTeX][latex],
[pip][pip],
[Python][python],
[SVG Screenshot][svg_screenshot],
[WAVE][webaim_wave],
and many other open source tools:
if we all give a little,
we all get a lot.

<div class="center" markdown="1">
  *This one's for Mike and Jon:*
  <br/>
  *I'm glad you've always found it hard to say no.*
</div>
