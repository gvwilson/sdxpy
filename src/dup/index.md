---
title: "Finding Duplicate Files"
syllabus:
-   A hash function creates a fixed-size value from an arbitrary sequence of bytes.
-   The output of a hash function is deterministic but not predictable.
-   A cryptographic hash function's output is evenly distributed.
---

Suppose we want to find duplicates in a large collection of files.
We can't rely on their names because files can be copied and renamed.
We could compare files byte by byte,
but this slows down dramatically as the number of files increases,
since the number of pairs is proportional to the square of the number of files.

A more efficient strategy is to calculate an identifier for each file
that depends on the bytes in the file.
If two files have different hash codes they are guaranteed to be different,
so we only have to compare files whose hash codes match ([% f dup-match %]).

[% figure
   slug="dup-match"
   img="match.svg"
   alt="Hashing to match files"
   caption="Using hash codes to find files that might be identical."
%]

## How do hash functions work?

A [%i "hash function" %][%g hash_function "hash function" %][%/i%]
takes an arbitrary block of data as input
and produces a single number as an output
([% f dup-hash %]).
A hash function always produces the same [%i "hash code" %][%g hash_code "hash code" %][%/i%] for any input;
while the output looks random,
it is deterministic.

[% figure
   slug="dup-hash"
   img="hash.svg"
   alt="Hash functions"
   caption="How hash functions work."
%]

A simple hash function is just a few lines long.
This one converts each letter in a string to an integer using the `ord` function,
multiplies that by 7,
adds it to the value produced so far,
and then takes the remainder modulo 13:

[% inc file="naive_hash.py" keep="hash" %]

Let's test this function on successive substrings of the string `"example"`:

[% inc file="naive_hash.py" keep="example" %]
[% inc file="naive_hash.out" %]

The output of `naive_hash` seems random, but how random is it?
To find out,
we can use it to hash each unique line in the novel *Dracula*.
The result seems to be unevently distributed,
which means that if we used our hash function to group files together,
some groups would probably be larger than others
([%f dup-naive %]).

[% figure
   slug="dup-naive"
   img="naive_dracula.svg"
   alt="Hashing *Dracula*"
   caption="Distribution of hash codes for the novel *Dracula*."
%]

A [%i "cryptographic hash function" "hash function!cryptographic" %][%g cryptographic_hash_function "cryptographic hash function" %][%/i%]
produces outputs that look like uniformly distributed random numbers,
i.e.,
each possible hash code is equally likely.
It's hard to write a hash function that meets this condition,
so we will therefore use Python's [hashlib][py_hashlib] module
to calculate [%i "hash code!SHA256" "SHA256 hash code" %][%g sha256 "SHA256" %][%/i%] hashes of our files.
These are random enough to make
[%i "hash function!collision" "collision (in hashing)" %][%g collision "collision" %][%/i%]
extremely unlikely.

<div class="callout" markdown="1">

### The Birthday Problem

The odds that two people share a birthday are 1/365 (ignoring February 29).
The odds that they *don't* are therefore 364/365.
When we add a third person,
the odds that they don't share a birthday with either of the preceding two people are 363/365,
so the overall odds that nobody shares a birthday are (364/365)×(363/365).
If we keep going,
there's a 50% chance of two people sharing a birthday in a group of just 23 people,
and a 99.9% chance with 70 people.

The same math can tell us how many files we need to hash before there's a 50% chance of a collision
with a 256-bit hash.
According to [Wikipedia][birthday_problem],
the answer is approximately \\(4{\times}10^{38}\\) files.
We're willing to take that risk…

</div>

## How can we match identical files? {: #dup-match}

EXAMPLE

FIXME: hash a file

## Summary {: #backup-summary}

[% figure
   slug="dup-concept-map"
   img="concept_map.svg"
   alt="Concept map of finding duplicate files"
   caption="Concepts in this lesson."
%]

## Exercises {: #dup-exercises}

### Odds of collision {: .exercise}

If hashes were only 2 bits long,
then the chances of collision with each successive file
assuming no previous collision are:

| Number of Files | Odds of Collision |
| --------------- | ----------------- |
| 1               | 0%                |
| 2               | 25%               |
| 3               | 50%               |
| 4               | 75%               |
| 5               | 100%              |

A colleague of yours says this means that if we hash four files,
there's only a 75% chance of any collision occurring.
What are the actual odds?

### Streaming I/O {: .exercise}

FIXME

### Big Oh {: .exercise}

FIXME
