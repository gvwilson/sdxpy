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

| Chapter  | Slides | Exercises | Figures | Words | Overall |
|:---------|-------:|----------:|--------:|------:|--------:|
| intro    |     10 |         0 |       2 |  1024 |    102% |
| dup      |     19 |         5 |       5 |  1752 |     82% |
| glob     |     22 |         8 |       4 |  1763 |    100% |
| parse    |     15 |         3 |       3 |  1194 | **58%** |
| test     |     16 |         7 |       4 |  1933 |     88% |
| interp   |     16 |         8 |       2 |  1921 |     92% |
| oop      |     17 |         2 |       4 |  1021 | **55%** |
| func     |     19 |         4 |       3 |  1422 | **73%** |
| mock     |      5 |         1 |       1 |  1239 | **32%** |
| archive  |     19 |         7 |       3 |  2132 |     96% |
| check    |     20 |         0 |       3 |  1296 | **56%** |
| template |     23 |        10 |       2 |  2240 |    118% |
| lint     |     20 |         7 |       2 |  2183 |     99% |
| layout   |     17 |        10 |       7 |  2277 |    107% |
| perf     |     26 |        11 |       8 |  3239 |  *143%* |
| persist  |     15 |        10 |       4 |  3237 |    118% |
| binary   |     25 |         6 |       4 |  3896 |  *130%* |
| db       |     27 |         3 |       4 |  2202 |     95% |
| build    |     18 |         8 |       4 |  1822 |     94% |
| pack     |     23 |         8 |       4 |  3001 |  *121%* |
| ftp      |     19 |         4 |       3 |  1814 | **79%** |
| http     |     18 |         9 |       3 |  2256 |    105% |
| viewer   |     32 |         3 |       2 |  2955 |    116% |
| undo     |     20 |         0 |       2 |  1239 | **55%** |
| vm       |     19 |        10 |       6 |  2242 |    110% |
| debugger |     21 |        10 |       4 |  2808 |  *123%* |
| finale   |      3 |         0 |       1 |   485 | **38%** |
| Total    |    504 |       154 |      94 | 54593 |     92% |
| Average  |   18.7 |       5.7 |     3.5 |  2021 |         |
| Chapter  | Slides | Exercises | Figures | Words | Overall |
|:---------|-------:|----------:|--------:|------:|--------:|
| intro    |     10 |         0 |       2 |  1024 |    102% |
| dup      |     19 |         5 |       5 |  1752 |     82% |
| glob     |     22 |         8 |       4 |  1763 |    100% |
| parse    |     15 |         3 |       3 |  1194 | **58%** |
| test     |     16 |         7 |       4 |  1933 |     88% |
| interp   |     16 |         8 |       2 |  1921 |     92% |
| oop      |     17 |         2 |       4 |  1021 | **55%** |
| func     |     19 |         4 |       3 |  1422 | **73%** |
| mock     |      5 |         1 |       1 |  1239 | **32%** |
| archive  |     19 |         7 |       3 |  2132 |     96% |
| check    |     20 |         0 |       3 |  1296 | **56%** |
| template |     23 |        10 |       2 |  2240 |    118% |
| lint     |     20 |         7 |       2 |  2183 |     99% |
| layout   |     17 |        10 |       7 |  2277 |    107% |
| perf     |     26 |        11 |       8 |  3239 |  *143%* |
| persist  |     15 |        10 |       4 |  3237 |    118% |
| binary   |     25 |         6 |       4 |  3896 |  *130%* |
| db       |     27 |         3 |       4 |  2202 |     95% |
| build    |     18 |         8 |       4 |  1822 |     94% |
| pack     |     23 |         8 |       4 |  3001 |  *121%* |
| ftp      |     19 |         4 |       3 |  1814 | **79%** |
| http     |     18 |         9 |       3 |  2256 |    105% |
| viewer   |     32 |         3 |       2 |  2955 |    116% |
| undo     |     20 |         0 |       2 |  1239 | **55%** |
| vm       |     19 |        10 |       6 |  2242 |    110% |
| debugger |     21 |        10 |       4 |  2808 |  *123%* |
| finale   |      3 |         0 |       1 |   485 | **38%** |
| Total    |    504 |       154 |      94 | 54593 |     92% |
| Average  |   18.7 |       5.7 |     3.5 |  2021 |         |
