---
abstract: >
    Pattern-matching is ubiquitous in computer programs.
    Whether we are selecting a set of files to open
    or finding names and email addresses inside those files,
    we need  an efficient way to find matches for complex patterns.
    This chapter therefore implements the filename matching used in the Unix shell
    to show how more complicated tools like regular expressions works.
syllabus:
-   Use globs and regular expressions to match patterns in text.
-   Use inheritance to make matchers composable and extensible.
-   Simplify code by having objects delegate work to other objects.
-   Use the Null Object pattern to eliminate special cases in code.
-   Use standard refactorings to move code from one working state to another.
-   Build and check the parts of your code you are least sure of first
    to find out if your design will work.
depends:
---

We used `*.txt` to tell the duplicate file finder of [%x dup %] which files to compare.
Older programmers (like this author) refer to this kind of pattern-matching as [%g globbing "globbing" %]
because early versions of Unix had a tool called [`glob`][unix_glob] to do it.
Globbing was so useful that it was quickly added to the shell,
and the [%i "Python standard library" %] includes a module called [`glob`][py_glob]
to match filenames in the same way.
For example,
`2023-*.{pdf,txt}` matches `2023-01.txt` and `2023-final.pdf` but not `draft-2023.docx`
([%f glob-examples %]).

[% figure
   slug="glob-examples"
   img="examples.svg"
   alt="Matching examples"
   caption="Examples of glob matching."
%]

Globbing patterns are simpler than
the [%g regular_expression "regular expressions" %]
used to scrape data from text files,
but the principles are the same.
This chapter therefore implements a simple version of globbing
to show how pattern-matching works in general.
This matcher will only handle the cases in [%t pattern-glob-cases %],
but as the exercises will show,
our design makes it easy to add new kinds of patterns.

<div class="table" id="pattern-glob-cases" caption="Pattern-matching cases." markdown="1">
| Pattern | Text     | Match? | Pattern  | Text     | Match? |
| ------- | -------- | ------ | -------- | -------- | ------ |
| `abc`   | "abc"    | true   | `a*c`    | "abc"    | true   |
| `ab`    | "abc"    | false  | `{a,b}`  | "a"      | true   |
| `abc`   | "ab"     | false  | `{a,b}`  | "c"      | false  |
| `*`     | ""       | true   | `{a,b}`  | "ab"     | false  |
| `*`     | "abc"    | true   | `*{x,y}` | "abcx"   | true   |
</div>

## Simple Patterns {: #glob-simple}

Matching is conceptually simple.
If the first element of the pattern
matches the target string at the current location,
we check if the rest of the pattern matches what's left of the string.
If the element doesn't match the front of the string,
or if the rest of the pattern can't match the rest of the string,
matching fails.
(This behavior makes globbing different from regular expressions,
which can match parts of strings.)

This design makes use of
the [%g chain_of_responsibility_pattern "Chain of Responsibility" %]
[%i "design pattern" %].
Each matcher matches if it can
then asks the next matcher in the chain to try to match the remaining text
([%f glob-chain %]).
Crucially,
objects don't know how long the chain after them is:
they just know whom to ask next.

[% figure
   slug="glob-chain"
   img="chain.svg"
   alt="Chain of Responsibility"
   caption="Matching with Chain of Responsibility."
%]

In some cases we only need to know what kind of matching we're doing:
for example, the `*` pattern matches any characters.
In other cases, though,
we need some extra information,
such as the literal text `"abc"` or the two alternatives `"pdf"` and `"txt"`.
We therefore decide to create matching objects that can hold this extra information
rather than just writing functions.

Our first matcher checks whether a piece of text like `"abc"`
matches a string.
We call this class `Lit` because a fixed string of characters
is sometimes called a [%g literal "literal" %],
and it has a constructor and a `match` method:

[% inc file="glob_lit.py" %]

`chars` is the characters to be matched,
while `rest` is responsible for matching the rest of the text.
If `rest` is `None`,
this matcher is the last one in the chain,
so it must match to the end of the target string.
{: .continue}

The `match` method takes the text to be matched as an input
along with an optional `start` parameter
that indicates where matching is to start.
This parameter has a default value of 0
(meaning "start at the beginning"),
but if this `Lit` follows other matchers,
they need to tell it where to start looking.
To see if this works,
let's write and run a few tests:

[% inc file="test_glob_lit.py" keep="tests" %]

Notice that we give tests long, meaningful names
to make failure reports from the test runner easier to read.
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

Chaining two literal matchers together is unnecessary:
we could (and probably should) write `Lit("ab")` instead of `Lit("a", Lit("b"))`.
However,
the fact that these two tests pass reassures us that our design is working.

<div class="callout" markdown="1">

### Test-Driven Development

Some programmers write the tests for a piece of code before writing the code itself.
This practice is called [%g tdd "test-driven development" %],
and its advocates claim that it yields better code in less time
because (a) writing tests helps people think about what the code should do
before they're committed to a particular implementation
and (b) if people write tests first,
they'll actually write tests.
However,
research shows that writing tests doesn't actually make a difference [%b Fucci2016 %];
what actually matters is alternating short bursts of testing and coding.

</div>

These tests for `Lit` pass,
so we're ready to move on to wildcards.
A `*` character in our pattern matches zero or more characters,
so if there are no more matchers in the chain,
then this `*` matches to the end of the target string
and `match` returns `True` right away.
If there *are* other matchers,
on the other hand,
we try matching no characters, one character, two characters, and so on
and see if those other matchers can get us to the end of the string if we do so.
If none of these possibilities succeeds,
the overall match fails
([%f glob-any %]).

<div class="pagebreak"></div>
[% figure
   slug="glob-any"
   img="any.svg"
   alt="Wildcard matching"
   caption="How wildcard matching works."
%]

[% inc file="glob_any.py" %]

Once again we write a few tests before moving on:
{: .continue}

[% inc file="test_glob_any.py" keep="tests" %]

Either/or matching works much the same way.
If the first alternative matches,
we try the rest of the chain.
If not,
we try the second alternative,
and if that doesn't work either,
we fail:

[% inc file="glob_either.py" %]

<div class="pagebreak"></div>

Our first few tests pass:

[% inc file="test_glob_either.py" keep="tests" %]

but further testing uncovers a bug:
{: .continue}

[% inc file="test_glob_problem.py" keep="keep" %]
[% inc file="test_glob_problem.out" %]

The problem is that `Either.match` isn't using `rest` properly—in fact,
it's not using `rest` at all
because it doesn't know what to pass it as a starting point.
Instead of having `match` methods return `True` or `False`,
we need them to return an indication of where the next match should start
so that `Either` can pass that information along to `rest`.
Before making this change,
we will clear up a bit of [%g technical_debt "technical debt" %] in our code.

## Rethinking {: #glob-rethink}

We now have three matchers with the same interfaces.
Before we do any further work,
we will [%g refactor "refactor" %]
using a pattern called [%g extract_parent_class_refactoring "Extract Parent Class" %]
to make the relationship between the matchers clear ([%f glob-refactoring %]).
At the same time,
each matcher is checking to see if its `rest` is `None`.
We can simplify this by creating a class to represent "nothing here",
which is known as the [%g null_object_pattern "Null Object" %] pattern.

[% figure
   slug="glob-refactoring"
   img="refactoring.svg"
   alt="Refactoring matchers"
   caption="Using the Extract Parent Class refactoring."
%]

<div class="callout" markdown="1">

### We Didn't Invent This

We didn't invent any of the patterns or refactorings used in this chapter.
Instead, we learned them from books like [%b Gamma1994 Fowler2018 Kerievsky2004 %].
And as [%b Tichy2010 %] showed,
learning these patterns makes people better programmers.

</div>

<div class="pagebreak"></div>

Our new parent class `Match` looks like this:

[% inc file="glob_null.py" keep="parent" %]

`Match.rest` requires every [%g child_class "child class" %] to have
a [%g helper_method "helper method" %] called `_match`
that returns the location from which searching is to continue.
`Match.match` checks whether the entire match reaches the end of the target string
and returns `True` or `False` as appropriate.
{: .continue}

Our new Null Object class looks like this:

[% inc file="glob_null.py" keep="null" %]

`Null` objects must be at the end of the matching chain,
i.e.,
their `rest` *must* be `None`,
so we remove the `rest` parameter from the class's constructor
and pass `None` up to the parent constructor every time.
Since `Null` objects don't match anything,
`Null._match` immediately returns whatever starting point it was given.
Every other matcher can now pass responsibility down the chain
without having to test whether it's the last matcher in line or not.
{: .continue}

With these changes in place,
our literal matcher becomes:

[% inc file="glob_null.py" keep="lit" %]

`Lit`'s constructor calls the constructor of its parent class
to initialize the things that all classes share,
then adds the data specific to this class.
It returns `None` for "no match" or whatever `self.rest` returns
If this object's `rest` is an instance of `Null`,
this result will be the index after the overall match.
{: .continue}

As before,
the matcher for `*` checks what happens
if it matches an ever-larger part of the target string:

[% inc file="glob_null.py" keep="any" %]

(The exercises will ask why loop has to run to `len(text) + 1`.)
Finally,
the either/or matcher that prompted this refactoring becomes:
{: .continue}

[% inc file="glob_null.py" keep="either" %]

Looping over the left and right alternative
saves us from repeating code or introducing a helper method.
It also simplifies the handling of more than two options,
which we explore in the exercises.
{: .continue}

Crucially,
none of the existing tests change
because none of the matching classes' constructors changed
and the [%g signature "signature" %] of the `match` method
(which they now [%g inheritance "inherit" %] from the generic `Match` class)
stayed the same as well.
We should add some tests for `Null`,
but we have now met our original goal,
and as the exercises will show we can easily add matchers for other kinds of patterns.

<div class="pagebreak"></div>

## Summary {: #glob-summary}

[%f glob-concept-map %] summarizes the key ideas in this chapter;
we will see the Null Object and Chain of Responsibility design patterns again.

[% figure
   slug="glob-concept-map"
   img="concept_map.svg"
   alt="Concept map for regular expression matching"
   caption="Regular expression matching concept map."
   cls="here"
%]

## Exercises {: #glob-exercises}

### Looping {: .exercise}

Rewrite the matchers so that a top-level object manages a list of matchers,
none of which know about any of the others.
Is this design simpler or more complicated than the Chain of Responsibility design?

### Length Plus One {: .exercise}

Why does the upper bound of the loop in the final version of `Any`
run to `len(text) + 1`?

### Find One or More {: .exercise}

Extend the regular expression matcher to support `+`,
meaning "match one or more characters".

### Match Sets of Characters {: .exercise}

1.  Add a new matching class that matches any character from a set,
    so that `Charset('aeiou')` matches any lower case vowel.

2.  Create a matcher that matches a range of characters.
    For example,
    `Range("a", "z")` matches any single lower case Latin alphabetic character.
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

### Returning Matches {: .exercise}

Modify the matcher so that it returns the substrings that matched
each part of the expression.
For example,
when `*.txt` matches `name.txt`,
the library should return some indication that `*` matched the string `"name"`.

### Alternative Matching {: .exercise}

The tool we have built implements [%g lazy_matching "lazy matching" %],
i.e.,
the `*` character matches the shortest string it can
that results in the overall pattern matching.
Modify the code to do [%g greedy_matching "greedy matching" %] instead,
and combine it with the solution to the previous exercise
for testing.
