---
template: slides
title: "Finding Duplicate Files"
---

## Overview

-   We want to find duplicate files, but can't rely on their names

-   Comparing pairs of files byte by byte is slow

    -   And gets slower per file as the number of files grows

-   Better approach:

    -   Calculate an identifier for each file that depends on its content

    -   Group files with the same identifier and compare those

-   Even better: calculate identifiers so that if two files have the same ID, they're guaranteed to have the same content

---

## Start Simple

-   Take filenames as command-line arguments

-   Generate and print a list of duplicate pairs

[%inc brute_force_1.py mark=main %]

---

## Byte by Byte

[%inc brute_force_1.py mark=bytes %]

-   `open(filename, "r")` opens a file for reading characters

-   But images, audio clips, etc. aren't character data

-   So use <code>open(filename, "r<strong>b</strong>")</code> to open in [% g binary_mode "binary mode" %]

    -   Look at the difference in more detail in [%x binary %]

---

## Test Case

-   Create a `tests` directory with six files

| `a1.txt` | `a2.txt` | `a3.txt` | `b1.txt` | `b2.txt` | `c1.txt` |
| ---- | ---- | ---- | ---- | ---- | ---- |
| aaa | aaa | aaa | bb | bb | c |

-   Expect the three `a` files and the two `b` files to be reported as duplicates

-   No particular reason for these tests—we just have to start somewhere

---

## Test Output

[%inc brute_force_1.sh %]
[%inc brute_force_1.out %]

-   Oops

---

## Revise Our Approach

[%inc brute_force_2.py mark=dup %]

[% figure
   slug="dup-triangle"
   img="triangle.svg"
   alt="Looping over distinct combinations"
   caption="Scoping the inner loop to produce unique combinations."
%]

---

## Algorithmic Complexity

-   \\( N \\) objects can be paired in \\( N(N-1)/2 \\) ways

-   So for very large \\( N \\), work is proportional to \\( N^2 \\)

-   Computer scientist would say "[%g time_complexity "time complexity" %] is \\( O(N^2) \\)"

    -   Pronounced "[%g big_oh "big-oh" %] of N squared"

-   In practice, this means that the time per file increases as the number of files increases

-   Sometimes unavoidable, but in this case there's a better way

---

## Grouping Files

-   Process each file once to produce a short identifier

-   I.e., use a [% g hash_function "hash function" %] to produce a [% g hash_code "hash code" %]

-   Only compare files with the same identifier

[% figure
   slug="dup-hash-group"
   img="hash_group.svg"
   alt="Grouping by hash code"
   caption="Grouping by hash code reduces comparisons from 15 to 4."
%]

---

## Naive Hashing

-   Bytes are just numbers

[%inc naive_hash.py mark=hash %]

[%inc naive_hash.py mark=example %]

[%inc naive_hash.out %]

---

## How Good Is This?

-   Want all hash codes to be equally likely

    -   Large file groups are disproportionately expensive

-   Hash each line of the novel *Dracula* and plot distribution

[% figure
   slug="dup-naive-dracula"
   img="naive_dracula.svg"
   alt="Hash codes of *Dracula*"
   caption="Distribution of hash codes per line in *Dracula*."
%]

---

## After a Little Digging…

-   Our text file uses a blank line to separate paragraphs

-   So it's no surprise that 0 is the most common hash code

-   Look at the distribution of hash codes of *unique* lines

[% figure
   slug="dup-naive-dracula-unique"
   img="naive_dracula_unique.svg"
   alt="Hash codes of unique lines of *Dracula*"
   caption="Distribution of hash codes per unique line in *Dracula*."
%]

---

## Modifying Our Program

-   Build a dictionary with hash codes as keys and sets of files as values

[%inc grouped.py mark=group %]

-   If we haven't seen this key before, add it with an empty value

---

## Modifying Our Program

-   We can re-use most of the previous code

[%inc grouped.py mark=main %]

[%inc grouped.out %]

---

## But We Can Do Better

-   Use a [%g cryptographic_hash_function "cryptographic hash function" %]

    -   Output is completely deterministic

    -   But also unpredictable

    -   And distributed like a uniform random variable

-   Output depends on *order* of input as well as *value*

    -   With overwhelming probability, any change in input will produce a different output

---

## We Don't Need Groups

-   Odds that two people don't share a birthday are \\( 364/365 \\)

-   Odds that three people don't have are \\( (364/365) {\times} (363/365) \\)

-   There's a 50% chance of two people sharing a birthday in a group of 23 people
    and a 99.9% chance with 70 people

-   How many files do we need to hash before there's a 50% chance of a [%g hash_collision "collision" %]
    with a 256-bit hash?

-   Answer is "approximately \\( 4{\times}10^{38} \\) files"

-   We're willing to take that risk

---

## SHA-256 Example

[%inc using_sha256.py mark=example %]

[%inc using_sha256.out %]

-   `hexdigest` gives [%g hexadecimal "hexadecimal" %] representation of 256-bit hash code

---

## Duplicate Finder

[%inc dup.py %]

---

## Duplicate Finder

[%inc dup.sh %]
[%inc dup.out %]

-   Runtime is \\(O(N)\\), i.e., fixed time per file

-   Which is as good as it can possibly be

---

<!--# class="aside" -->

## Learning Debt

-   What else can we use hashing for?

    -   Dictionaries

    -   Version control

-   How can we test our duplicate finder?

-   How can we make sure the code follows style guidelines?

-   How can we package it for others to use?

---

<!--# class="summary" -->

## Summary

[% figure
   slug="dup-concept-map"
   img="concept_map.svg"
   alt="Concept map for finding duplicate files"
   caption="Concept map for duplicate file detection with hashing."
%]
