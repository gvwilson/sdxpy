---
syllabus:
-   When we define a function,
    our programming system saves instructions for later use.
-   Since functions are just data,
    we can separate creation from naming.
-   Most programming languages use eager evaluation,
    in which arguments are evaluated before a function is called.
-   Programming languages can also use lazy evaluation,
    in which expressions are passed to functions for just-in-time evaluation.
-   Every call to a function creates a new stack frame on the call stack.
-   When a function needs to look up variables,
    it looks in its own stack frame and the global frame.
-   A closure stores the variables referenced in a particular scope.
-   We can use decorators to wrap functions after defining them.
-   Defining a decorator that has parameters is much more complicated
    than defining one that doesn't.
---

One way to evaluate the design of a piece of software is
to ask how [%g extensibility "extensible" %] it is,
i.e.,
how easily we can add or change things [%b Wilson2022a %].
The answer for the interpreter of [%x interp %] is, "Pretty easily,"
but the answer for the little language it interprets is, "Not at all,"
because there is currently no way for users to create new operations of their own.
We need to give users a way to define and call functions.
Doing this will take less than 60 lines of code,
and once we understand how definition works,
we will be able to understand
how some more advanced features of modern programming languages work as well.

## Definition and Storage {: #func-defstore}

Let's start by defining a function that takes a single parameter
and immediately returns it.
In Python,
this is:

[% inc file="example_def.py" keep="python" %]

It has a name,
a (possibly empty) list of parameter names,
and a body,
which in this case is a single statement.
Its equivalent in our little language is:
{: .continue}

[% inc file="example_def.py" keep="def" %]

In Python,
we would call this function as `same(3)`.
Our little language requires us to specify an operator explicitly,
so we write the call as:

[% inc file="example_def.py" keep="call" %]

The arguments passed to the functions can be expressions rather than constants,
so we have to evaluate them when we make the call.
We have decided not to put them in a sub-list
in order to save ourselves one more layer of parentheses.

<div class="callout" markdown="1">

### Eager and Lazy

We said above that we have to evaluate a function's arguments when we call it,
which is called [%g eager_evaluation "eager evaluation" %].
We could instead use [%g lazy_evaluation "lazy evaluation" %],
in which case we would pass the argument sub-lists into the function
and let the function evaluate them when it needed their values.
Python and most other languages use the former strategy,
but a handful of languages, such as R, use the latter.
It's a bit more work,
but it allows the function to inspect the expressions it has been called with
and decide how to handle them.

</div>

Between defining and calling a function,
we must store it somewhere.
Since we are using lists for everything else,
we will use them for stored functions as well:

[% inc file="example_def.py" keep="store" %]

Notice that we don't store the function's name with it.
Instead,
we are going to store functions in the environment
in exactly the same way that we store other values.

<div class="callout" markdown="1">

### Anonymity

We could skip the special syntax for definition a function
and define them by creating the list that we're going to store (as shown above)
and then assigning it to a name in the environment:

[% inc file="example_def.py" keep="alt" %]

In this case,
the function itself is [%g anonymous_function "anonymous" %].
JavaScript makes heavy use of anonymous functions;
Python supports a very limited version of them
using [%g lambda_expression "lambda expressions" %]:
{: .continue}

[% inc file="example_def.py" keep="lambda" %]

</div>

## Calling Functions {: #func-call}

The last step in our implementation is to make sure that
local variables defined inside a function
don't overwrite variables defined outside the function.
In other words,
we need to implement [%g scope "scope" %].
When a function is called with one or more expressions as arguments,
we will:

1.  Evaluate all of these expressions.

2.  Look up the function.

3.  Create a new environment whose keys are the parameters' names
    and whose values are the expressions' values.

4.  Call `do` to run the function's action and captures the result.

5.  Discard the environment created in step 3.

6.  Return the function's result.

To make this work,
the environment must be a list of dictionaries instead of a single dictionary.
This list is the [%g call_stack "call stack" %] of our program,
and each dictionary in it is usually called a [%g stack_frame "stack frame" %].
When a function wants the value associated with a name,
we look through the list from the most recent dictionary to the oldest.

<div class="callout" markdown="1">

### Scoping Rules

Searching through all active stack frames for a variable
is called is [%i "dynamic scoping" "scoping!dynamic" %][%g dynamic_scoping "dynamic scoping" %][%/i%].
In contrast,
most programming languages used [%i "lexical scoping" "scoping!lexical" %][%g lexical_scoping "lexical scoping" %][%/i%],
which figures out what a variable name refers to based on the structure of the program text.

</div>

The completed implementation of function definition is:

[% inc file="func.py" keep="def" %]

The completed implementation of function call is:
{: .continue}

[% inc file="func.py" keep="call" %]

Our test program and its output are:
{: .continue}

[% inc pat="func.*" fill="tll out" %]

Once again,
Python and other languages work exactly as shown here.
The interpreter
(or the CPU, if we're running code compiled to machine instructions)
reads an instruction,
figures out what operation it corresponds to,
and executes that operation.

## Closures {: #func-closures}

We normally define functions at the top level of our program,
but Python and most other modern languages
allow us to define functions within functions.
And since functions are just another kind of data,
we can return that inner function:

[% inc pat="closure.*" fill="py out" %]

The inner function [%g variable_capture "captures" %]
the variables in the enclosing function
to create a [%g closure "closure" %].
Doing this is a way to make data private:
once `make_hidden` returns `_inner` and we assign it to `m` in the example above,
nothing else in our program can access
the value that was passed to `make_hidden` as `thing`.

Here's a more useful example of this technique:

[% inc pat="adder.*" fill="py out" %]

As [%f func-closure %] shows,
we have essentially created a way to build functions *now*
that remember the values they're supposed to add *later*.
{: .continue}

[% figure
   slug="func-closure"
   img="closure.svg"
   alt="Closures"
   caption="Closures"
%]

We can use closures to implement objects with truly private data.
In the code below,
for example,
the function `make_object` creates a dictionary
that exposes two functions:

[% inc pat="oop.*" fill="py out" %]

These functions both refer to a dictionary called `private`,
through which they can share data,
but nothing else in the program has access to that dictionary
([%f func-objects %]).
{: .continue}

[% figure
   slug="func-objects"
   img="objects.svg"
   alt="Objects as closures"
   caption="Implementing objects using closures"
%]

It's easy to become confused when working with closures.
For example,
suppose we want to create a function called `logging`
that prints a message before and after
each call to some other arbitrary function.
We could try to do it like this:

[% inc file="wrap_infinite.py" %]

but when we try to call `original` we wind up in an infinite loop.
The wrapped version of our function refers to `original`,
but Python looks that up at the time of call,
which means it calls the wrapped function instead.
We can solve this problem by creating a closure:

[% inc pat="wrap_capture.*" fill="py out" %]

Doing this also gives us a way to pass extra arguments
when we create the wrapped function:

[% inc pat="wrap_param.*" fill="py out" %]

Wrapping functions like this is so useful
that Python provides a special syntax for doing it
called a [%g decorator "decorator" %].
We define the function that does the wrapping as before,
but then use `@wrap` to apply it
rather than `name = wrap(name)`:

[% inc pat="decorator_simple.*" fill="py out" %]

If we want to pass parameters at the time we apply the decorator,
though,
it seems like we're stuck,
because a Python decorator must take exactly one argument,
which must be the function we want to decorate.
If we want to pass extra parameters,
we need to call a function that returns a function of one parameter
that we can then use as a decorator.
This means that we need to define a function inside a function *inside another function*
to create a closure that captures the parameters:

[% inc pat="decorator_param.*" fill="py out" %]

<div class="callout" markdown="1">

### Design Flaw

Decorators didn't need to be this complicated.
In order to define a method that takes \\( N \\) parameters in Python,
we have to write a function of \\( N+1 \\) parameters,
the first of which represents the object for which the method is being called.
Python could have done the same thing with decorators,
i.e.,
allowed people to define a function of \\( N+1 \\) parameters
and have `@` fill in the first automatically:

[% inc file="decorators_simple.py" %]

But this isn't the path Python took,
and as a result,
decorators are much harder to learn and use than they could have been.

</div>

## Summary	       

[% figure
   slug="func-concept-map"
   img="concept_map.svg"
   alt="Concept map of functions and closures"
   caption="Concept map"
%]
