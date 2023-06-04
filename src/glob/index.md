---
title: "Matching Patterns"
syllabus:
-   Use globs and regular expressions to match patterns in text.
-   Use inheritance to make matchers composable and extensible.
-   Simplify code by having objects delegate work to other objects.
---

We had to tell the duplicate file finder of [%x dup %] which files to compare.
It would be more useful if it could find files itself,
and more useful still if we could tell it to check
files whose names matched patterns like `*.png`.

Early versions of Unix had a tool called [`glob`][unix_glob] to do this.
The name was short for "global",
and older programmers (like this author)
still use the word [%g globbing "globbing" %]
to mean "matching filenames against a pattern".
The Python standard library includes a module called [`glob`][py_glob]
to match filenames in the same way.
For example,
`2023-*.{pdf,txt}` matches `2023-01.txt` and `2023-final.pdf` but not `draft-2023.docx`
([%f glob-examples %]).
In this chapter,
we will implement a simple version of globbing
to show how pattern matching works in general.

[% figure
   slug="glob-examples"
   img="examples.svg"
   alt="Matching examples"
   caption="Examples of glob matching."
%]

## Simple Patterns {: #glob-simple}

Globbing patterns are simpler than
the [%g regular_expression "regular expressions" %]
used to scrape data from text files.
Our matcher will handle only the cases shown in
[%t pattern-glob-cases %].

<div class="table" id="pattern-glob-cases" caption="Pattern matching cases" markdown="1">
| Pattern | Text     | Match? || Pattern | Text     | Match? |
| ------- | -------- | ------ || ------- | -------- | ------ |
| abc     | "abc"    | True   || a*c     | "abc"    | True   |
| ab      | "abc"    | False  || {a,b}   | "a"      | True   |
| abc     | "ab"     | False  || {a,b}   | "c"      | False  |
| *       | ""       | True   || {a,b}   | "ab"     | False  |
| *       | "abc"    | True   || *{x,y}  | "abcx"   | True   |
</div>

Matching is conceptually simple.
If the first element of the pattern
matches the target string at the current location,
we check if the rest of the pattern matches what's left of the string.
If it doesn't,
or if we don't get to the end of the string,
matching fails.
(This behavior makes globbing different from regular expressions,
which can match parts of strings.)

In some cases all we need is the type of match:
for example, the `*` pattern matches any characters.
In other cases, though,
we need some extra information,
such as the literal text `"abc"` or the two alternatives `"x"` and `"y"`.
We will therefore create objects to do matching
rather than using bare functions.

Our design uses
the [%g chain_of_responsibility_pattern "Chain of Responsibility" %] pattern.
Each object matches if it can,
then delegates the rest of the match to the next object in the chain
([%f glob-chain %]).

[% figure
   slug="glob-chain"
   img="chain.svg"
   alt="Chain of Responsibility"
   caption="Matching with Chain of Responsibility."
%]

Our first matcher checks whether a fixed piece of text like `"abc"`
matches a string:

[% inc file="glob_lit.py" %]

`chars` is the characters to be matched,
while `rest` is the chain responsible for matching the rest of the text.
If `rest` is `None`,
this matcher is the last one in the chain,
so it must match to the end of the target string.
Finally,
`start` is needed when this matcher isn't the first one in the chain.

Before building our second matcher,
let's write and run a few tests for this one:

[% inc file="test_glob_lit.py" keep="tests" %]

Notice that we give tests long names
so that failure reports from the test runner are easier to read.
{: .continue}

We could go ahead and build some more matchers right away,
but as [%b Petre2016 %] explains,
good programmers build and check
the parts of their code that they are *least* sure of
as early as possible
to find out if their entire design is going to work or not.
We therefore write a test to make sure that chaining works
when one literal matcher is followed by another:

[% inc file="test_glob_lit.py" keep="chain" %]

<div class="callout" markdown="1">

## Test-Driven Development

Some programmers write the tests for a piece of code before writing the code itself.
This practice is called [%g tdd "test-driven development" %],
and its advocates claim that it produces better code in less time
because (a) writing tests helps people think about what the code should do
before they're committed to a particular implementation
and (b) if people write tests first,
they'll actually write tests.
Research shows that the order doesn't actually make a difference [%b Fucci2016 %];
what does is alternating in short bursts between testing and coding.

</div>

These tests pass,
so we're ready to move on to wildcards.
A `*` character in our pattern matches zero or more characters,
so if there are no more matchers in the chain,
then this `*` matches to the end of the target string
and `match` returns `True` right away.
If there *are* other matchers,
on the other hand,
we try matching no characters, one character, two characters, and so on
and see if those other matchers can get us to the end of the string if we do so.
If nothing works,
the match fails:

[% inc file="glob_any.py" %]

[% inc file="test_glob_any.py" keep="tests" %]

Either/or matching works much the same way.
If the first alternative matches we try the rest of the chain.
If not,
we try the second alternative,
and if neither gives us a match,
we fail:

[% inc file="glob_either.py" %]
[% inc file="test_glob_either.py" keep="tests" %]

But further testing uncovers a bug:

[% inc file="test_glob_problem.py" keep="keep" %]
[% inc file="test_glob_problem.out" %]

Our `Either` matcher doesn't handle `rest` properly.
We can try to patch it using our current design,
but we've accumulated a bit of [%g technical_debt "technical debt" %]
that we should clear up.

## Rethinking {: #glob-rethink}

We now have three matchers with the same interfaces.
Before we do any further work,
we will [%g refactor "refactor" %]
using [%g extract_parent_class_refactoring "Extract Parent Class" %]
to eliminate duplicated code ([%f glob-refactoring %]).
Similarly,
the test `if self.rest is None` appears several times.
We can simplify this by creating a class to represent "nothing here",
which is known as the [%g null_object_pattern "Null Object" %] pattern.

[% figure
   slug="glob-refactoring"
   img="refactoring.svg"
   alt="Refactoring matchers"
   caption="Using the Extract Parent Class refactoring."
%]

<div class="callout" markdown="1">

## We Didn't Invent This

We didn't invent any of the patterns or refactorings used in this chapter.
Instead, we learned them from books like [%b Gamma1994,Fowler2018,Kerievsky2004 %].
And as [%b Tichy2010 %] showed,
learning these patterns makes people better programmers.

</div>

Our new parent class `Match` looks like this:

[% inc file="glob_null.py" keep="parent" %]

It assumes every child class has a `_match` method
that returns the location from which searching is to continue
rather than just `True` or `False`.
`Match.match` therefore checks that we've reached the end of the text.

The Null Object class is:

[% inc file="glob_null.py" keep="null" %]

The null object must be the last one in the chain,
and as advertised,
it doesn't advance the match (i.e., it does nothing).
Every other matcher can now pass responsibility down the chain
without having to test whether it's at the end or not.
{: .continue}

With these changes in place,
our literal matcher becomes:

[% inc file="glob_null.py" keep="lit" %]

`Lit`'s constructor calls the constructor of its parent class
to initialize the things that all classes share,
then adds the data specific to this class.
It returns `None` for "no match" or whatever `self.rest` returns
If this object's `rest` is an instance of `Null`,
this result will be the index after our match.
{: .continue}

As before,
the matcher for `*` checks what happens
if it matches an ever-larger part of the target string:

[% inc file="glob_null.py" keep="any" %]

(The exercises will ask why loop has to run to `len(text) + 1`.)
Finally,
the matcher for either/or alternatives that initially prompted this refactoring
becomes:
{: .continue}

[% inc file="glob_null.py" keep="either" %]

Looping over the left and right alternative
saves us from repeating code or introducing a [%g helper_method "helper method" %].
It also simplifies the handling of more than two options,
which we explore in the exercises.
{: .continue}

Crucially,
none of the existing tests change
because none of the matching classes' constructors changed
and the [%g signature "signature" %] of the `match` method
(which they now [%g inheritance "inherit" %] from the generic `Match` class)
stayed the same as well.
We should (should) add a couple of tests for `Null`,
but basically we have now met our original goal,
and as the exercises will show,
we can easily add matchers for other kinds of patterns.

## Summary {: #glob-summary}

[% figure
   slug="glob-concept-map"
   img="concept_map.svg"
   alt="Concept map for regular expression matching"
   caption="Regular expression matching concept map."
%]

## Exercises {: #glob-exercises}

### Length Plus One {: .exercise}

Why does the upper bound of the loop in the final version of `Any`
run to `len(text) + 1`?

[% inc file="glob_null.py" keep="any" %]

### Find One or More {: .exercise}

Extend the regular expression matcher to support `+`,
meaning "match one or more characters".

### Match Sets of Characters {: .exercise}

1.  Add a new matching class that matches any character from a set,
    so that `Charset('aeiou')` matches any lower-case vowel.

2.  Create a matcher that matches a range of characters.
    For example,
    `Range("a", "z")` matches any single lower-case Latin alphabetic character.
    (This is just a convenience matcher: ranges can always be spelled out in full.)

3.  Write some tests for your matchers.

### Make Repetition More Efficient {: .exercise}

Rewrite `Any` so that it does not repeatedly re-match text.

### Exclusion {: .exercise}

1.  Create a matcher that *doesn't* match a specified pattern.
    For example, `Not(Lit("abc"))` only succeeds if the text isn't "abc".

2.  Write some tests for it.

### Multiple Alternatives {: .exercise}

1.  Modify `Either` so that it can match any number of sub-patterns, not just two.

2.  Write some tests for it.

3.  What does your implementation do when no sub-patterns are specified?
