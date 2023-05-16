Most data scientists have taught themselves most of what they know about programming.
As a result,
many have gaps in their knowledge:
they may be experts in some areas,
but don't even know what they don't know about others.

One of those other areas is software design.
A large program is not just a dozen short programs stacked on top of each other;
since *N* things can interact with each other in *N(N-1)/2* ways,
doubling the size of a program more than doubles its complexity
unless we reorganize its parts
([%f intro-complexity %]).
Since our brains can only hold a small number of things at once [%b Hermans2021 %],
making large programs comprehensible, testable, shareable, and maintainable
requires more than using functions and sensible variable names:
it requires design.

[% figure
   slug="intro-complexity"
   img="complexity.svg"
   alt="Complexity and size"
   caption="How complexity grows with size."
%]

The best way to learn design in any field is to study examples [%b Schon1984 Petre2016 %].
These lessons therefore build small versions of tools that programmers use every day
to show how experienced software designers think.
Along the way,
they introduce some fundamental ideas in computer science
that most data scientists haven't encountered.
Finally,
we hope that if you know how programming tools work,
you'll be more likely to use them
and better able to use them well.

## Audience {: #intro-audience}

This [learner persona][t3_personas] [%b Wilson2019 %] describes who this book is for:

> Maya has a master's degree in genomics.
> She knows enough Python to analyze data from her experiments,
> but is struggling to write code that other people (including her future self) can use.
> These lessons will teach her how to design, build, and test large programs
> in less time and with less pain.

Like Maya, you should be able to:

-   Write Python programs using lists, loops, conditionals, dictionaries, and functions.

-   Puzzle your way through Python programs that use classes and exceptions.

-   Run basic Unix shell commands like `ls` and `mkdir`.

-   Read and write a little bit of HTML.

-   Use [Git][git] to save and share files.
    (It's OK not to know [the more obscure commands][git_man_page_generator].)

This book is also designed to help another persona:

> Yim teaches two college courses on web programming.
> They are frustrated that so many books talk about details but not about design
> and use examples that their students can't relate to.
> This material will give them material they can use in class
> and starting points for course projects.

## Topics {: #intro-contents}

Programmers have invented [a lot of tools][programming_tools] over the years.
This book focuses on those that people use while building code,
but includes a few like databases and web servers
that are primarily used in building general-purpose applications.

[%x glossary %] defines the terms these lessons introduce,
which in turn define this book's big ideas [%f intro-syllabus %]:

-   Source code is just text.

-   A program in memory is just a data structure.

-   We can control and inspect programs while they are running.

-   A week of hard work can sometimes save us an hour of thought.

[% figure
   slug="intro-syllabus"
   img="syllabus.svg"
   alt="Syllabus"
   caption="Lesson topics and dependencies."
%]

## Formatting {: #intro-layout}

We display Python source code like this:

[% inc file="python_sample.py" %]

and Unix shell commands like this:
{: .continue}

[% inc file="shell_sample.sh" %]

Data files and program output are shown like this:
{: .continue}

[% inc file="data_sample.yml" %]

[% inc file="output_sample.out" %]

We use `...` to show where lines have been omitted,
and occasionally break lines in unnatural ways to make them fit on the page.
Where we do this,
we end all but the last line with a single backslash `\`.
Finally,
we write functions as `function_name` rather than `function_name()`.
The latter is more common,
but people don't use `array_name[]` for arrays,
and the empty parentheses makes it hard to tell
whether we're talking about "the function itself" or "a call to the function with no parameters".

## Usage {: #intro-use}

The source for this book is available in [our Git repository][book_repo]
and all of it can be read on [our website][book_site].
All of the written material in this book
is licensed under the [Creative Commons - Attribution - NonCommercial 4.0 International license][cc_by_nc]
(CC-BY-NC-4.0),
while the software is covered by the [Hippocratic License][hippocratic_license].
The first license allows you to use and remix this material for non-commercial purposes,
as-is or in adapted form,
provided you cite its original source;
if you want to sell copies or make money from this material in any other way,
you must [contact us][email] and obtain permission first.
The second license allows you to use and remix the software on this site
provided you do not violate international agreements governing human rights;
please see [%x license %] for details.

If you would like to improve what we have,
add new material,
or ask questions,
please file an issue in [our GitHub repository][book_repo]
or [send email][email].
All contributors are required to abide by our Code of Conduct
([%x conduct %]).

## Acknowledgments {: #intro-acknowledgments}

This book is a sequel to [%b Wilson2022b %],
and like it,
was inspired by [%b Kamin1990 Kernighan1979 Kernighan1981 Kernighan1983 Kernighan1988 Oram2007 %] and by:

-   the entries in the [*Architecture of Open Source Applications*][aosa] series [%b Brown2011 Brown2012 Armstrong2013 Brown2016 %];
-   [Mary Rose Cook's][cook_mary_rose] [Gitlet][gitlet];
-   [Matt Brubeck's][brubeck_matt] [browser engine tutorial][browser_engine_tutorial];
-   [Pavel Panchekha][panchekha_pavel] and [Chris Harrelson's][harrelson_chris] [*Web Browser Engineering*][browser_engineering]
-   [Connor Stack's][stack_connor] [database tutorial][db_tutorial];
-   [Maël Nison's][nison_mael] [package manager tutorial][package_manager_tutorial];
-   [Paige Ruten's][ruten_paige] [kilo text editor][kilo_editor]
    and [Wasim Lorgat's][lorgat_wasim] [editor tutorial][lorgat_editor];
-   [Bob Nystrom's][nystrom_bob] [*Crafting Interpreters*][crafting_interpreters] [%b Nystrom2021 %];
    and 
-   the posts and [zines][evans_zines] created by [Julia Evans][evans_julia].

I am grateful to [% thanks %] for feedback on early drafts of this material.
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
  *This one's for Mike and both Jons:*
  <br>
  *I'm glad you always found time to chat.*
</div>
