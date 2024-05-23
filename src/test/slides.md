---
template: slides
title: "Running Tests"
---

## The Problem

-   Not all software needs formal testing
    -   Check one-off data analysis script incrementally
-   But 98% of the code in [SQLite][sqlite] is there to test the other 2%
    -   For which I am grateful
-   Good tools make tests easier to write
    -   So that programmers have fewer excuses not to write them
-   This lesson build a unit testing framework like [pytest][pytest]
    -   Most frameworks in most other languages share its design

---

## Functions in Lists

-   We can put functions in lists

[%inc func_list.py %]
[%inc func_list.out %]

---

## Signatures

-   We have to know how to call the functions
    -   They must have the same [%g signature "signature" %]

[%inc signature.py %]
[%inc signature.out %]

---

<!--# class="aside" -->

## Checking

-   Use `type` to see if something is a function

[%inc type_int.py %]
[%inc type_int.out %]

[%inc type_func.py %]
[%inc type_func.out %]

---

<!--# class="aside" -->

## Checking

-   But built-in functions have a different type

[%inc type_len.py %]
[%inc type_len.out %]

-   So use `callable` to check if something can be called

[%inc callable.py %]
[%inc callable.out %]

---

## Testing Terminology

-   Apply the function we want to test to a [%g fixture "fixture" %]
-   Compare the [%g actual_result "actual result" %]
    to the [%g expected_result "expected result" %]
-   Possible outcomes are:
    -   [%g pass_test "pass" %]: the target function worked
    -   [%g fail_test "fail" %]: the target function didn't do what we expected
    -   [%g error_test "error" %]: something went wrong with the test itself
-   Typically use `assert` to check results
    -   If condition is `True`, does nothing
    -   Otherwise, raises an `AssertionError`
-   Failed assertions usually cause the program to halt
    -   But we can catch the exception ourselves if we want

---

## A Function and Some Tests

[%inc manual.py mark=sign %]
[%inc manual.py mark=tests %]

---

## What We Want

[%inc manual.py mark=use %]
[%inc manual.out %]

-   But we have to remember to add each one to `TESTS`

---

## How Python Stores Variables

-   Python stores variables in (something very much like) a dictionary

[%inc globals.py %]
[%inc globals.out %]

---

## Further Proof

[%inc globals_plus.py %]
[%inc globals_plus.out %]

-   The function `locals` gives local variables

---

## Introspection

-   We know how to loop over a dictionary's keys

[%inc find_test_funcs.py mark=main %]
[%inc find_test_funcs.out %]

-   When we print a function, Python shows its name and address

---

## A Better Test Runner

[%inc runner.py mark=run %]

-   Really should check that tests are callable

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="test-concept-map"
   img="concept_map.svg"
   alt="Concept map of unit testing framework"
   caption="Concept map"
%]
