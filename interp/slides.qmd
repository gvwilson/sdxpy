---
title: "An Interpreter"
---

<section class="slide" markdown="1">

## Background

-   Programs are just data
-   Compilers and interpreters are just programs
    -   Compiler: generate instructions once in advance
    -   Interpreter: generate instructions on the fly
    -   Differences are increasingly blurry in practice
-   Most have a [%g parser "parser" %] and a [%g runtime "runtime" %]
-   Look at the latter in this lesson to see how programs actually run

</section>
<section class="slide" markdown="1">

## Representing Expressions

-   Represent simple arithmetic operations as lists

[%inc add_example.py %]

-   We use special [%g infix_notation "infix notation" %] like `1+2` for historical reasons
-   Always putting the operation first makes processing easier

</section>
<section class="slide" markdown="1">

## Evaluating Expressions

[%inc expr.py mark=do_add %]

-   `args` is everything _except_ the name of the operation
-   Use an as-yet-unwritten function `do` to evaluate the operands
-   Then add their values

</section>
<section class="slide" markdown="1">

## Evaluating Expressions

[%inc expr.py mark=do_abs %]

-   All the `do_` functions can be called interchangeably
-   Like the unit test functions of [%x test %]

</section>
<section class="slide" markdown="1">

## Dispatching Operations

-   Write a function that [%g dynamic_dispatch "dispatches" %] to actual operations

[%inc expr.py mark=do %]

</section>
<section class="slide" markdown="1">

## Dispatching Operations

[% figure
  slug="interp-recursive-evaluation"
  img="recursive_evaluation.svg"
  alt="Recursive evaluation of an expression tree"
  caption="Recursively evaluating an expression tree"
%]

</section>
<section class="slide" markdown="1">

## An Example

[%inc expr.tll %]
[%inc expr.sh %]
[%inc expr.out %]

</section>
<section class="slide" markdown="1">

## Environments

-   Store variables in a dictionary that's passed to every `do_` function
    -   Like the dictionary returned by the `globals` function
    -   An [%g environment "environment" %]

[%inc vars.py mark=do_abs %]

</section>
<section class="slide" markdown="1">

## Getting Variables' Values

-   Choices for getting variables' values:
    1.  Assume strings are variable names
    2.  Define another function that we call explicitly

[%inc vars.py mark=do_get %]

[%inc vars.py mark=do_set %]

</section>
<section class="slide" markdown="1">

## Sequencing

-   Need a way to set values before evaluating expressions
-   `["seq", ["set", "a", 1], ["add", ["get", "a"], 2]]`

[%inc vars.py mark=do_seq %]

</section>
<section class="slide" markdown="1">

## Everything Is An Expression

-   Python distinguishes [%g expression "expressions" %] that produce values
    from [%g statement "statements" %] that don't
-   But it doesn't have to, and many languages don't

[%inc ex_assign_expr.py %]

</section>
<section class="slide" markdown="1">

## Doubling

[%inc doubling.tll %]

</section>
<section class="slide" markdown="1">

## Doubling

[%inc doubling.out %]

</section>
<section class="slide" markdown="1">

## This Is Tedious

[%inc vars.py mark=do %]

-   But we know what to do

</section>
<section class="slide" markdown="1">

## Introspection

[%inc vars_reflect.py mark=lookup %]

</section>
<section class="slide" markdown="1">

## How Good Is Our Design?

-   One way to evaluate a design is to ask how [%g extensibility "extensible" %] it is
-   The answer for the interpreter is "pretty easily"
-   The answer for our little language is "not at all"
-   We need a way to define and call functions of our own
-   We will tackle this in [%x func %]

</section>
<section class="slide" markdown="1">

## Summary	       

[% figure
   slug="interp-concept-map"
   img="concept_map.svg"
   alt="Concept map"
   caption="Concept map."
%]

</section>
