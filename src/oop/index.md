---
syllabus:
-   Objects are useful without classes, but classes make them easier to understand.
-   A well-designed class defines a contract that code using its instances can rely on.
-   Objects that respect the same contract are polymorphic, i.e.,
    they can be used interchangeably even if they do different specific things.
-   Objects and classes can be thought of as dictionaries with stereotyped behavior.
-   Most programming languages allow functions and methods to take a variable number of arguments.
-   Inheritance can be implemented in several ways
    that differ in the order in which objects and classes are searched for methods.
depends:
-   interp
---

We have created a lot of objects and classes in previous lessons.
Historically,
they were invented to solve two problems:

1.  What is a natural way to represent real-world "things" in code?

2.  How can we organize code to make it easier to understand, test, and extend?

## Objects {: #oop-objects}

Let's start by defining the things a generic two-dimensional shape must be able to do:

[% inc file="shapes_original.py" keep="shape" %]

A specification like this is sometimes called
a [%g design_by_contract "contract" %]
because any particular shape must conform to it:
{: .continue}

[% inc file="shapes_original.py" keep="concrete" %]

More importantly,
code that uses shapes can *rely* on the contract
and use different shapes interchangeably.

[% inc file="shapes_original.py" keep="poly" %]

This is called [%g polymorphism "polymorphism" %].
It reduces [%i "cognitive load" %][%/i%]
by allowing the people using a set of related things (in this case, objects)
to ignore their differences.

But how does it work?
To find out,
let's use a dictionary to represent a square
and write some functions that to
the same things as the methods in our earlier classes:

[% inc file="shapes_dict.py" keep="square" %]

Crucially,
the square's dictionary stores references to
the functions that know how to operate on squares ([%f oop-shapes-dict %]).

[% figure
   slug="oop-shapes-dict"
   img="shapes_dict.svg"
   alt="Storing shapes as dictionaries"
   caption="Using dictionaries to emulate objects."
%]

Behind the scenes,
this is (almost) how objects actually work.
We can think of an object as a special kind of dictionary.
A method is just a function that takes an object object of the right kind as its first parameter
(typically called `self` in Python).

Here's how we call methods:

[% inc file="shapes_dict.py" keep="call" %]

The function `call` looks up the function stored in the dictionary,
then calls that function with the dictionary as its first object.
In other words,
instead of using `obj.meth(arg)` we use `obj["meth"](obj, arg)`,
but the former is really just the latter in disguise.

## Classes {: #oop-classes}

One problem with implementing objects as dictionaries is that
it allows every single object to behave slightly differently.
In practice,
we want objects to have different properties
(e.g., different squares to have different sizes)
but the same behaviors
(e.g., all squares should have the same methods).
We can implement this by storing the methods in a dictionary called `Square`
that corresponds to a class,
and have each particular square contain a reference to that higher-level dictionary
([%f oop-shapes-class %]):

[% inc file="shapes_class.py" keep="square" %]

[% figure
   slug="oop-shapes-class"
   img="shapes_class.svg"
   alt="Separating properties from methods"
   caption="Using dictionaries to emulate classes."
%]

Calling a method now involves one more lookup
because we have go to from the object to the class to the method,
but once again we call the "method" with the object as the first argument:

[% inc file="shapes_class.py" keep="call" %]

As a bonus,
we can now reliably identify objects' classes
and ask whether two objects have the same class or not.
{: .continue}

<div class="callout" markdown="1">

### Variable Arguments

Like most modern programming languages,
Python allows us to define functions that take a variable number of arguments,
and to call functions by [%g spread "spreading" %] a list or dictionary:

[% inc pat="varargs.*" fill="py out" %]

</div>

## Inheritance {: #oop-inheritance}

The last step in building our own object system is to implement [%i "inheritance" %][%/i%].
First,
we add a method to our original `Shape` class that uses methods defined in derived classes:

[% inc file="inherit_original.py" keep="shape" %]

and check that it works:
{: .continue}

[% inc file="inherit_original.py" keep="use" %]
[% inc file="inherit_original.out" %]

To enable our dictionary-based "classes" to do the same thing,
we add a similar "method" to the dictionary representing a generic shape:

[% inc file="inherit_class.py" keep="shape" %]

and then modify the `call` function to look up the chain of inheritance
to find the requested method ([%f oop-inherit-class %]):

[% inc file="inherit_class.py" keep="search" %]

[% figure
   slug="oop-inherit-class"
   img="inherit_class.svg"
   alt="Implementing inheritance"
   caption="Using dictionary search to implement inheritance."
%]

A simple test shows that this is working as intended:

[% inc file="inherit_class.py" keep="use" %]
[% inc file="inherit_class.out" %]

We do have one task left, though:
we need to make sure that when a square or circle is made,
it is made correctly.
In short, we need to implement [%g constructor "constructors" %].
We do this by giving the dictionaries that implements classes
a special key `_new`
whose value is the function that builds something of that type:

[% inc file="inherit_constructor.py" keep="shape" %]

The constructor function for a square now calls
the constructor function for a generic shape
and then adds square-specific values by using `|` to combine two dictionaries:

[% inc file="inherit_constructor.py" keep="square" %]

Of course,
we're not done until we test it:

[% inc file="inherit_constructor.py" keep="call" %]
[% inc file="inherit_constructor.out" %]

## Summary {: #oop-summary}

We have only scratched the surface of what Python's object system provides.
[%g multiple_inheritance "Multiple inheritance" %],
[%g class_method "class methods" %],
[%i "static method" %]static methods[%/i%],
and [%g monkey_patching "monkey patching" %] are all useful,
but all can be understood in terms of dictionaries
that contain references to properties, functions, and other dictionaries.

[% figure
   slug="oop-concept-map"
   img="concept_map.svg"
   alt="Concept map for objects and classes"
   caption="Concept map for implementing objects and classes."
%]

## Exercises {: #oop-exercises}

### Multiple Inheritance {: .exercise}

Implement [%i "multiple inheritance" %][%/i%] using dictionaries.
Does your implementation look methods up in the same order as Python would?

### Class Methods and Static Methods {: .exercise}

Implement [%i "class method" %]class methods[%/i%]
and [%i "static method" %]static methods[%/i%]
and explain how they differ.
