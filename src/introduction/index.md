---
title: "Introduction"
---

The best way to learn design is to study examples [%b Schon1984 Petre2016 %],
and some of the best examples of software design come from
the tools programmers use in their own work.
These lessons build small versions of file backup systems,
testing frameworks,
and regular expression matchers
both to demystify them
and to give some insights into how experienced programmers think.
We draw inspiration from [%b Brown2011 Brown2012 Brown2016 %],
[Mary Rose Cook's][cook_mary_rose] [Gitlet][gitlet],
and the books that introduced the Unix philosophy to an entire generation of programmers
[%b Kernighan1979 Kernighan1981 Kernighan1983 Kernighan1988 %].

## Who is our audience? {: #introduction-audience}

Every lesson should be written with specific learners in mind [%b Wilson2019 %].
These three [personas][t3_personas] describe ours:

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

## What tools and ideas do we cover? {: #introduction-contents}

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

<div class="pagebreak"></div>

## How are these lessons laid out? {: #introduction-layout}

We display Python source code like this:

```python
for thing in collection:
    print(thing)
```

and Unix shell commands like this:
{: .continue}

```sh
for filename in *.dat
do
    cut -d , -f 10 $filename
done
```

Data and output are shown in italics:
{: .continue}

```txt
Package,Releases
0,1
0-0,0
0-0-1,1
00print-lol,2
00smalinux,0
01changer,0
```

We occasionally wrap lines in source code in unnatural ways to make listings fit the printed page,
and sometimes use `...` to show where lines have been omitted.
Where we need to break lines of output for the same reason,
we end all but the last line with a single backslash `\`.
The full listings are all available in [our Git repository][sdpy_repo]
and [on our website][sdpy_site].

Finally,
we write functions as `function_name` rather than `function_name()`;
the latter is more common,
but people don't use `array_name[]` for arrays,
and the empty parentheses makes it hard to tell
whether we're talking about "the function itself" or "a call to the function with no parameters".

## How can people use and contribute to this material? {: #introduction-use}

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

## Who helped us? {: #introduction-help}

I am grateful to the creators of
[Black][black],
[flake8][flake8],
[Glosario][glosario],
[GNU Make][gnu_make],
[isort][isort],
[LaTeX][latex],
[pip][pip],
[SVG Screenshot][svg_screenshot],
[WAVE][webaim_wave],
and all the other open source tools used in creating these lessons:
if we all give a little,
we all get a lot.
