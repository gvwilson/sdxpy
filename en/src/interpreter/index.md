---
title: "An Interpreter"
syllabus:
-   Compilers and interpreters are just programs.
-   Basic arithmetic operations are just functions that have special notation.
-   Programs can be represented as trees, which can be stored as nested lists.
-   Interpreters recurisvely dispatch operations to functions that implement low-level details.
-   Programs store variables in stacked dictionaries called environments.
-   One way to evaluate a program's design is to ask how extensible it is.
---

[%x tester %] introduced the idea that programs are just another kind of data.
Similarly,
the compilers and interpreters that make programs run are just programs themselves.
instead of changing the characters in a block of memory like text editors,
or calculating sums and averages like spreadsheets,
compilers turn text into instructions for interpreters or hardware to run.

Most real programming languages have two parts:
a [%g parser "parser" %] that translates the source code into a data structure in memory,
and a [%g runtime "runtime" %] that executes the instructions in that data structure.
This chapter focuses on the runtime;
[%x parser %] will explore parsing,
whle [%x vm %] will look at more efficient ways to execute instructions.

## Expressions {: #interpreter-expressions}

Let's start by building something that can evaluate simple expressions
like `1+2` or `abs(-3.5)`.
We represent each expression as a list
with the name of the operation as the first item
and the values to be operated on as the other items.
To add 1 and 2 we use:

```python
["add", 1, 2]
```

and to calculate the absolute value of -3.5 we use:
{: .continue}

```python
["abs", -3.5]
```

<div class="callout" markdown="1">

### Nothing Special

We have special symbols for addition, subtraction, and so on for historical reasons,
but our list representation doesn't distinguish between things like `+` and `abs`
because it doesn't need to.
If our program is being compiled into low-level instructions for a particular CPU,
it's the compiler's job to decide what can be done directly
and what needs multiple instructions.
For example,
early CPUs didn't have instructions to do division,
while modern CPUs may have instructions to do addition or multiplication
on multiple values at once.

</div>

We can represent more complicated expressions using nested lists.
For example, `abs(1+2)` is:

```python
["abs", ["add", 1, 2]]
```

The function to add two expressions looks like this:

[%inc file="expr.py" keep="do_add" %]

Its single parameter is a list containing
the two sub-expressions to be evaluated and added.
After checking that it has the right number of parameters,
it calls the function `do` [%g recursion "recursively" %] to evaluate those sub-expressions.
(We've called the function `do` instead of `eval`
because Python already has a function called `eval`.)
Once `do_add` has two actual values,
it adds them and returns the result
([%f interpreter-recursive-evaluation %])
{: .continue}

[% figure
   slug="interpreter-recursive-evaluation"
   img="interpreter-recursive-evaluation.svg"
   alt="Recursive evaluation of an expression tree."
   caption="Recursively evaluation an expression tree."
%]

<div class="callout" markdown="1">

### Arguments versus Parameters

Many programmers use the words [%g argument "argument" %]
and [%g parameter "parameter" %] interchangeably,
but to make our meaning clear,
we call the values passed into a function its arguments
and the names the function uses to refer to them as its parameters.
Put it another way,
parameters are part of the definition
and arguments are given when the function is called.

</div>

`do_abs`, which calculates absolute value,
works the same way.
The only differences are that it expects one value instead of two
and calculates a different return value:

[%inc file="expr.py" keep="do_abs" %]

So how does `do` work?
It starts by checking if its input is an integer.
If so,
it returns that value right away
because integers "evaluate" to themselves:
no more calculation is needed.
Otherwise,
`do` checks that its parameter is a list
and then uses the first value in the list
to decide what other function to call.
This process is often called [%g dispatch "dispatch" %].

[%inc file="expr.py" keep="do" %]

Finally,
the main body of the program reads
the file containing the instructions to execute,
calls `do`,
and prints the result:

[%inc file="expr.py" keep="main" %]

Our program is a list of lists (of lists…)
so we can read it as [%g "json" JSON %] using `json.load`.
If our program file contains:

[% inc file="expr.tll" %]

then our little interpreter prints:
{: .continue}

[% inc file="expr.out" %]

This is a lot of code to do something that Python already does,
but it shows what Python (and other languages) do themselves.
When we run our little interpreter with:

```bash
$ python expr.py expr.tll
```

Python reads `expr.py`,
turns it into a data structure with operation identifiers and constants,
then uses those operation identifiers to decide what functions to call.
Those functions are written in C
and have been compiled to machine instructions,
but the cycle of lookup, call, and recurse is exactly the same.

## Variables {: #interpreter-variables}

Adding up constants is a start,
but our programs will be easier to read with variables
that let us give names to values.
We can add them to our interpreter
by passing around a dictionary containing all the variables seen so far.
Such a dictionary is sometimes called an [%g environment "environment %]
because it is the setting in which expressions are evaluated;
the dictionaries returned by the `globals` and `locals` functions
introduced in [%x tester %] are both environments.

Let's modify `do_add` and `do_abs`
to take an environment as an extra parameter and pass it on to `do` as needed:

[% inc file="vars.py" keep="do_abs" %]

Looking up variables when we need their values is straightfoward.
We check that we have a variable name and that the name is in the environment,
then return the stored value:

[% inc file="vars.py" keep="do_get" %]

To define a new variable or change an existing one,
we evaluate an expression and store its value in the environment:

[% inc file="vars.py" keep="do_set" %]

We need to add one more function to make this all work.
Our programs no longer consist of a single expression;
instead,
we may have several expressions that set variables' values
and then use them in calculations.
To handle this,
we add a function `do_seq` that runs a sequence of expressions one by one.
This function is our first piece of [%g control_flow "control flow" %]:
rather than calculating a value itself,
it controls when and how other expressions are evaluated.
Its implementation is:

[% inc file="vars.py" keep="do_seq" %]

Let's try it out.
Our test program is:

[% inc pat="vars.*" fill="tll out" %]

## Introspection Again {: #interpreter-introspection}

Before we add more operations,
let's have a look at the current state of `do`:

[% inc file="vars.py" keep="do" %]

The sequence of `if` statements that decide what function to call
is going to become unreadably long.
Let's use [%g introspection "introspection" %] to create a lookup table instead
by finding and storing every function whose name starts with `do_`:

[% inc file="vars_reflect.py" keep="lookup" %]

Line by line:
{: .continue}

1.  We use a [%g dictionary_comprehension "dictionary comprehension" %]
    to create a dictionary in a single statement.

1.  We only add functions whose names start with `do_`.

1.  Each key-value pair in the dictionary is the name of an operation
    and the function that implements the operation.
    The operation's name is what comes after `do_` in the function's name.

With this lookup table in hand,
the code to select and run an operation is:

[% inc file="vars_reflect.py" keep="do" %]

As with unit test functions in [%x tester %],
the `do_*` functions must have exactly the same [%g signature "signature" %]
so that we can all any of them with an environment and a list of arguments
without knowing exactly which function we're calling.
And as with finding tests,
introspection is more reliable than a hand-written lookup table,
but it isn't necessarily easier to understand.
If we write out the lookup table explicitly like this:

[% inc file="vars_table.py" keep="lookup" %]

then it's easy to see exactly what operations are available
and what their names are.
If we use introspection,
we have to search through the source file (or possibly several files)
to find all the available operations.
{: .continue}

## Statements {: #interpreter-statements}

Now that we have recursive evaluation, function lookup, and environments,
it's easy to add more features to our little language.
Our goal is to execute this program,
which starts with the number 1 and doubles it four times:

[% inc file="doubling.tll" %]

The simplest of the new operations is `comment`,
which does nothing and returns `None`:

[% inc file="stmt.py" keep="comment" %]

An `if` statement is a bit more complex.
If its first argument is true it evaluates and returns its second argument
(the "if" branch).
Otherwise,
it evaluates and returns its second argument (the "else" branch):

[% inc file="stmt.py" keep="if" %]

This is called [%g lazy_evaluation "lazy evaluation" %]
to distinguish it from the more usual [%g eager_evaluation "eager evaluation" %]
that evaluates everything up front.
`do_if` only evaluates what it absolutely needs to;
most languages do this so that we can safely write things like:
{: .continue}

```python
if x != 0:
    return 1/x
else:
    return None
```

If the language always evaluated both branches
then the code shown above would fail whenever `x` was zero,
even though it's supposed to handle that case.
In this case it might seem obvious what the language should do,
but most languages use lazy evaluation for `and` and `or` as well
so that expressions like:
{: .continue}

```python
reference and reference.part
```

will produce `None` if `reference` is `None`
and `reference.part` if it isn't.
{: .continue}

## Functions {: #interpreter-functions}

One way to evaluate the design of a piece of software is
to ask how [%g extensibility "extensible" %] it is,
i.e.,
how easily we can add or change things [%b Wilson2022 %].
The answer for our interpreter is now, "Pretty easily,"
but for our little language is, "Not at all,"
because there's no way for users to create new operations of their own.
We need to give users a way to define and call functions.

Doing this takes less than 60 lines:

1.  A function definition looks like:

    ```python
    ["def", "same", ["num"], ["get", "num"]]
    ```

    It has a name, a (possibly empty) list of parameter names,
    and a single instruction as a body
    (which will usually be a `"seq"` instruction).

2.  Functions are stored in the environment like any other value.
    The value stored for the function defined above would be:

    ```python
    ["func", ["num"], ["get", "num"]]
    ```

    We don't need to store the name: that's recorded by the environment,
    just like it is for any other variable.

3.  A function call looks like:

    ```python
    ["call", "same", 3]
    ```

    The values passed to the functions are normally expressions rather than constants,
    and are *not* put in a sub-list.
    The implementation:
    1.  Evaluates all of these expressions.
    2.  Looks up the function.
    3.  Creates a new environment whose keys are the parameters' names
        and whose values are the expressions' values.
    4.  Calls `do` to run the function's action and captures the result.
    5.  Discards environment created two steps previously.
    6.  Returns the function's result.

4.  Instead of using a single dictionary to store an environment
    we use a list of dictionaries.
    The first dictionary is the global environment;
    the others store the variables belonging to active function calls.

5.  When we get or set a variable,
    we check the most recent environment first
    (i.e., the one that's last in the list);
    if the variable isn't there we look in the global environment.
    We don't look at the environments in between;
    the exercises explore why not.

Here's the implementation of `do_def`:

[% inc file="func.py" keep="def" %]

And here's the implementation of `do_call`:
{: .continue}

[% inc file="func.py" keep="def" %]

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

[% figure
   slug="interpreter-concept-map"
   img="interpreter-concept-map.svg"
   alt="Concept map of interpreter."
   caption="Interpreter concept map."
%]

## Exercises {: #interpreter-exercises}

### Arrays {: .exercise}

Implement fixed-size one-dimensional arrays:
`["array", "new", 10]` creates an array of 10 elements,
while other instructions get and set particular array elements by index.

### While loops {: .exercise}

1.  Add a `while` loop using a Python `while` loop.

1.  Add a `while` loop using recursion.

### Loop counters {: .exercise}

The `"repeat"` instruction runs some other instruction(s) several times,
but there is no way to access the loop counter inside those instructions.
Modify `"repeat"` so that programs can do this.
(Hint: allow people to create a new variable to hold the loop counter's current value.)

### Chained maps {: .exercise}

Look at the documentation for the [`ChainMap`][py_chainmap] class
and modify the interpreter to use that to manage environments.

### Better error handling {: .exercise}

Several of the instruction functions started with `assert` statements,
which means that users get a stack trace of TLL itself
when there's a bug in their program.

1.  Define a new exception class called `TLLException`.

2.  Write a utility function called `check`
    that raises a `TLLException` with a useful error message
    when there's a problem.

3.  Add a `catch` statement to handle these errors.

### Tracing {: .exercise}

Add a `--trace` command-line flag to the interpreter.
When enabled, it makes TLL print a messages showing each function call and its result.

### Early return {: .exercise}

Add a `"return"` instruction to TLL that ends a function call immediately
and returns a single value.

### Variable argument lists {: .exercise}

Add variable-length parameter lists to functions.

### Scoping {: .exercise}

1.  Our interpreter looks for variables in
    the current function call's environment
    and in the global environment,
    but not in the environments in between.
    Why not?
    How could looking in those intermediate environments
    make programs harder to debug?

1.  The interpreter allows users to define functions inside functions.
    What variables can the inner function access when you do this?
    What variables *should* it be able to access?
    What would you have to do to enable this?
