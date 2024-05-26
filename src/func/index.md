---
title: "Functions and Closures"
abstract: >
    This chapter extends the little interpreter of the previous one
    to allow users to define functions of their own.
    By doing so,
    it shows that the way programs handle variable scope is a design choice,
    and that the use of a particular technique called closures
    enables programs written in Python (and other modern programming languages)
    to encapsulate information in useful ways.
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
-   When a function looks up variables
    it checks its own stack frame and the global frame.
-   A closure stores the variables referenced in a particular scope.
depends:
-   interp
---

One way to evaluate the design of a piece of software is
to ask how [%g extensibility "extensible" %] it is,
i.e.,
how easily we can add or change things [%b Wilson2022b %].
The answer for the [%i "interpreter" %] of [%x interp %] is "pretty easily"
but the answer for the little language it interprets is "not at all",
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

[%inc example_def.py mark=python %]

It has a name,
a (possibly empty) list of parameters,
and a body,
which in this case is a single [%i "statement" %].
{: .continue}

Our little language does things differently.
Since a function is just another kind of object,
we can define it on its own without naming it:

[%inc example_def.py mark=def %]

<div class="pagebreak"></div>

To save the function for later use,
we simply assign it to a name
as we would assign any other value:
{: .continue}

[%inc example_def.py mark=save %]

<div class="callout" markdown="1">

### Anonymity

A function without a name is called an [%g anonymous_function "anonymous" %] function.
JavaScript makes heavy use of anonymous functions;
Python supports a very limited version of them
using [%g lambda_expression "lambda expressions" %]:

[%inc example_def.py mark=lambda %]

</div>

## Calling Functions {: #func-call}

In Python,
we would call this function as `same(3)`.
Our little language requires us to specify an operator explicitly,
so we write the call as:

[%inc example_def.py mark=call %]

To make `"call"` work the way most programmers expect,
we need to implement [%i "scope" %]
so that the parameters and variables used in a function
aren't confused with those defined outside it.
In other words,
we need to prevent [%g name_collision "name collision" %].
When a function is called with one or more expressions as [%i "argument" "arguments" %],
we will:

1.  Evaluate all of these expressions.

2.  Look up the function.

3.  Create a new [%i "environment" %] from the function's parameter names
    and the expressions' values.

4.  Call `do` to run the function's action and capture the result.

5.  Discard the environment created in Step 3.

6.  Return the function's result.

<div class="callout" markdown="1">

### Eager and Lazy

Evaluating a function's arguments before we run it
is called [%g eager_evaluation "eager evaluation" %].
We could instead use [%g lazy_evaluation "lazy evaluation" %],
in which case we would pass the argument sub-lists into the function
and let it evaluate them when it needed their values.
Python and most other languages are eager,
but a handful of languages, such as R, are lazy.
It's a bit more work,
but it allows the function to inspect the expressions it has been called with
and to decide how to handle them.

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
is called [%g dynamic_scoping "dynamic scoping" %].
In contrast,
most programming languages used [%g lexical_scoping "lexical scoping" %],
which figures out what a variable name refers to
based on the structure of the program text.
The former is easier to implement (which is why we've chosen it);
the latter is easier to understand,
particularly in large programs.
[%b Nystrom2021 %] has an excellent step-by-step explanation
of how to build lexical scoping.

</div>

The completed implementation of function definition is:

[%inc func.py mark=func %]

and the completed implementation of function call is:
{: .continue}

[%inc func.py mark=call %]

and our test program and its output are:

[%inc func.tll %]
[%inc func.out %]

<div class="callout" markdown="1">

### Unpacking One Line

`do_call` contains the line:

[%inc ex_dict_zip.py %]

Working from the inside out,
it uses the built-in function `zip`
to create a list of pairs of corresponding items
from `params` and `values`,
then passes that list of pairs to `dict` to create a dictionary,
which it then appends to the list `env`.
The exercises will explore whether rewriting this
would make it easier to read.
{: .continue}

</div>

Once again,
Python and other languages do more or less what we've done here.
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

[%inc inner.py %]
[%inc inner.out %]

But since functions are just another kind of data,
the outer function can return the inner function it defined as its result:

<div class="pagebreak"></div>

[%inc closure.py %]
[%inc closure.out %]

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
   caption="Closures."
   cls="here"
%]

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

[%inc oop.py %]
[%inc oop.out %]

When this code runs,
Python creates a closure that is shared by the two functions ([%f func-objects %]).
The closure has a key `"private"`;
there is nothing special about this name,
but nothing in the program can see the data in the closure
except the two functions.
We could add more keys to this dictionary to create more complex objects
and build an entire system of objects and classes this way.
{: .continue}

[% figure
   slug="func-objects"
   img="objects.svg"
   alt="Objects as closures"
   caption="Implementing objects using closures."
%]

## Summary {: #func-summary}

[%f func-concept-map %] summarizes the ideas in this chapter,
which is one of the most technically challenging in this book.
In particular,
don't be surprised if it takes several passes to understand closures:
they are as subtle as they are useful.

[% figure
   slug="func-concept-map"
   img="concept_map.svg"
   alt="Concept map of functions and closures"
   caption="Concept map."
   cls="here"
%]

## Exercises {: #func-exercises}

### Rewriting Environment Creation {: .exercise}

Re-read the description of how this line in `do_call` works:

[%inc ex_dict_zip.py %]

and then rewrite the line using a loop to insert
parameter names and values into a dictionary.
Do you find your rewritten code easier to read?
{: .continue}

### Chained Maps {: .exercise}

Look at the documentation for the [`ChainMap`][py_chainmap] class
and modify the interpreter to use that to manage environments.

### Defining Named Functions {: .exercise}

Modify `do_func` so that if it is given three arguments instead of two,
it uses the first one as the function's name
without requiring a separate `"set"` instruction.

### Evaluating Parameters {: .exercise}

`do_func` stores the new function's parameters and body
without evaluating them.
What would happen if it did evaluate them immediately?

### Implicit Sequence {: .exercise}

1.  Modify `do_func` so that if it is given more than one argument,
    it uses all but the first as the body of the function
    (i.e., treats everything after the parameter list as an implicit `"seq"`).

2.  Is there a way to make this work in combination with
    naming-at-creation from the previous exercise?

### Preventing Redefinition {: .exercise}

1.  Modify the interpreter so that programs cannot redefine functions,
    i.e.,
    so that once a function has been assigned to a variable,
    that variable's value cannot be changed.

2.  Why might this be a good idea?
    What does it make more difficult?

### Generalizing Closure-Based Objects {: .exercise}

Modify the `getter`/`setter` example so that:

1.  `make_object` accepts any number of named parameters
    and copies them into the `private` dictionary.

2.  `getter` takes a name as an argument
    and returns the corresponding value from the dictionary.

3.  `setter` takes a name and a new value as arguments
    and updates the dictionary.

What does your implementation of `getter` do
if the name isn't already in the `private` dictionary?
What does your `setter` do
if the name isn't already there?
What does it do if the update value has a different type than the current value?

### What Can Change? {: .exercise}

Explain why this program doesn't work:

[%inc counter_fail.py %]

Explain why this one does:
{: .continue}

[%inc counter_succeed.py %]

### How Private Are Closures? {: .exercise}

If the data in a closure is private,
explain why lines 1 and 2 are the same in the output of this program
but lines 3 and 4 are different.

[% inc closure_list.py %]
[% inc closure_list.out %]
