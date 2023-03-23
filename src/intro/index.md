---
title: "Introduction"
---

The best way to learn software design is to study examples [%b Schon1984 Petre2016 %],
and the most approachable examples are the tools programmers use themselves.
These lessons therefore build small versions of file backup systems,
testing frameworks,
and regular expression matchers
in order to show you how experienced programmers think.
And if you know how these tools work,
you will be more likely to use them
and better able to use them well.

## Who is this book for? {: #intro-audience}

This [learner persona][t3_personas] [%b Wilson2019 %] describes who this book is for:

> Maya has a master's degree in genomics.
> She has taught herself enough Python to analyze data from her experiments,
> but is constantly frustrated by the gaps in her programming knowledge.
> These lessons will teach her how to design, build, and test large programs
> in less time and with less pain,
> and show her how the libraries and tools she uses actually work.

Like Maya, you should be able to:

-   Write Python programs using lists, loops, conditionals, dictionaries, and functions.

-   Puzzle your way through Python programs that use classes and exceptions.

-   Write a little bit of HTML.

-   Use [Git][git] to save and share files.
    (It's OK not to know [the more obscure commands][git_man_page_generator].)

This book is also designed to help another kind of reader:

> Yim teaches two college courses on web programming.
> They are frustrated that so many books talk about algorithms but not about design
> and use examples that their students can't relate to.
> This material will give them material they can use in class
> and starting points for course projects.

You can read this book on its own or use it as a classroom resource.
If you need projects for a software design course,
adding a tool to those covered here would be fun as well as educational:
please [send email][email] if you'd like to chat.

## What does this book cover? {: #intro-contents}

Programmers have invented [a lot of tools][programming_tools] over the years.
This book focuses on those that people use while building code,
but includes a few things (like databases and web servers)
that are primarily used in applications for other people.

[%x glossary %] defines the terms these lessons introduce,
which in turn define this book's big ideas [%f intro-syllabus %]:

-   How to process a program like any other piece of text.

-   How to turn a program into a data structure that can be analyzed and modified.

-   What design patterns are and which ones are used most often.

-   How programs are executed and how we can control and inspect their execution.

-   How we can analyze programs' performance in order to make sensible design tradeoffs.

[% figure
   slug="intro-syllabus"
   img="syllabus.svg"
   alt="Syllabus"
   caption="Syllabus topics and dependencies."
%]

## How is this book formatted? {: #intro-layout}

We display Python source code like this:

[% inc file="python_sample.py" %]

and Unix shell commands like this:
{: .continue}

[% inc file="shell_sample.sh" %]

Data files and program output are shown like this:
{: .continue}

[% inc file="output_sample.out" %]

[% inc file="data_sample.yml" %]

We use `...` to show where lines have been omitted,
and occasionally wrap lines in unnatural ways to make them fit on the page.
Where we need to break lines for the same reason,
we end all but the last line with a single backslash `\`.
The full listings are all available in [our Git repository][book_repo]
and [on our website][book_site].

Finally,
we write functions as `function_name` rather than `function_name()`.
The latter is more common,
but people don't use `array_name[]` for arrays,
and the empty parentheses makes it hard to tell
whether we're talking about "the function itself" or "a call to the function with no parameters".

## How can this material be used? {: #intro-use}

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
please file an issue in [our GitHub repository][book_repo]
or [send email][email].
Please note that all contributors are required to abide by our Code of Conduct
([%x conduct %]).

## Who helped create this material? {: #intro-acknowledgments}

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

I am grateful to 
Christian Drumm,
Julia Evans,
Joe Nash,
Juanan Pereira,
and
Dave Smith
for feedback,
and to 
Miras Adilov,
Alvee Akand,
Alexey Alexapolsky,
Lina Andrén,
Alberto Bacchelli,
Yanina Bellini Saibene,
Adrienne Canino,
Stephen Childs,
Hector Correa,
Socorro Dominguez,
Thomas Fritz,
Francisco Gabriel,
Craig Gross,
Jonathan Guyer,
McKenzie Hagen,
Fraser Hay,
Bahman Karimi,
Carolyn Kim,
Jenna Landy,
Peter Lin,
Becca Love,
Dan McCloy,
Ramiro Mejia,
Michael Miller,
Firas Moosvi,
Sheena Ng,
Reiko Okamoto,
Mahmoodur Rahman,
Arpan Sarkar,
Ece Turnator,
and Yundong Yao
for test-driving this material with me.
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
