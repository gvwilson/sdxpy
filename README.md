# Software Design for Data Scientists

Most data scientists have taught themselves most of what they know
about programming.  As a result, many have gaps in their knowledge:
they may be experts in some areas, but don't even know what they don't
know about others.

One of those other areas is software design.  A large program is not
just a dozen short programs stacked on top of each other: doubling the
size of a program more than doubles its complexity.  Since our brains
can only hold a small number of things at once, making large programs
comprehensible, testable, shareable, and maintainable requires more
than using functions and sensible variable names: it requires design.

The best way to learn design in any field is to study examples.  These
lessons therefore build small versions of tools that programmers use
every day to show how experienced software designers think.  Along the
way, they introduce some fundamental ideas in computer science that
most data scientists haven't encountered.  Finally, we hope that if
you know how programming tools work, you'll be more likely to use them
and better able to use them well.

## Who is this book for?

> Maya has a master's degree in genomics.  She knows enough Python to
> analyze data from her experiments, but is struggling to write code
> that other people (including her future self) can use.  These
> lessons will teach her how to design, build, and test large programs
> in less time and with less pain.

Like Maya, you should be able to:

-   Write Python programs using lists, loops, conditionals, dictionaries, and functions.

-   Puzzle your way through Python programs that use classes and exceptions.

-   Run basic Unix shell commands like `ls` and `mkdir`.

-   Read and write a little bit of HTML.

-   Use Git to save and share files.

This book is also designed for:

> Yim teaches two college courses on web programming.  They are
> frustrated that so many books talk about details but not about
> design and use examples that their students can't relate to.  This
> material will give them material they can use in class and starting
> points for course projects.

## Status

| Chapter   | Code   | Slides | Diagrams | Exercises | Prose  | Overall |
| --------- | ------ | ------ | -------- | --------- | ------ | ------: |
| intro	    | N/A    | done   | done     | N/A       | done   | 100%    |
| dup	    | done   | done   | done     | -         | -      |  50%    |
| glob	    | done   | done   | -        | -         | -      |  25%    |
| parse	    | done   | done   | -        | -         | -      |  25%    |
| test	    | revise | revise | done     | -         | -      |  50%    |
| mock	    | -      | -      | -        | -         | -      |   0%    |
| archive   | revise | revise | revise   | revise    | -      |  25%    |
| oop	    | done   | done   | done     | done      | -      |  50%    |
| meta	    | -      | -      | -        | -         | -      |   0%    |
| check	    | done   | done   | done     | -         | -      |  50%    |
| interp    | done   | done   | done     | done      | -      |  50%    |
| func	    | revise | -      | -        | -         | -      |   0%    |
| template  | done   | done   | done     | -         | -      |  50%    |
| layout    | revise | revise | done     | -         | -      |  25%    |
| lint	    | revise | revise | done     | -         | -      |  25%    |
| perf	    | done   | done   | done     | done      | -      |  50%    |
| persist   | done   | done   | done     | done      | -      |  50%    |
| binary    | revise | revise | done     | -         | -      |  25%    |
| db	    | done   | -      | -        | -         | -      |  10%    |
| build	    | done   | done   | done     | done      | -      |  50%    |
| flow	    | done   | -      | -        | -         | -      |  10%    |
| pack	    | done   | -      | -        | -         | -      |   0%    |
| server    | done   | -      | -        | -         | -      |  25%    |
| editor    | revise | -      | -        | -         | -      |  10%    |
| undo	    | -      | -      | -        | -         | -      |   0%    |
| vm	    | done   | -      | -        | -         | -      |  10%    |
| compiler  | done   | -      | -        | -         | -      |  10%    |
| debug	    | done   | -      | -        | -         | -      |   0%    |
| finale    | N/A    | -      | -        | -         | revise |  25%    |
|           |        |        |          |           |        | *27%*   |
