---
template: slides
title: "An Interpreter"
---

## Background

-   Programs are just data
-   Compilers and interpreters are just programs
    -   Compiler: generate instructions once in advance
    -   Interpreter: generate instructions on the fly
    -   Differences are increasingly blurry in practice
-   Most have a [%g parser "parser" %] and a [%g runtime "runtime" %]
-   Look at the latter in this lesson to see how programs actually run

---

## Representing Expressions

-   Represent simple arithmetic operations as lists

[%inc add_example.py %]

-   We use special [%g infix_notation "infix notation" %] like `1+2` for historical reasons
-   Always putting the operation first makes processing easier

---

## Evaluating Expressions

[%inc expr.py mark=do_add %]

-   `args` is everything _except_ the name of the operation
-   Use an as-yet-unwritten function `do` to evaluate the operands
-   Then add their values

---

## Evaluating Expressions

[%inc expr.py mark=do_abs %]

-   All the `do_` functions can be called interchangeably
-   Like the unit test functions of [%x test %]

---

## Dispatching Operations

-   Write a function that [%g dynamic_dispatch "dispatches" %] to actual operations

[%inc expr.py mark=do %]

---

## Dispatching Operations

[% figure
  slug="interp-recursive-evaluation"
  img="recursive_evaluation.svg"
  alt="Recursive evaluation of an expression tree"
  caption="Recursively evaluating an expression tree"
%]

---

## An Example

[%inc expr.tll %]
[%inc expr.sh %]
[%inc expr.out %]

---

## Environments

-   Store variables in a dictionary that's passed to every `do_` function
    -   Like the dictionary returned by the `globals` function
    -   An [%g environment "environment" %]

[%inc vars.py mark=do_abs %]

---

## Getting Variables' Values

-   Choices for getting variables' values:
    1.  Assume strings are variable names
    2.  Define another function that we call explicitly

[%inc vars.py mark=do_get %]

[%inc vars.py mark=do_set %]

---

## Sequencing

-   Need a way to set values before evaluating expressions
-   `["seq", ["set", "a", 1], ["add", ["get", "a"], 2]]`

[%inc vars.py mark=do_seq %]

---

<!--# class="aside" -->

## Everything Is An Expression

-   Python distinguishes [%g expression "expressions" %] that produce values
    from [%g statement "statements" %] that don't
-   But it doesn't have to, and many languages don't

```python
# not actually legal Python
result =
    if a > 0:
        1
    elif a == 0:
        0
    else:
        -1
```

---

## Doubling

[%inc doubling.tll %]

---

## Doubling

[%inc doubling.out %]

---

## This Is Tedious

[%inc vars.py mark=do %]

-   But we know what to do

---

## Introspection

[%inc vars_reflect.py mark=lookup %]

---

<!--# class="aside" -->

## How Good Is Our Design?

-   One way to evaluate a design is to ask how [%g extensibility "extensible" %] it is
-   The answer for the interpreter is "pretty easily"
-   The answer for our little language is "not at all"
-   We need a way to define and call functions of our own
-   We will tackle this in [%x func %]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="interp-concept-map"
   img="concept_map.svg"
   alt="Concept map"
   caption="Concept map of interpreter"
%]
