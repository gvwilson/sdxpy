---
template: slides
title: "Matching Patterns"
---

## The Problem

-   `glob.glob` finds files whose names match patterns

-   `2023-*.{pdf,txt}` matches `2023-01.txt` and `2023-final.pdf`
    but not `draft-2023.docx`

[% figure
   slug="glob-examples"
   img="examples.svg"
   alt="Matching examples"
   caption="Examples of glob matching."
%]

-   How does this work?

---

<!--# class="aside" -->

## Why "Globbing"?

-   Early versions of Unix had a tool called `glob`

-   People used pattern matching so often
    that it was quickly built into the shell

---

## Write a Few Tests

| Pattern | Text     | Match? || Pattern | Text     | Match? |
| ------- | -------- | ------ || ------- | -------- | ------ |
| abc     | "abc"    | True   || a*c     | "abc"    | True   |
| ab      | "abc"    | False  || {a,b}   | "a"      | True   |
| abc     | "ab"     | False  || {a,b}   | "c"      | False  |
| *       | ""       | True   || {a,b}   | "ab"     | False  |
| *       | "abc"    | True   || *{x,y}  | "abcx"   | True   |

---

## Objects vs. Functions

-   Create matchers for particular cases instead of one big function

-   Some of those matchers need extra data

    -   E.g., which literal characters to match

-   So create objects

---

## Design Patterns

-   Use the [%g chain_of_responsibility_pattern "Chain of Responsibility" %] pattern

    -   Each object matches if it can…

    -   …then asks something else to try to match the rest of the text

[% figure
   slug="glob-chain"
   img="chain.svg"
   alt="Chain of Responsibility"
   caption="Matching with Chain of Responsibility."
%]

---

## Matching a Literal String

[%inc glob_lit.py %]

-   `chars` is the characters to be matched
-   `rest` is the rest of the chain (or `None`)
-   `start` is needed when this isn't the first matcher

---

## Testing the Matcher

[%inc test_glob_lit.py mark=tests %]

-   Give tests long names to make failure reports immediately readable

---

## Does Chaining Work?

-   Try to find flaws in the design as early as possible

-   So test chaining before writing more matchers

[%inc test_glob_lit.py mark=chain %]

---

<!--# class="aside" -->

## Test-Driven Development

-   Some people write tests *before* writing code to clarify the design

    -   And to ensure they actually write tests

-   Research shows the order doesn't matter [%b Fucci2016 %]

-   What *does* is alternating between short bursts of coding and testing

---

## Wildcards

-   `*` can match zero or more characters

-   If it's the last matcher, it always succeeds

-   Otherwise try zero characters, one, two, etc. characters

[%inc glob_any.py %]

---

## And We Test It


[%inc test_glob_any.py mark=tests %]

---

## Matching Alternatives

[%inc glob_either.py %]

---

## And We Test It

[%inc test_glob_either.py mark=tests %]

---

## But Wait…

[%inc test_glob_problem.py mark=keep %]
[%inc test_glob_problem.out %]

-   `Either` doesn't handle `rest` properly

---

## Rethinking

-   We now have three matchers with the same interfaces
    -   [%g refactor "Refactor" %] using
        [%g extract_parent_class_refactoring "Extract Parent Class" %]
-   The test `if self.rest is None` appears several times
    -   Use the [%g null_object_pattern "Null Object" %] pattern instead

[% figure
   slug="glob-refactoring"
   img="refactoring.svg"
   alt="Refactoring matchers"
   caption="Using the Extract Parent Class refactoring."
%]

---

<!--# class="aside" -->

## We Didn't Invent This

<div class="center">
[% image src="gamma-design-patterns.webp" alt="Design Patterns book cover" width="25%" %]
[% image src="fowler-refactoring.webp" alt="Refactoring book cover" width="25%" %]
[% image src="kerievsky-refactoring-to-patterns.webp" alt="Refactoring to Patterns book cover" width="22%" %]
</div>

-   [%b Tichy2010 %] showed that learning these patterns
    makes people better programmers

---

## The Parent Class

[%inc glob_null.py mark=parent %]

-   Assume every child class has a `_match` method

-   This method returns the location to continue searching

-   So `Match.match` checks that we've reached the end of the text

---

## The Null Object Class

[%inc glob_null.py mark=null %]

-   Must be the last one in the chain

-   Doesn't advance the match (i.e., does nothing)

-   Every other class can now delegate to its `next`
    without checking for `None`

---

## Refactoring Literal Matcher

[%inc glob_null.py mark=lit %]

-   Ask parent class to do common initialization
-   Return `None` for "no match" or whatever `self.rest` returns
    -   If `rest` is `Null`,
        result will be the index after this object's match

---

## Refactoring Wildcard

[%inc glob_null.py mark=any %]

-   The exercises will ask, "Why `len(text) + 1`?"

---

## Refactoring Alternatives

[%inc glob_null.py mark=either %]

-   Looping over left and right options is simpler than
    repeating code or writing a helper method

-   Could easily be extended to any number of alternatives

---

## Testing

-   None of the existing tests change
    -   None of the constructors changed
    -   Neither did the signature of `match`
-   We should (should) add a couple of tests for `Null`
-   But basically we're done
-   And we can easily add matchers for other kinds of patterns

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="glob-concept-map"
   img="concept_map.svg"
   alt="Concept map of globbing"
   caption="Concept map"
%]
