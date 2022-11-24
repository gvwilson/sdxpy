---
title: "A Package Manager"
syllabus:
- FIXME
---

- https://eerielinux.wordpress.com/2017/08/15/the-history-of-nix-package-management/
- https://twitter.com/stephenrkell/status/1559930052464283650

## Exhaustive Search {: #packman-exhaustive}

-   Specify package dependencies

[% inc file="triple.py" %]

-   Generate possibilities and then see which ones fit constraints

[% inc file="exhaustive.py" keep="main" %]

-   Generate possibilities with recursive enumeration

[% inc file="exhaustive.py" keep="possible" %]

-   Check for compatibility

[% inc file="exhaustive.py" keep="compatible" %]

-   18 possibilities reduce to 3 valid combinations

[% inc file="exhaustive.out" %]

## Incremental Search {: #packman-incremental}

-   Can we thin out possibilities as we go?
    -   Reverse the search order to make a point later

[% inc file="incremental.py" keep="main" %]

-   Check compatibility so far as we go

[% inc file="incremental.py" keep="find" %]

-   Search in the order keys are given

[% inc pat="incremental.*" fill="sh out" %]

-   Search in reverse order

[% inc pat="incremental_reverse.*" fill="sh out" %]

## {: #packman-smt}

- https://www.fuzzingbook.org/html/AcademicPrototyping.html

## Summary {: #builder-summary}

[% figure
   slug="packman-concept-map"
   img="packman_concept_map.svg"
   alt="Concept map for package manager."
   caption="Concepts for package manager."
%]

## Exercises {: #packman-exercises}

FIXME
