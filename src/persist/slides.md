---
template: slides
title: "Object Persistence"
---

## How to Save Data?

-   Prose as plain text
-   Tables as CSV
-   What about objects?
    -   List of dictionaries of lists of dictionaries

---

## Existing Options

-   [JSON][py_json] or [YAML][py_yaml]: language-neutral
    -   But therefore lowest common denominator
    -   Boolean, number, string, list, dictionary (with string keys)
-   [pickle][py_pickle] module: Python-specific
    -   Arbitrary nested objects (good)
    -   Other languages can't read its files (bad)

---

## Getting Started

-   Store each __atomic value__ on a line of its own
    -   `type_name:value`

[%inc format.txt %]

-   Split strings on newlines
    -   Save the number of lines

[%inc multiline_input.txt %]
[%inc multiline_output.txt %]

---

## Implementation

[%inc builtin.py mark=save omit=extras %]

---

## Collections

-   Save type and number of elements

[%inc builtin.py mark=save_list %]

---

## What This Looks Like

[%inc save_builtin.py mark=save %]
[%inc save_builtin.out %]

-   Computer doesn't need indentation or end markers
-   But we might add them for readability

---

## Reading Data

[%inc builtin.py mark=load omit=extras %]

---

## Reading Multi-line Values

[%inc builtin.py mark=load_list %]

-   Use a list comprehension instead of a loop

---

## Open-Closed Principle

-   Software should be open for extension but closed for modification
    -   I.e., should be able to add new code without rewriting existing code
-   Create a dispatch function that figures out what reader or writer to call
-   Find appropriate things to call dynamically
-   Instead of looking for functions, look for methods
-   If the type of the thing we're saving is `something`,
    provide a method `_something`

---

## Saving

[%inc objects.py mark=save %]

-   Handle loading the same way

---

## Next Steps

-   What to do with user-defined classes?
    -   Or things from the standard library, for that matter?
-   Convert user types to built-in types
    -   Either the object tells us how…
    -   …or we do it generically
    -   Either way, how to convert back?
-   Save class definitions as well as objects' values
    -   Most general (code is just data)
    -   But most difficult to implement
    -   And a potential security hole

---

## Aliasing

[% figure
   slug="persist-shared"
   img="shared.svg"
   alt="A shared data structure"
   caption="A shared data structure"
%]

[%inc shared.py %]

-   "Surely nobody would ever do this!"
-   But every child node in an HTML tree has a reference to its parent

---

## Aliasing

-   Store a unique ID for every object using Python's `id`

-   Keep track of the objects seen so far

-   Write that ID the first time we see the object

-   Write a special entry when we see the object again

---

## Saving

[%inc aliasing.py mark=save %]

---

## What It Looks Like

[%inc save_aliasing.py mark=save %]
[%inc save_aliasing.out %]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="persist-concept-map"
   img="concept_map.svg"
   alt="Concept map of persistence"
   caption="Concept map."
%]
