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
status: "revised 2023-07-27"
depends:
---

We are going to create a lot of [%i "object" "objects" %] and [%i "class" "classes" %] in these lessons,
and they will be a lot easier to use if we understand how they are implemented.
Historically,
[%g oop "object-oriented programming" %] was invented to solve two problems:

1.  What is a natural way to represent real-world "things" in code?

2.  How can we organize code to make it easier to understand, test, and extend?

## Objects {: #oop-objects}

As a motivating problem,
let's define some of the things a generic shape in a drawing package must be able to do:

[% inc file="shapes_original.py" keep="shape" %]

A specification like this is sometimes called
a [%g design_by_contract "contract" %]
because an object must satisfy it in order to be considered a shape,
i.e.,
must provide methods with these names that do what those names suggest.
For example,
we can [%g derived_class "derive" %] classes from `Shape`
to represent squares and circles
{: .continue}

[% inc file="shapes_original.py" keep="concrete" %]

Since squares and circles have the same methods,
we can use them interchangeably.
This is called [%g polymorphism "polymorphism" %],
and it reduces [%i "cognitive load" %]
by allowing the people using related things to ignore their differences:

[% inc file="shapes_original.py" keep="poly" %]
[% inc file="shapes_original.out" %]

But how does polymorphism work?

The first thing we need to understand is that a function is an [%i "object" %].
While the bytes in a string represent characters
and the bytes in an image represent pixels,
the bytes in a function are instructions
([%f oop-func-obj %]).
When Python executes the code below,
it creates an object in memory
that contains the instructions to print a string
and assigns that object to the variable `example`:

[% inc file="func_obj.py" keep="def" %]

[% figure
   slug="oop-func-obj"
   img="func_obj.svg"
   alt="Bytes as characters, pixels, or instructions"
   caption="Bytes can be interpreted as text, images, instructions, and more."
%]

We can create an [%g alias "alias" %] for the function
by assigning it to another variable,
and then call the function by referencing that second variable.
Doing this doesn't alter or erase
the connection between the function and the original name:
{: .continue}

[% inc file="func_obj.py" keep="alias" %]
[% inc file="func_obj.out" %]

We can also store function objects in data structures like
lists and [%i "dictionary" "dictionaries" %].
Let's write some functions that do
the same things as the [%i "method" "methods" %] in our original Python
and store them in a dictionary to represent a square ([%f oop-shapes-dict %]):

[% inc file="shapes_dict.py" keep="square" %]

[% figure
   slug="oop-shapes-dict"
   img="shapes_dict.svg"
   alt="Storing shapes as dictionaries"
   caption="Using dictionaries to emulate objects."
%]

If we want to use one of the "methods" in this dictionary,
we call it like this:

[% inc file="shapes_dict.py" keep="call" %]

The function `call` looks up the function stored in the dictionary,
then calls that function with the dictionary as its first object;
in other words,
instead of using `obj.meth(arg)` we use `obj["meth"](obj, arg)`.
Behind the scenes,
this is (almost) how objects actually work.
We can think of an object as a special kind of dictionary.
A method is just a function that takes an object of the right kind
as its first [%i "parameter" %]
(typically called `self` in Python).
{: .continue}

## Classes {: #oop-classes}

One problem with implementing objects as dictionaries is that
it allows every single object to behave slightly differently.
In practice,
we want objects to store different values
(e.g., different squares to have different sizes)
but the same behaviors
(e.g., all squares should have the same methods).
We can implement this by storing the methods in a dictionary called `Square`
that corresponds to a class,
and have each individual square contain a reference to that higher-level dictionary
([%f oop-shapes-class %]).
In the code below,
that special reference uses the key `"_class"`:

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
and ask whether two objects are of the same class or not
by checking what their `"_class"` keys refer to.
{: .continue}

<div class="callout" markdown="1">

### Arguments vs. Parameters

Many programmers use the words [%g argument "argument" %]
and [%g parameter "parameter" %] interchangeably,
but to make our meaning clear,
we call the values passed into a function its arguments
and the names the function uses to refer to them as its parameters.
Put it another way,
parameters are part of the definition
and arguments are given when the function is called.

</div>

## Arguments {: #oop-args}

The methods we have defined so far operate on
the values stored in the object's dictionary,
but none of them take any extra arguments as input.
Implementing this is a little bit tricky
because different methods might need different numbers of arguments.
We could define functions `call_0`, `call_1`, `call_2` and so on
to handle each case,
but like most modern languages,
Python gives us a better way.
If we define a parameter in a function with a leading `*`,
it captures any "extra" values passed to the function
that don't line up with named parameters.
Similarly,
if we define a parameter with two leading stars `**`,
it captures any extra named parameters:

[% inc pat="varargs.*" fill="py out" %]

This mechanism is sometimes referred to as [%g varargs "varargs" %]
(short for "variable arguments").
A complementary mechanism called [%g spread "spreading" %]
allows us to take a list or dictionary full of arguments
and spread them out in a call to match a function's parameters:

[% inc pat="spread.*" fill="py out" %]

With these tools in hand,
let's add a method to our `Square` class
to tell us whether a square is larger than a user-specified size:

[% inc file="larger.py" keep="square" %]

The function that implements this check for circles
looks exactly the same:
{: .continue}

[% inc file="larger.py" keep="circle" %]

We then modify `call` to capture extra arguments in `*args`
and spread them into the function being called:
{: .continue}

[% inc file="larger.py" keep="call" %]

Our tests show that this works:

[% inc file="larger.py" keep="example" %]
[% inc file="larger.out" %]

However,
we now have two functions that do exactly the same thing—the
only difference between them is their names.
Anything in a program that is duplicated in several places
will eventually be wrong in at least one,
so we need to find some way to share this code.
{: .continue}

## Inheritance {: #oop-inheritance}

The tool we want is [%i "inheritance" %].
To see how this works in Python,
let's add a method called `density` to our original `Shape` class
that uses other methods defined by the class

[% inc file="inherit_original.py" keep="shape" %]
[% inc file="inherit_original.py" keep="use" %]
[% inc file="inherit_original.out" %]

To enable our dictionary-based "classes" to do the same thing,
we create a dictionary to represent a generic shape
and give it a "method" to calculate density:

[% inc file="inherit_class.py" keep="shape" %]

We then add another specially-named field to
the dictionaries for "classes" like `Square`
to keep track of their parents:

[% inc file="inherit_class.py" keep="square" %]

and modify the `call` function to search for
the requested method ([%f oop-inherit-class %]):
{: .continue}

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

In order to make an object,
we call the function associated with its `_new` key:
{: .continue}

[% inc file="inherit_constructor.py" keep="make" %]

That function is responsible for [%g upcall "upcalling" %]
the constructor of its parent.
For example,
the constructor for a square calls the constructor for a generic shape
and adds square-specific values using `|` to combine two dictionaries:
{: .continue}

[% inc file="inherit_constructor.py" keep="square" %]

Of course,
we're not done until we test it:

[% inc file="inherit_constructor.py" keep="call" %]
[% inc file="inherit_constructor.out" %]

## Summary {: #oop-summary}

We have only scratched the surface of Python's object system.
[%g multiple_inheritance "Multiple inheritance" %],
[%g class_method "class methods" %],
[%g static_method "static methods" %],
and [%g monkey_patching "monkey patching" %]
are powerful tools,
but they can all be understood in terms of dictionaries
that contain references to properties, functions, and other dictionaries.

[% figure
   slug="oop-concept-map"
   img="concept_map.svg"
   alt="Concept map for objects and classes"
   caption="Concept map for implementing objects and classes."
   cls="here"
%]

## Exercises {: #oop-exercises}

### Handling Named Arguments {: .exercise}

The final version of `call` declares a parameter called `*args`
to capture all the positional parameters of the method being called
and then spreads them in the actual call.
Modify it to capture and spread named parameters as well.

### Multiple Inheritance {: .exercise}

Implement multiple inheritance using dictionaries.
Does your implementation look methods up in the same order as Python would?

### Class Methods and Static Methods {: .exercise}

1.  Explain the differences between class methods and static methods.

2.  Implement both using dictionaries.

### Reporting Type {: .exercise}

Python `type` method reports the most specific type of an object,
while `isinstance` determines whether an object inherits from a type
either directly or indirectly.
Add your own versions of both to dictionary-based objects and classes.

### Using Recursion {: .exercise}

A [%g recursion "recursive function" %]
is one that calls itself,
either directly or indirectly.
Modify the `find` function that finds a method to call
so that it uses recursion instead of a loop.
Which version is easier to understand?
Which version is more efficient?

### Method Caching {: .exercise}

Our implementation searches for the implementation of a method
every time that method is called.
An alternative is to add a [%g cache "cache" %] to each object
to save the methods that have been looked up before.
For example,
each object could have a special key called `_cache` whose value is a dictionary.
The keys in that dictionary are the names of methods that have been called in the past,
and the values are the functions that were found to implement those methods.
Add this feature to our dictionary-based objects.
How much more complex does it make the code?
How much extra storage space does it need compared to repeated lookup?
