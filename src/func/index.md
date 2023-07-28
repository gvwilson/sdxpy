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
status: "awaiting revision"
depends:
-   interp
---

One way to evaluate the design of a piece of software is
to ask how [%g extensibility "extensible" %] it is,
i.e.,
how easily we can add or change things [%b Wilson2022a %].
The answer for the [%i "interpreter" %] of [%x interp %] is, "Pretty easily,"
but the answer for the little language it interprets is, "Not at all,"
because there is currently no way for users to create new operations of their own.
We need to give users a way to define and call functions.
Doing this will take less than 60 lines of code,
and once we understand how definition works,
we will be able to understand
how some more advanced features of modern programming languages work as well.

## Definition and Storage {: #func-defstore}

Let's start by defining a function that takes a single [%i "parameter" %]
and immediately returns it.
In Python,
this is:

[% inc file="example_def.py" keep="python" %]

It has a name,
a (possibly empty) list of parameter names,
and a body,
which in this case is a single [%i "statement" %].
{: .continue}

Our little language does things differently.
Since a function is just another kind of object,
we can define it on its own without naming it:

[% inc file="example_def.py" keep="def" %]

To save the function for later use,
we simply assign it to a name
as we would assign any other value:

[% inc file="example_def.py" keep="save" %]

<div class="callout" markdown="1">

### Anonymity

A function without a name is called an [%g anonymous_function "anonymous" %].
JavaScript makes heavy use of anonymous functions;
Python supports a very limited version of them
using [%g lambda_expression "lambda expressions" %]:

[% inc file="example_def.py" keep="lambda" %]

</div>

## Calling Functions {: #func-call}

In Python,
we would call this function as `same(3)`.
Our little language requires us to specify an operator explicitly,
so we write the call as:

[% inc file="example_def.py" keep="call" %]

To make `"call"` work,
we need to implement [%i "scope" %]
so that parameters and variables used in a function
don't overwrite those defined outside it—in other words,
to prevent [%g name_collision "name collision" %].
When a function is called with one or more expressions as [%i "argument" "arguments" %],
we will:

1.  Evaluate all of these expressions.

2.  Look up the function.

3.  Create a new [%i "environment" %] whose keys are the parameters' names
    and whose values are the expressions' values.

4.  Call `do` to run the function's action and captures the result.

5.  Discard the environment created in step 3.

6.  Return the function's result.

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

To make this work,
the environment must be a list of dictionaries instead of a single dictionary.
This list is the [%g call_stack "call stack" %] of our program,
and each dictionary in it is usually called a [%g stack_frame "stack frame" %].
When a function wants the value associated with a name,
we look through the list from the most recent dictionary to the oldest.

<div class="callout" markdown="1">

### Scoping Rules

Searching through all active stack frames for a variable
is called is [%g dynamic_scoping "dynamic scoping" %].
In contrast,
most programming languages used [%g lexical_scoping "lexical scoping" %],
which figures out what a variable name refers to based on the structure of the program text.

</div>

The completed implementation of function definition is:

[% inc file="func.py" keep="func" %]

The completed implementation of function call is:
{: .continue}

[% inc file="func.py" keep="call" %]

Our test program and its output are:
{: .continue}

[% inc pat="func.*" fill="tll out" %]

Once again,
Python and other languages work exactly as shown here.
The interpreter
(or the CPU, if we're running code [%g compile "compiled" %] to machine instructions)
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

One common use of closures is
to turn a function that needs many arguments
into one that needs fewer.
For example,
Python's built-in `map` function
applies a user-defined function to each value in a list:

[% inc pat="map_double.*" fill="py out" %]

It's annoying to have to define a one-line function
each time we want to use this,
so we can instead use a function to define the function we want
and rely on closures to remember the extra parameters:

[% inc file="map_closure.py" keep="keep" %]
[% inc file="map_closure.out" %]

In practice,
most programmers would use `lambda` to wrap a function this way:

[% inc file="map_lambda.py" keep="keep" %]
[% inc file="map_lambda.out" %]

We can also use closures to implement objects with truly private data.
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

## Summary {: #func-summary}

[% figure
   slug="func-concept-map"
   img="concept_map.svg"
   alt="Concept map of functions and closures"
   caption="Concept map"
%]

## Exercises {: #func-exercises}

### Defining Named Functions {: .exercise}

Modify `do_func` so that if it is given three arguments instead of two,
it uses the first one as the function's name
without requiring a separate `"set"` instruction.

### Implicit Sequence {: .exercise}

1.  Modify `do_func` so that if it is given more than one argument,
    it uses all but the first as the body of the function
    (i.e., treats every after the parameter list as an implicit `"seq"`).

2.  Is there a way to make this work in combination with
    naming-at-creation from the previous exercise?

### Preventing Redefinition {: .exercise}

1.  Modify the interpreter so that programs cannot redefine functions,
    i.e.,
    so that once a function has been assigned to a variable,
    that variable's value cannot be changed.

2.  Why might this be a good idea?
    What does it make more difficult?

### How Private Are Closures? {: .exercise}

If the data in a closure is private,
explain why lines 1 and 2 are the same in the output of this program
but lines 3 and 4 are different.

[% inc pat="closure_list.*" fill="py out" %]
