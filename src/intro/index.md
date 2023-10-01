---
abstract: >
    The best way to learn design is to study examples,
    and the best programs to use as examples are the ones programmers use every day.
    These lessons therefore build small versions
    of tools that programmers use every day
    to show how experienced software designers think.
    Along the way,
    they introduce some fundamental ideas in computer science
    that many self-taught programmers haven't encountered.
    The lessons assume readers can write small programs and want to write larger ones,
    or are looking for material to use in software design classes that they teach.
syllabus:
-   The complexity of a system increases more rapidly than its size.
-   The best way to learn design is to study examples,
    and the best programs to use as examples are the ones programmers use every day.
-   These lessons assume readers can write small programs and want to write larger ones,
    or are looking for material to use in software design classes that they teach.
-   All of the content is free to read and re-use under open licenses,
    and all royalties from sales of this book will go to charity.
---

The best way to learn design in any field
is to study examples [%b Schon1984 Petre2016 %],
and the most approachable examples are ones that readers are already familiar with.
These lessons therefore build small versions
of [tools that programmers use every day][programming_tools]
to show how experienced software designers think.
Along the way,
they introduce some fundamental ideas in computer science
that many self-taught programmers haven't encountered.
We hope these lessons will help you design better software yourself,
and that if you know how programming tools work,
you'll be more likely to use them
and better able to use them well.

## Audience {: #intro-audience}

This [learner persona][t3_personas] [%b Wilson2019 %] describes who this book is for:

> *Maya has a master's degree in genomics.
> She knows enough Python to analyze data from her experiments,
> but struggles to write code other people can use.
> These lessons will show her how to design, build, and test large programs
> in less time and with less pain.*
> {: .continue}

Like Maya, you should be able to:
{: .continue}

-   Write Python programs using lists, loops, conditionals, dictionaries, and functions.

-   Puzzle your way through Python programs that use [%i "class" "classes" %]
    and [%i "exception" "exceptions" %].

-   Run basic Unix shell commands like `ls` and `mkdir`.

-   Read and write a little bit of [%i "HTML" %].

-   Use [Git][git] to save and share files.
    (It's OK not to know [the more obscure commands][git_man_page_generator].)

This book is also designed to help another persona:

> *Yim teaches two college courses on software development.
> They are frustrated that so many books talk about details but not about design
> and use examples that their students can't relate to.
> This material will give them material they can use in class
> and starting points for course projects.*
> {: .continue}

[% figure
   slug="intro-syllabus"
   img="syllabus.svg"
   alt="Syllabus"
   caption="Lesson topics and dependencies."
%]

## The Big Ideas {: #intro-ideas}

Our approach to design is based on three big ideas.
First,
as the number of components in a system grows,
the complexity of the system increases rapidly
([%f intro-complexity %]).
However,
the number of things we can hold in working memory at any time
is fixed and fairly small [%b Hermans2021 %].
If we want to build large programs that we can understand,
we therefore need to construct them out of pieces
that interact in a small number of ways.
Figuring out what those pieces and interactions should be
is the core of what we call "design".

[% figure
   slug="intro-complexity"
   img="complexity.svg"
   alt="Complexity and size"
   caption="How complexity grows with size."
%]

Second,
"making sense" depends on who we are.
When we use a low-level language,
we incur the [%g cognitive_load "cognitive load" %]
of assembling micro-steps into something more meaningful.
When we use a high-level language,
on the other hand,
we incur a similar load translating functions of functions of functions
into actual operations on actual data.

More experienced programmers are more capable at both ends of the curve,
but that's not the only thing that changes.
If a novice's comprehension curve looks like the lower one in [%f intro-comprehension %],
then an expert's looks like the upper one.
Experts don't just understand more at all levels of abstraction;
their *preferred* level has also shifted
so they find \\( \sqrt{x^2 + y^2} \\) easier to read
than the Medieval equivalent
"the side of the square whose area is the sum of the areas of the two squares
whose sides are given by the first part and the second part".
This curve means that for any given task,
the code that is quickest for a novice to comprehend
will almost certainly be different from the code that
an expert can understand most quickly.

[% figure
   slug="intro-comprehension"
   img="comprehension.svg"
   alt="Comprehension curves"
   caption="Novice and expert comprehension curves."
%]

Our third big idea is that programs are just another kind of data.
Source code is just text,
which we can process like other text files.
Likewise,
a program in memory is just a data structure
that we can inspect and modify like any other.
Treating code like data enables us to solve hard problems in elegant ways,
but at the cost of increasing the level of abstraction in our programs.
Once again,
finding the balance is what we mean by "design".

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
we show glossary entries in **bold text**
and write functions as `function_name` rather than `function_name()`.
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
The first license allows you to use and remix this material for noncommercial purposes,
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

## What People Are Saying {: #intro-praise}

Here's what people said about the JavaScript version of this book [%b Wilson2022b %]:

-   [Jessica Kerr][kerr_jessica]:
    *Software Design by Example* is the book I'll recommend to every new dev…
    It is nice to you.
    It wants you to succeed…
    It's a bridge from "learn to program" to working programmer.

-   [Jenn Schiffer][schiffer_jenn]:
    I am v much enjoying gvwilson's book *Software Design by Example*.
    It makes me miss teaching, it would be such a fun text to use!

-   [Emily Gorcenski][gorcenski_emily]:
    There's a lot of books on programming
    but fewer books that couple software development with effective and practical use of tools,
    presenting a language not as a main course but as a part of an engineering ecosystem.
    Greg Wilson's book hits all the right notes in bringing together theory, pragmatism, and best practices.

-   [Danielle Navarro][navarro_danielle]:
    The book is really bloody lovely.

## Acknowledgments {: #intro-acknowledgments}

Like [%b Wilson2022b %],
this book was inspired by [%b Kamin1990 Kernighan1979 Kernighan1981 Kernighan1983 Kernighan1988 Oram2007 Wirth1976 %] and by:

-   [*The Architecture of Open Source Applications*][aosa] series
    [%b Brown2011 Brown2012 Armstrong2013 Brown2016 %];
-   [Mary Rose Cook's][cook_mary_rose] [Gitlet][gitlet];
-   [Matt Brubeck's][brubeck_matt] [browser engine tutorial][browser_engine_tutorial];
-   [*Web Browser Engineering*][browser_engineering]
    by [Pavel Panchekha][panchekha_pavel] and [Chris Harrelson][harrelson_chris];
-   [Connor Stack's][stack_connor] [database tutorial][db_tutorial];
-   [Maël Nison's][nison_mael] [package manager tutorial][package_manager_tutorial];
-   [Paige Ruten's][ruten_paige] [kilo text editor][kilo_editor]
    and [Wasim Lorgat's][lorgat_wasim] [editor tutorial][lorgat_editor];
-   [Bob Nystrom's][nystrom_bob] [*Crafting Interpreters*][crafting_interpreters] [%b Nystrom2021 %];
    and 
-   the posts and [zines][evans_zines] created by [Julia Evans][evans_julia].

I am grateful to [% thanks %] for feedback on early drafts of this material.

I am also grateful to Shashi Kumar for help with LaTeX,
to [Odin Beuchat][beuchat_odin] for help with JavaScript,
and to the creators of
[Black][black],
[flake8][flake8],
[Glosario][glosario],
[GNU Make][gnu_make],
[isort][isort],
[ark][ark],
[LaTeX][latex],
[pip][pip],
[Python][python],
[Remark][remark],
[WAVE][webaim_wave],
and many other open source tools:
if we all give a little,
we all get a lot.

<div class="center" markdown="1">
  *This one's for Mike and Jon: I'm glad you always found time to chat.*
</div>

All royalties from this book will go to the [Red Door Family Shelter][red_door] in Toronto.
{: .continue}

## Exercises {: #intro-exercises}

### Setting Up {: .exercise}

1.  Use [pip][pip] to install [Black][black], [flake8][flake8], and [isort][isort]
    on your computer.
2.  Run them on a few programs you have already written.
    (The file `setup.cfg` in the root directory of [this book's GitHub repository][book_repo]
    has the settings we use for these tools.)
    What problems do they report?
    Which of these reports do you disagree with?

### Avoiding Potholes {: .exercise}

Go to [the GitHub repository][book_repo] for this book and look at the open issues.
Which of them can you understand?
What makes the others hard to understand?
What could you add, leave out, or write differently
when you report a problem that you have found?
