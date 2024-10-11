---
template: slides
title: "Functions and Closures"
---

## Background

-   The little programming language of [%x interp %] isn't extensible

-   So add a way to define and call functions

-   And then look at design tactics this opens up

---

## Definition

-   In Python

[%inc example_def.py mark=python %]

-   In our little language

[%inc example_def.py mark=def %]

-   Keyword `"func"`
-   (Possibly empty) list of parameter names
-   Body

---

## Saving Functions

-   A function is just another object

-   Assign it to a variable so we can call it later

[%inc example_def.py mark=save %]

---

<!--# class="aside" -->

## Anonymous Functions

-   An [%g anonymous_function "anonymous function" %]
    is one that doesn't have a name

-   JavaScript and other languages use them frequently

-   Python supports limited [%g lambda_expression "lambda expressions" %]

[%inc example_def.py mark=lambda %]

---

## Implementing Call

[%inc example_def.py mark=call %]

1.  Evaluate arguments.

2.  Look up the function.

3.  Create a new environment.

4.  Call `do` to run the function's action and captures the result.

5.  Discard environment created in step 3.

6.  Return the result.

---

<!--# class="aside" -->

## Eager and Lazy

-   [%g eager_evaluation "Eager evaluation" %]:
    arguments are evaluated *before* call

-   [%g lazy_evaluation "Lazy evaluation" %]:
    pass expression sub-lists into the function to be evaluated on demand

    -   Gives the called function a chance to inspect or modify expressions
        before using them

-   Python and most other languages (including ours) are eager

-   R is lazy

-   A design choice

---

## The Environment

-   A variable `x` in a function shouldn't clobber
    a variable with the same name in its caller

-   Use a list of dictionaries to implement a
    [%g call_stack "call stack" %]

-   Each dictionary called a [%g stack_frame "stack frame" %]

-   Look down the stack to find the name

-   If not found, add to the current (top-most) frame

---

## Implementing Definition

[%inc func.py mark=func %]

-   Should check that parameters are strings

---

## Implementing Call

[%inc func.py mark=call %]

---

## A Test

[%inc func.tll %]
[%inc func.out %]

---

## Dynamic Scoping

-   Searching active stack for a variable is called
    [%g dynamic_scoping "dynamic scoping" %]

-   Have to trace execution to figure out what a variable might refer to

[%inc dynamic.tll %]
[%inc dynamic.out %]

---

## Lexical Scoping

-   Almost all languages used [%g lexical_scoping "lexical scoping" %]

-   Decide what a name refers to based on the structure of the program

-   More efficient for the computer: doesn't have to search each time

-   More efficient for the person: limits scope of reasoning

-   More complicated to implement

-   But enables a very powerful programming technique

---

## Closures

[%inc closure.py %]
[%inc closure.out %]

-   The inner function [%g variable_capture "captures" %]
    the variables in the enclosing function

-   A way to make data private

---

## A More Useful Example

[%inc adder.py %]
[%inc adder.out %]

[% figure
   slug="func-closure"
   img="closure.svg"
   alt="Closures"
   caption="Closures"
%]

---

## Objects

[%inc oop.py %]
[%inc oop.out %]

---

## Objects

[% figure
   slug="func-objects"
   img="objects.svg"
   alt="Objects as closures"
   caption="Implementing objects using closures"
%]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="func-concept-map"
   img="concept_map.svg"
   alt="Concept map of functions and closures"
   caption="Concept map."
%]
