---
syllabus:
-   Compilers and interpreters are just programs.
-   Basic arithmetic operations are just functions that have special notation.
-   Programs can be represented as trees, which can be stored as nested lists.
-   Interpreters recursively dispatch operations
    to functions that implement low-level details.
-   Programs store variables in stacked dictionaries called environments.
-   One way to evaluate a program's design is to ask how extensible it is.
---

[%x test %] introduced the idea that programs are just another kind of data.
Similarly,
the [%g compiler "compilers" %] and [%g interpreter "interpreters" %]
that make programs run are just programs themselves.
Instead of changing the characters in a block of memory like text editors,
or calculating sums and averages like spreadsheets,
compilers turn text into instructions for interpreters or hardware to run.

Most real programming languages have two parts:
a [%g parser "parser" %] that translates the source code into a data structure in memory,
and a [%g runtime "runtime" %] that executes the instructions in that data structure.
[%x parse %] explored parsing;
this chapter will build a runtime for a very simple interpreter,
while [%x vm %] will look at compiling code for more efficient execution.

<div class="callout" markdown="1">

### Two Ways to Run Code

A compiler translates a program into runnable instructions
before the program runs,
while an interpreter generates instructions on the fly
as the program is running.
In practice,
the difference between the two are blurry:
when Python runs a program,
for example,
it translates the source code into instructions as it loads files,
but saves those instructions in `.pyc` files to save time in future.

</div>

## Expressions {: #interp-expressions}

Let's start by building something that can evaluate simple expressions
like `1+2` or `abs(-3.5)`.
We represent each expression as a list
with the name of the operation as the first item
and the values to be operated on as the other items.
If we have multiple operations,
we use nested lists:

[% inc file="add_example.py" %]

<div class="callout" markdown="1">

### Notation

We use [%g infix_notation "infix notation" %] like `1+2` for historical reasons
in everyday life,
but our programs use [%g prefix_notation "prefix notation" %]—i.e.,
they always put the operations' names first—to make the operations easier to find.
Similarly,
we have special symbols for addition, subtraction, and so on for historical reasons,
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

The function to add two expressions looks like this:

[% inc file="expr.py" keep="do_add" %]

Its single parameter is a list containing
the two sub-expressions to be evaluated and added.
After checking that it has the right number of parameters,
it calls an as-yet-unwritten function `do`
to evaluate those sub-expressions.
(We've called the function `do` instead of `eval`
because Python already has a function called `eval`.)
Once `do_add` has two actual values,
it adds them and returns the result
([%f interp-recursive-evaluation %])
{: .continue}

[% figure
   slug="interp-recursive-evaluation"
   img="recursive_evaluation.svg"
   alt="Recursive evaluation of an expression tree"
   caption="Recursively evaluating the expression `abs(1+2)`."
%]

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

`do_abs`, which calculates absolute value,
works the same way.
The only differences are that it expects one value instead of two
and calculates a different return value:

[% inc file="expr.py" keep="do_abs" %]

Notice that `do_abs` and `do_add` have the same [%g signature "signature" %].
As with the unit testing functions in [%x test %],
this allows us to call them interchangeably.

So how does `do` work?
It starts by checking if its input is an integer.
If so,
it returns that value right away
because integers "evaluate" to themselves.
Otherwise,
`do` checks that its parameter is a list
and then uses the first value in the list
to decide what other function to call.
This lookup-and-call process is the same [%g dynamic_dispatch "dynamic dispatch" %]
that we saw in [%x parse %].

[% inc file="expr.py" keep="do" %]

Finally,
the main body of the program reads
the file containing the instructions to execute,
calls `do`,
and prints the result:

[% inc file="expr.py" keep="main" %]

Our program is a list of lists (of lists…)
so we can read it as [%g "json" JSON %] using `json.load`
rather than writing our own parser.
If our program file contains:

[% inc file="expr.tll" %]

then our little interpreter prints:
{: .continue}

[% inc file="expr.out" %]

This is a lot of code to do something that Python already does,
but it shows what Python (and other languages) do themselves.
Suppose we run our little interpreter with:

[% inc file="expr.sh" %]

Python reads `expr.py`,
turns it into a data structure with operation identifiers and constants,
then uses those operation identifiers to decide what functions to call.
Those functions are written in C
and have been compiled to machine instructions,
but the cycle of lookup and call is exactly the same.

## Variables {: #interp-variables}

Doing arithmetic on constants is a start,
but our programs will be easier to read with variables
that let us give names to values.
We can add them to our interpreter
by passing around a dictionary containing all the variables seen so far.
Such a dictionary is sometimes called an [%g environment "environment" %]
because it is the setting in which expressions are evaluated;
the dictionaries returned by the `globals` and `locals` functions
introduced in [%x test %] are both environments.

Let's modify `do_add`, `do_abs`, `do`, and `main`
to take an environment as an extra parameter and pass it on as needed:

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

<div class="callout" markdown="1">

### Everything Is An Expression

Python distinguishes [%g expression "expressions" %] that produce values
from [%g statement "statements" %] that don't.
But it doesn't have to, and many languages don't.
For example,
Python could have been designed to allow this:

```python
# not actually legal Python
result =
    if a > 0:
        1
    elif a == 0:
        0
    else:
        -1
```

</div>

## Introspection Again {: #interp-introspection}

Now that we have evaluation, function lookup, and environments,
we can write programs like this one,
which starts with the number 1 and doubles it four times:

[% inc pat="doubling.*" fill="tll out" %]

However,
our `do` function now looks like this:

[% inc file="vars.py" keep="do" %]

The sequence of `if` statements that decide what function to call
is becoming unwieldy.
(Quick:
can you see if any of the instruction names are accidentally duplicated?)
We can replace this by using [%g introspection "introspection" %]
to create a lookup table
that stores every function whose name starts with `do_`:

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

As with unit test functions in [%x test %],
the `do_*` functions must have exactly the same [%g signature "signature" %]
so that we can call any of them with an environment and a list of arguments
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

## Summary {: #interp-summary}

*Please see [%x bonus %] for extra material related to these ideas.*

[% figure
   slug="interp-concept-map"
   img="concept_map.svg"
   alt="Concept map of interpreter"
   caption="Interpreter concept map."
%]

## Exercises {: #interp-exercises}

### Arrays {: .exercise}

Implement fixed-size one-dimensional arrays:
`["array", 10]` creates an array of 10 elements,
while other instructions that you design
get and set particular array elements by index.

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

### While Loops {: .exercise}

Implement a `while` loop instruction.
Your implementation can use either a Python `while` loop or recursion.

### For Loops {: .exercise}

Implement a `for` loop instruction that repeats instructions a certain number of times.
Your implementation should allow users to specify a loop variable
so that they know which iteration of the loop they're in.
