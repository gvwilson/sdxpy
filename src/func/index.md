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
depends:
-   interp
status: "revised 2023-07-31"
---

One way to evaluate the design of a piece of software is
to ask how [%g extensibility "extensible" %] it is,
i.e.,
how easily we can add or change things [%b Wilson2022a %].
The answer for the [%i "interpreter" %] of [%x interp %] is pretty easily"
but the answer for the little language it interprets is "not at all"
because users cannot define new operations in the little language itself.
We need to give them a way to define and call functions.
Doing this will take less than 60 lines of code,
and once we understand how definition works,
we will be able to understand
how an advanced feature of most modern programming languages works as well.

## Definition and Storage {: #func-defstore}

Let's start by defining a function that takes a single [%i "parameter" %]
and immediately returns it.
In Python,
this is:

[% inc file="example_def.py" keep="python" %]

It has a name,
a (possibly empty) list of parameters,
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
{: .continue}

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

To make `"call"` work the way most programmers expect,
we need to implement [%i "scope" %]
so that parameters and variables used in a function
aren't confused with defined outside it—in other words,
we need to prevent [%g name_collision "name collision" %].
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
The former is easier to implement (which is why we've chosen it);
the latter is easier to understand,
particularly in large programs.
[%b Nystrom2021 %] has an excellent step-by-step explanation
of how to build lexical scoping.

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
Python and other languages do more or less that we've done here.
When we define a function,
the interpreter saves the instructions in a lookup table.
When we call a function at runtime,
the interpreter finds the function in the table,
creates a new stack frame,
executes the instructions in the function,
and pops the frame off the stack.

## Closures {: #func-closures}

We normally define functions at the top level of our program,
but Python and most other modern languages
allow us to define functions within functions.
Those inner functions have access to
the variables defined in the enclosing function,
just as the functions we've seen in earlier examples
have access to things defined at the [%i "global" %] level of the program:

[% inc pat="inner.*" fill="py out" %]

But since functions are just another kind of data,
the outer function can return the inner function it defined as its result:

[% inc pat="closure.*" fill="py out" %]

The inner function still has access to the value of `thing`,
but nothing else in the program does.
A computer scientist would say that the inner function [%g variable_capture "captures" %]
the variables in the enclosing function
to create a [%g closure "closure" %]
([%f func-closure %]).
Doing this is a way to make data private:
once `make_hidden` returns `_inner` and we assign it to `has_secret` in the example above,
nothing else in our program has any way to access
the value that was passed to `make_hidden` as `thing`.

[% figure
   slug="func-closure"
   img="closure.svg"
   alt="Closures"
   caption="Closures"
%]

[% inc pat="adder.*" fill="py out" %]

One common use of closures is
to turn a function that needs many arguments
into one that needs fewer,
i.e.,
to create a function *now*
that remembers some values it's supposed to use *later*;
we will explore this in [%x protocols %].
Closures are also another way to implement objects.
Instead of building a dictionary ourselves as we did in [%x oop %],
we use the one that Python creates behind the scenes to implement a closure.
In the code below,
for example,
the function `make_object` creates a dictionary
containing two functions:

[% inc pat="oop.*" fill="py out" %]

These functions both refer to a dictionary called `private`,
which is another way of saying that
they both have reference to the dictionary Python created to represent the closure
that has a key `"private"` ([%f func-objects %]).
They share the data in this dictionary,
but nothing else in the program has access to it.
We could add more keys to this dictionary to create more complex objects,
and build an entire system of objects and classes this way.
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
   cls="here"
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

### What Can Change? {: .exercise}

Explain why this program doesn't work:

[% inc file="counter_fail.py" %]

Explain why this one does:
{: .continue}

[% inc file="counter_succeed.py" %]

### How Private Are Closures? {: .exercise}

If the data in a closure is private,
explain why lines 1 and 2 are the same in the output of this program
but lines 3 and 4 are different.

[% inc pat="closure_list.*" fill="py out" %]

### Generalizing Closure-Based Objects {: .exercise}

Modify the `getter`/`setter` example so that:

1.  `make_object` accepts any number of named parameters
    and copies them into the `private` dictionary.

2.  `getter` takes a name as a parameter
    and returns the corresponding value from the dictionary.

3.  `setter` takes a name and a new value as parameters
    and updates the dictionary.

What does your implementation of `getter` do
if the name isn't already in the `private` dictionary?
What does your `setter` do
if the name isn't already there?
What does it do if the update value has a different type than the current value?
