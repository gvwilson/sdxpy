---
title: "Pattern Matching"
syllabus:
- FIXME
---

Sooner or later everyone needs to scrape data out of text files.
Regular expressions are the best tool for the job,
so this chapter explores how they work by building a simple but extensible pattern matcher.
Our approach is inspired by [%i "Kernighan, Brian" %]Brian Kernighan's[%/i%] entry
in [% b Oram2007 %].

## Simple Patterns {: #pattern-matching-simple}

Our matcher will initially handle just the five cases shown in
[%t pattern-matching-cases %].
These cases are a small subset of what JavaScript provides,
but as [%i "Kernighan, Brian" %]Kernighan[%/i%] wrote,
"This is quite a useful class;
in my own experience of using regular expressions on a day-to-day basis,
it easily accounts for 95 percent of all instances."

<div class="table" id="pattern-matching-cases" caption="Pattern matching cases." markdown="1">
| Meaning                   | Character |
| ------------------------- | --------- |
| Any literal character *c* | *c*       |
| Any single character      | .         |
| Beginning of input        | ^         |
| End of input              | $         |
| Zero or more of something | *         |
</div>

Matching is conceptually simple.
If the first element of the pattern matches where we are,
we see if the rest of the pattern matches what's left;
otherwise,
we see if the the pattern will match further along.
The function users call handles the special case of `^` at the start of a pattern
matching the start of the target string being searched.
It then tries the pattern against each successive substring of the target string
until it finds a match or runs out of characters:

[% excerpt f="simple_regexp.py" keep="match" %]

`match_here` does the matching and recursing:

[% excerpt f="simple_regexp.py" keep="match_here" %]

We use a table of test cases and expected results to test it:

[% excerpt f="simple_regexp.py" keep="tests" %]
[% excerpt f="simple_regexp.out" %]

This program seems to work,
but it actually contains an error that we will correct in the exercises.
(Think about what happens if we match the pattern `a*ab` against the string `'aab'`.)
It is also hard to extend:
`match_here` is already very complicated,
and handling parentheses in patterns like `a(bc)*d` will make it more complicated still.

## A Direct Matcher {: #pattern-matching-direct}

Instead of packing all our code into one function,
we can implement each kind of match separately.
Doing this makes it easier to add more matchers:
we just define something we can mix in with the matchers we already have.

Rather than matching text immediately,
though,
we will create objects that know how to do matches
so that we can build a complex matcher once and re-use it many times.
This is a common pattern in text processing:
we may want to apply a regular expression to each line in a large set of files,
so recycling matchers makes programs more efficient.

Each matching object has a method
that takes the target string and the index to start matching at as inputs.
Its output is the index to continue matching at
or `None` indicating that matching failed.
We can combine these objects to match complex patterns.

The first step to implement this is to write test cases,
which forces us to define how our classes will work:

[% excerpt f="direct.py" keep="tests" %]

Next,
we define a [%g base_class "base class" %] that all matchers will inherit from.
This class contains the `match` method that users will call
so that we can start matching right away
no matter what kind of matcher we have at the top level of our pattern.

[% excerpt f="direct.py" keep="base_class" %]

The base class defines a `match` method
that other classes will fill in with actual matching code.
The base implementation of this method always returns `None`
so that if we forget to implement it in a derived class,
matching will always fail.
{: .continue}

We can now define each matching class,
like this one for literal characters:

[% excerpt f="direct.py" keep="lit" %]

Our tests now run, but most of them fail:
"most" because we expect some tests not to match,
so the test runner reports `true`.
This output tells us how much work we have left to do:
when all of these tests pass,
we're finished.
{: .continue}

What about repetition?
It can just apply a pattern over and over to consume as many matches as possible---or can it?
Suppose we have the pattern `a*ab`.
This ought to match the text `"ab"`, but will it?
`*` is [%i "greedy algorithm" "algorithm!greedy" %][%g greedy_algorithm "greedy" %][%/i%]:
it matches as much as it can.
(This is also called [%i "eager matching" "matching!eager" %][%g eager_matching "eager matching" %][%/i%].)
As a result,
`a*` will match the leading `"a"`, leaving nothing for the literal `a` to match.
Our current implementation doesn't give us a way to try other possible matches when this happens.

## An Alternative Design {: #pattern-matching-alternative}

Let's re-think our design
and have each matcher take its own arguments and a `rest` parameter containing the rest of the matchers
([% fixme pattern-matching-rest %]).
(We will provide a default of `None` in the creation function
so we don't have to type `None` over and over again.)
Each matcher will try each of its possibilities and then see if the rest will also match:

[% excerpt f="re_base.py" %]

[% fixme
   slug="pattern-matching-rest"
   img="figures/rest.svg"
   alt="Matching the rest of the pattern"
   caption="Using "rest" to match the remainder of a pattern."
%]

This design means we can get rid of `Seq`,
but it does mean our expressions become deeply nested.
For example, the expression to match `ab*c` is:

```{: .python}
Lit("a", Any(Lit("b"), Lit("c")))
```

Here's how this strategy works for matching a literal expression:

[% excerpt f="re_lit.py" %]

The `_match` method checks whether all of the pattern matches the target text
starting at the current location.
If so,
it checks whether the rest of the overall pattern matches what's left.
Matching the start `^` and end `$` anchors is just as straightforward.

[% excerpt f="re_start.py" %]

[% excerpt f="re_end.py" %]

Matching either/or is done by trying the first pattern and the rest,
and if that fails,
trying the second pattern and the rest:

[% excerpt f="re_alt.py" %]

To match a repetition,
we figure out the maximum number of matches that might be left,
then count down until something succeeds.
(We start with the maximum because matching is supposed to be greedy.)
Each non-empty repetition matches at least one character,
so the number of remaining characters is the maximum number of matches worth trying.

[% excerpt f="re_any.py" %]

With these classes in place,
our tests all pass:

[% fixme f="re_main.out" %]

The most important thing about this design is how extensible it is:
if we want to add other kinds of matching,
all we have to do is add more classes.
That extensibility comes from the lack of centralized decision-making,
which in turn comes from our use of [%i "polymorphism" %][%g polymorphism "polymorphism" %][%/i%]
and the [%i "Chain of Responsibility pattern" "design pattern!Chain of Responsibility" %][%g chain_of_responsibility_pattern "Chain of Responsibility" %][%/i%] design pattern.
Each component does its part and asks something else to handle the remaining work;
so long as each component takes the same inputs,
we can put them together however we want.

> ### The Open-Closed Principle
>
> The [%i "Open-Closed Principle" "software design!Open-Closed Principle" %][%g open_closed_principle "Open-Closed Principle" %][%/i%] states that
> software should be open for extension but closed for modification,
> i.e., that it should be possible to extend functionality
> without having to rewrite existing code.
> As we said in [% fixme %],
> this allows old code to use new code,
> but only if our design permits the kinds of extensions people are going to want to make.
> Since we can't anticipate everything,
> it is normal to have to revise a design the first two or three times we try to extend it.
> As [% b Brand1995 %] said of buildings,
> the things we make learn how to do things better as we use them.

## Exercises {: #pattern-matching-exercises}

### Find and Fix the Error {: .exercise}

The first regular expression matcher contains an error:
the pattern `'a*ab'` should match the string `'aab'` but doesn't.
Figure out why it fails and fix it.

### One More Than Length {: .exercise}

The main loop in `RegexBase.match` has `+1` inside the `range` call.
Which test(s) break when this is removed and why?

### Find All {: .exercise}

Modify the regular expression matcher to return *all* matches rather than just the first one.

### Find One or More {: .exercise}

Extend the regular expression matcher to support `+`, meaning "one or more".

### Match Sets of Characters {: .exercise}

Add a new regular expression matching class that matches any character from a set,
so that `Charset('aeiou')` matches any lower-case vowel.

### Make Repetition More Efficient {: .exercise}

Rewrite `Any` so that it does not repeatedly re-match text.

### Lazy Matching {: .exercise}

The regular expressions we have seen so far are [%g eager_matching "eager" %]:
they match as much as they can, as early as they can.
An alternative is [%g lazy_matching "lazy matching" %],
in which expressions match as little as they need to.
For example,
given the string `"ab"`,
an eager match with the expression `ab*` will match both letters
(because `b*` matches a 'b' if one is available)
but a lazy match will only match the first letter
(because `b*` can match no letters at all).
Implement lazy matching for the `*` operator.

### Optional Matching {: .exercise}

The `?` operator means "optional",
so that `a?` matches either zero or one occurrences of the letter 'a'.
Implement this operator.
