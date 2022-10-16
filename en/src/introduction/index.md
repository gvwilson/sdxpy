---
title: "Introduction"
---

[% root README.md %]

## Audience {: #introduction-audience}

These [personas][t3_personas] describe who this book is meant to help [%b Wilson2019 %]:

-   Aïsha started writing VB macros for Excel in an accounting course and never looked back.
    After spending three years fixing her company's [Django][django] website
    she wants to learn how to build back-end applications properly.
    This material will fill in some gaps in her programming knowledge
    and teach her some common design patterns.

-   Rupinder is studying computer science at college.
    He has learned a lot about the theory of algorithms,
    and while he uses Git and unit testing tools in his assignments,
    he doesn't feel he understands how they work.
    This material will give him a better understanding of those tools
    and of how to design new ones.

-   Yim builds mobile apps for a living
    but also teaches two college courses.
    They are frustrated that so many books talk about algorithms but not about design
    and use examples that their students can't relate to.
    This material will fill those gaps
    and give them starting points for a wide variety of course assignments.

Like these three personas, readers should be able to:

-   Write Python programs using loops, arrays, functions, and classes.

-   Create static web pages using HTML and CSS.

-   Use [Git][git] to save and share files.
    (It's OK not to know [the more obscure commands][git_man_page_generator].)

-   Explain what a tree is and how to process one recursively.
    (This is the most complicated data structure and algorithm we *don't* explain.)

This book can be read on its own or used as a classroom resource.
If you are looking for a project to do in a software design course,
adding a tool to those covered here would be fun as well as educational.
Please see [%x conclusion %] for more details.

## Topics {: #introduction-contents}

Programmers have invented [a lot of tools][programming_tools] to make their lives easier.
This volume focuses on a few that individual developers use while writing software;
we hope future volumes
will explore those used in the applications that programmers build.

[%x glossary %] defines the terms we introduce in these lessons,
which in turn define their scope:

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

We occasionally wrap lines in source code in unnatural ways to make listings fit the printed page,
and sometimes use `...` to show where lines have been omitted.
Where we need to break lines of output for the same reason,
we end all but the last line with a single backslash `\`.
The full listings are all available in [our Git repository][sdxpy_repo]
and [on our website][sdxpy_site].

Finally,
we write functions as `function_name` rather than `function_name()`;
the latter is more common,
but people don't use `array_name[]` for arrays,
and the empty parentheses makes it hard to tell
whether we're talking about "the function itself" or "a call to the function with no parameters".

## Contributing {: #introduction-use}

All of the written material in this book
is made available under the [Creative Commons - Attribution - NonCommercial 4.0 International license][cc_by_nc]
(CC-BY-NC-4.0),
while the software is made available under the [Hippocratic License][hippocratic_license].
The first allows you to use and remix this material for non-commercial purposes,
as-is or in adapted form,
provided you cite its original source.
The second allows you to use and remix the software on this site
provided you do not violate international agreements governing human rights.
Please see [%x license %] for details.

If you would like to improve what we have,
add new material,
or have questions,
please file an issue in our GitHub repository or send us email.
Please note that all contributors are required to abide by our Code of Conduct
([%x conduct %]).

## Acknowledgments {: #introduction-acknowledgments}

This book was inspired by
classics like [%b Kernighan1979 Kernighan1981 Kernighan1983 Kernighan1988 Petre2016 %],
and by:

-   the entries in the [*Architecture of Open Source Applications*][aosa] series [%b Brown2011 Brown2012 Armstrong2013 Brown2016 %];
-   [Mary Rose Cook][cook_mary_rose]'s [Gitlet][gitlet];
-   [Matt Brubeck][brubeck_matt]'s [browser engine tutorial][browser_engine_tutorial];
-   [Connor Stack][stack_connor]'s [database tutorial][db_tutorial];
-   [Maël Nison][nison_mael]'s [package manager tutorial][package_manager_tutorial];
-   [Paige Ruten][ruten_paige]'s [kilo text editor][kilo_editor];
-   [Bob Nystrom][nystrom_bob]'s book [*Crafting Interpreters*][crafting_interpreters] [%b Nystrom2021 %];
-   [Pavel Panchekha][panchekha_pavel] and [Chris Harrelson][harrelson_chris]'s [*Web Browser Engineering*][browser_engineering]
-   [Julia Evans][evans_julia]' posts and [zines][evans_zines].

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
and the other open source tools used to make this material.
If we all give a little,
we all get a lot.

<div class="center" markdown="1">
  *This one's for Mike:*
  <br/>
  *I'm glad you've always found it hard to say no.*
</div>
