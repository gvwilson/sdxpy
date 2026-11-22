---
title: "Objects and Classes"
---

<section class="slide" markdown="1">

## The Problem(s)

-   What is a natural way to represent real-world "things" in code?

-   How can we organize code to make it easier to understand, test, and extend?

-   Are these the same thing?

</section>
<section class="slide" markdown="1">

## The Big Idea

<p class="shout">A program is just another data structure.</p>

[% figure
   slug="oop-func-obj"
   img="func_obj.svg"
   alt="Bytes as characters, pixels, or instructions"
   caption="Bytes can be interpreted as characters, pixels, or instructions."
%]

</section>
<section class="slide" markdown="1">

## Functions are Objects

-   `def` defines a variable whose value is the function's instructions

[%inc func_obj.py mark=def %]

-   We can assign that value to another variable

[%inc func_obj.py mark=alias %]
[%inc func_obj.out %]

</section>
<section class="slide" markdown="1">

## Representing Shapes

-   Start with the [%g design_by_contract contract %] for shapes

[%inc shapes_original.py mark=shape %]

</section>
<section class="slide" markdown="1">

## Provide Implementations

[%inc shapes_original.py mark=concrete %]

</section>
<section class="slide" markdown="1">

## Polymorphism

[%inc shapes_original.py mark=poly %]

-   OK, but how does it work?

</section>
<section class="slide" markdown="1">

## Let's Make a Square

[%inc shapes_dict.py mark=square %]

-   An object is just a (specialized) dictionary

-   A method is just a function that takes the object as its first parameter

</section>
<section class="slide" markdown="1">

## Let's Make a Square

[% figure
   slug="oop-shapes-dict"
   img="shapes_dict.svg"
   alt="Storing shapes as dictionaries"
   caption="Using dictionaries to emulate objects."
%]

</section>
<section class="slide" markdown="1">

## Calling Methods

[%inc shapes_dict.py mark=call %]

-   Look up the function in the object

-   Call it with the object as its first argument

-   `obj.meth(arg)` is `obj["meth"](obj, arg)`

</section>
<section class="slide" markdown="1">

## A Better Square

[%inc shapes_class.py mark=square %]

</section>
<section class="slide" markdown="1">

## Calling Methods

[%inc shapes_class.py mark=call %]

-   Look in the class for the method

-   Call it with the object as the first parameter

-   And we can now reliably identify objects' classes

</section>
<section class="slide" markdown="1">

## Calling Methods

[% figure
   slug="oop-shapes-class"
   img="shapes_class.svg"
   alt="Separating properties from methods"
   caption="Using dictionaries to emulate classes."
%]

</section>
<section class="slide" markdown="1">

## Variable Arguments

[%inc varargs.py %]
[%inc varargs.out %]

</section>
<section class="slide" markdown="1">

## Spreading

[%inc spread.py %]
[%inc spread.out %]

</section>
<section class="slide" markdown="1">

## Inheritance

-   Add a method to `Shape` that uses methods defined in derived classes

[%inc inherit_original.py mark=shape %]

</section>
<section class="slide" markdown="1">

## Inheritance

[% figure
   slug="oop-inherit-class"
   img="inherit_class.svg"
   alt="Implementing inheritance"
   caption="Using dictionary search to implement inheritance."
%]

</section>
<section class="slide" markdown="1">

## Yes, This Works

[%inc inherit_original.py mark=use %]
[%inc inherit_original.out %]

</section>
<section class="slide" markdown="1">

## Implementing Inheritance

[%inc inherit_class.py mark=shape %]

</section>
<section class="slide" markdown="1">

## Searching for Methods

[%inc inherit_class.py mark=search %]

</section>
<section class="slide" markdown="1">

## Yes, This Works Too

[%inc inherit_class.py mark=use %]
[%inc inherit_class.out %]

</section>
<section class="slide" markdown="1">

## Constructors

[%inc inherit_constructor.py mark=shape %]

</section>
<section class="slide" markdown="1">

## Parentage

[%inc inherit_constructor.py mark=square %]

</section>
<section class="slide" markdown="1">

## Use

[%inc inherit_constructor.py mark=call %]
[%inc inherit_constructor.out %]

</section>
<section class="slide" markdown="1">

## Summary	       

[% figure
   slug="oop-concept-map"
   img="concept_map.svg"
   alt="Concept map of objects and classes"
   caption="Concept map."
%]

</section>
