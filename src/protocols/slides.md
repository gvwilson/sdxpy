---
template: slides
title: "Protocols"
---

## The Problem

-   Want to use some more advanced features of Python in coming examples

-   Can now explain them in terms of what we've seen in previous lessons

---

## Mock Objects

[%inc mock_time.py %]

-   But this changes `time.time` for *everything*

-   Want a reliable way to restore the original

---

## Callable

-   If a function is just an object

-   We can make an object that looks like a function

[%inc callable.py %]
[%inc callable.out %]

---

## A Generic Replacer

[%inc mock_object.py mark=fake %]

[%inc mock_object.py mark=fakeit %]

---

## Replacement in Action

[%inc mock_object.py mark=test_real %]

[%inc mock_object.py mark=test_fixed %]

-   Yes, we would usually do something more useful…

---

## Replacement in Action

[% figure
   slug="protocols-timeline"
   img="timeline.svg"
   alt="Timeline of mock operation"
   caption="Timeline of mock operation."
%]

---

## But Wait, There's More

-   Record arguments

[%inc mock_object.py mark=test_record %]

-   Return a user-defined value

[%inc mock_object.py mark=test_calc %]

---

## Protocols

-   A [%g protocol "protocol" %] specifies
    how programs can tell Python to do specific things at specific moments

    -   `__init__` to build objects

    -   `__call__` to emulate function call

-   Define `__enter__` and `__exit__` to create a [%g context_manager "context manager" %]
    that a `with` statement can use

---

## Operation

```python
with C(…args…) as name:
    …do things…
```

1.  Call `C`'s constructor to create an object.
2.  Call that object's `__enter__` method and assign the result to `name`.
3.  Run the code inside the `with` block.
4.  Call `name.__exit__()` when the block finishes.

-   `__enter__` doesn't need extra arguments

    -   Use the object's constructor

-   Python calls `__exit__` with three values for error handling

---

## Mock With Context

[%inc mock_context.py mark=contextfake %]

---

## Wrapping Functions

-   Try writing a function that wraps another function

[%inc wrap_infinite.py %]
[%inc wrap_infinite.out %]

-   Well, that didn't work

---

## Capture the Original

[%inc wrap_capture.py %]
[%inc wrap_capture.out %]

---

## Parameters

[%inc wrap_param.py %]
[%inc wrap_param.out %]

---

## Decorators

[%inc decorator_simple.py %]
[%inc decorator_simple.out %]

---

## Decorator Parameters

[%inc decorator_param.py %]
[%inc decorator_param.out %]

---

<!--# class="aside" -->

## Design Flaw

-   A decorator must take exactly one argument,
    so how do we pass other parameters to the decorator itself?

-   Simple-to-learn answer would have been to treat function being decorated
    like `self` in method definition and call

[%inc alternative_design.py %]

---

## Iteration

-   Python calls `thing.__iter__` at the start of a `for` loop
    to get an [%g iterator "iterator" %]

-   Calls `iterator.__next__` repeatedly to get loop items

-   Stops when the iterator raises `StopIteration`

-   (Almost) always create a separate object
    so that we can run nested loops on the same target

---

## Loop Over a List of Strings

[%inc better_iterator.py mark=buffer %]

[%inc better_iterator.py mark=cursor omit=advance %]

---

## Iterator in Action

[%inc test_better_iterator.py mark=example %]

---

<!--# class="summary" -->

## Summary

[% figure
   slug="protocols-concept-map"
   img="concept_map.svg"
   alt="Concept map of reflection"
   caption="Concept map"
%]
