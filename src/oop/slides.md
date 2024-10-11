---
template: slides
title: "Objects and Classes"
---

## The Problem(s)

-   What is a natural way to represent real-world "things" in code?

-   How can we organize code to make it easier to understand, test, and extend?

-   Are these the same thing?

---

## The Big Idea

<p class="shout">A program is just another data structure.</p>

[% figure
   slug="oop-func-obj"
   img="func_obj.svg"
   alt="Bytes as characters, pixels, or instructions"
   caption="Bytes can be interpreted as characters, pixels, or instructions."
%]

---

## Functions are Objects

-   `def` defines a variable whose value is the function's instructions

[%inc func_obj.py mark=def %]

-   We can assign that value to another variable

[%inc func_obj.py mark=alias %]
[%inc func_obj.out %]

---

## Representing Shapes

-   Start with the [%g design_by_contract contract %] for shapes

[%inc shapes_original.py mark=shape %]

---

## Provide Implementations

[%inc shapes_original.py mark=concrete %]

---

## Polymorphism

[%inc shapes_original.py mark=poly %]

-   OK, but how does it work?

---

## Let's Make a Square

[%inc shapes_dict.py mark=square %]

-   An object is just a (specialized) dictionary

-   A method is just a function that takes the object as its first parameter

---

## Let's Make a Square

[% figure
   slug="oop-shapes-dict"
   img="shapes_dict.svg"
   alt="Storing shapes as dictionaries"
   caption="Using dictionaries to emulate objects."
%]

---

## Calling Methods

[%inc shapes_dict.py mark=call %]

-   Look up the function in the object

-   Call it with the object as its first argument

-   `obj.meth(arg)` is `obj["meth"](obj, arg)`

---

## A Better Square

[%inc shapes_class.py mark=square %]

---

## Calling Methods

[%inc shapes_class.py mark=call %]

-   Look in the class for the method

-   Call it with the object as the first parameter

-   And we can now reliably identify objects' classes

---

## Calling Methods

[% figure
   slug="oop-shapes-class"
   img="shapes_class.svg"
   alt="Separating properties from methods"
   caption="Using dictionaries to emulate classes."
%]

---

<!--# class="aside" -->

## Variable Arguments

[%inc varargs.py %]
[%inc varargs.out %]

---

<!--# class="aside" -->

## Spreading

[%inc spread.py %]
[%inc spread.out %]

---

## Inheritance

-   Add a method to `Shape` that uses methods defined in derived classes

[%inc inherit_original.py mark=shape %]

---

## Inheritance

[% figure
   slug="oop-inherit-class"
   img="inherit_class.svg"
   alt="Implementing inheritance"
   caption="Using dictionary search to implement inheritance."
%]

---

## Yes, This Works

[%inc inherit_original.py mark=use %]
[%inc inherit_original.out %]

---

## Implementing Inheritance

[%inc inherit_class.py mark=shape %]

---

## Searching for Methods

[%inc inherit_class.py mark=search %]

---

## Yes, This Works Too

[%inc inherit_class.py mark=use %]
[%inc inherit_class.out %]

---

## Constructors

[%inc inherit_constructor.py mark=shape %]

---

## Parentage

[%inc inherit_constructor.py mark=square %]

---

## Use

[%inc inherit_constructor.py mark=call %]
[%inc inherit_constructor.out %]

---

<!--# class="summary" -->

## Summary	       

[% figure
   slug="oop-concept-map"
   img="concept_map.svg"
   alt="Concept map of objects and classes"
   caption="Concept map."
%]
