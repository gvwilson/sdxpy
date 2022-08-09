---
title: "Interpreter"
syllabus:
- Compilers and interpreters are programs like any others.
---

Many software tools take advantage of the fact that
a program is just a data structure.
While the values in a string represent characters
and the values in an image represent pixels,
the values in a program represent instructions.
We can manipulate those instructions just like we manipulate characters and pixels.
This chapter shows how to do that
by building a very small programming language.

Real programming languages have two parts:
a [%g parser "parser %] that translates the source code into a data structure in memory,
and a [%g runtime "runtime" %] that executes the instructions in that data structure.
To keep this chapter manageable we only consider the runtime;
[%x parser %] will explore parsing.

## Expressions {: #interpreter-expressions}

Let's start by building something that can evaluate simple expressions
like `1+2` or `abs(-3.5)`.
We represent each expression as a list
with the name of the operation as the first element
and the values to be operated on as the other elements.
Our first expression is:

```python
["add", 1, 2]
```

and our second is:
{: .continue}

```python
["abs", -3.5]
```

We represent more complicated expressions with nested lists:

```python
# abs(1+2)
["abs", ["add", 1, 2]]
```

We use lists because that's all programs are:
lists of instructions,
some of which are other lists of instructions.
We put the name of the operation first to make it easy to find.

The function to add two expressions looks like this:

[%excerpt f="expr.py" keep="do_add" %]

Its single parameter is a list containing
the two sub-expressions to be evaluated and added.
After checking that it has the right number of parameters,
it calls the function `do` to evaluate those sub-expressions.
(We've called the function `do` instead of `eval`
because Python already has a function called `eval`.)
Once `do_add` has two actual values,
it adds them and returns the result.
{: .continue}

<div class="callout" markdown="1">
### Argument versus parameter

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

[%excerpt f="expr.py" keep="do_abs" %]

`do_add` and `do_abs` both rely on `do`,
which figures out what function corresponds to an operation name
and calls it:

[%excerpt f="expr.py" keep="do" %]

`do` starts by checking if its input is an integer.
If so,
it returns that value right away
because integers "evaluate" to themselves:
no more calculation is needed.
Otherwise,
`do` checks that its parameter is a list
and then uses the first value in the list
to decide what other function to call.
This process is often called [%g dispatch "dispatch" %].

Finally,
the main body of the program reads
the file containing the instructions to execute,
calls `do`,
and prints the result:

[%excerpt f="expr.py" keep="main" %]

Since our instructions are a list (of lists of lists…)
we can use `json.load` to read the input file.
If that file is:

[% excerpt f="expr.tll" %]

then our little interpreter prints:
{: .continue}

[% excerpt f="expr.out" %]

This is a lot of code to do something that Python already does,
but the key point is that
*this is what Python does internally*.
When we run our little interpreter with:

```bash
$ python expr.py expr.tll
```

Python reads `expr.py`,
turns it into a data structure with operation identifiers and constants,
then uses those operation identifiers to decide what functions to call.
Those functions are written in C,
but the cycle of lookup, call, and recurse is exactly the same.

## Variables {: #interpreter-variables}

Adding up constants is a good start,
but real programming languages let us give names to values.
We can add this to our interpreter
by passing around a dictionary containing all the variables seen so far.
Such a dictionary is often called an [%g environment "environment %]
because it is the setting in which expressions are evaluated.

We can easily modify existing functions like `do_abs`
to take an environment as an extra parameter and pass it on to `do` as needed:

[% excerpt f="vars.py" keep="do_abs" %]

Looking up variables when we need their values is straightfoward.
We check that we have a variable name and that the name is in the environment,
then return the stored value:

[% excerpt f="vars.py" keep="do_get" %]

To define a new variable or change an existing one,
we evaluate an expression and store its value in the environment:

[% excerpt f="vars.py" keep="do_get" %]

We need to add one more function to make this all work.
Our programs no longer consist of a single expression;
instead,
we may have several expressions that set variables' values
and then use them in calculations.
To handle this,
we can add a function `do_seq` that runs a sequence of expressions one by one:

[% excerpt f="vars.py" keep="do_seq" %]

Let's try it out.
Our test program is:

[% excerpt f="vars.tll" %]

and its output is:
{: .continue}

[% excerpt f="vars.out" %]

## Reflection {: #interpreter-reflection}

`do_seq` is our first piece of [%g control_flow "control flow" %]
that controls when and how other expressions are evaluated.
Before we add more (and more basic operations)
let's have a look at the current state of `do`:

[% excerpt f="vars.py" keep="do" %]

The sequence of `if` statements that decide what function to call
is going to become unreadably long.
Let's create a lookup table instead:

[% excerpt f="vars_table.py" keep="lookup" %]

and then look up the function we want:
{: .continue}

[% excerpt f="vars_table.py" keep="do" %]

This lookup table is the central point of this chapter.
A program is just a data structure
with instructions and functions instead of characters and pixels.
That means we can put functions in other data structures such as dictionaries
just like we would put in strings or images.

Of course we still have to know how to call the function,
i.e.,
what parameters to give it in what order.
That's why all the `do_*` functions have exactly the same [%g signature "signature" %]:
we can all any of them with an environment and a list of arguments
without knowing exactly which function we're calling.

We can go one step further with our lookup table.
Python has a built-in function called `globals`
that returns a dictionary of all the variables defined at the top level of the current running program.
This dictionary is essentially the same thing as the environment
we are passing around in our interpreter.
If we call the function in a newly-launched interpreter we get this:

```python
>>> globals()
{
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': <class '_frozen_importlib.BuiltinImporter'>,
    '__spec__': None,
    '__annotations__': {},
    '__builtins__': <module 'builtins' (built-in)>
}
```

which shows us that Python has defined seven variables for us
before our code even starts running.
(We'll take a closer look at some of these variables in future chapters.)
{: .continue}

If we define a variable of our own and then re-run `globals`,
our variable shows up along with the predefined ones:

```python
>>> example = 3
>>> globals()
{
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': <class '_frozen_importlib.BuiltinImporter'>,
    '__spec__': None,
    '__annotations__': {},
    '__builtins__': <module 'builtins' (built-in)>,
    'example': 3
}
```

Let's use this to add every function whose name starts with `do_`
to the `OPS` lookup table:

[% excerpt f="vars_reflect.py" keep="lookup" %]

Line by line:
{: .continue}

1.  We are using a [%g dictionary_comprehension "dictionary comprehension" %]
    to create a dictionary in a single statement.

1.  Each key-value pair in the dictionary is the name of an operation
    and the function that implements the operation.
    The operation's name is what comes after `do_` in the function's name.

1.  We only add functions whose names start with `do_`.

Looking things up in a live program like this is called [%g reflection "reflection" %].
We're going to use it a lot in the chapters to come.

## Statements {: #interpreter-statements}

We're finally ready to add some more control flow to our little languages.
Our goal is to execute this program,
which starts with the number 1 and doubles it four times:

[% excerpt f="doubling.tll" %]

The simplest of the new operations is `comment`,
which does nothing and returns `None`:

[% excerpt f="stmt.py" keep="comment" %]

An `if` statement is a bit more complex.
If its first argument is true it evaluates and returns its second argument
(the "if" branch).
Otherwise,
it evaluates and returns its second argument (the "else" branch):

[% excerpt f="stmt.py" keep="if" %]

This is called [% g lazy_evaluation "lazy evaluation" %]:
`do_if` only evaluates what it absolutely needs to.
Most languages do this so that we can write things like:
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
{: .continue}

## Functions {: #interpreter-functions}

There are many ways to assess the design of a piece of software [%b Wilson2022 %].
One of them is to ask how [%g extensibility "extensible" %] it is,
i.e.,
how easily we can add or change things.
The answer for our little interpreter is, "Pretty easily."
Whenever we want it to do something new,
like a `for` loop,
all we have to do is add a function called `do_whatever`
that takes an environment and a list of arguments.
That function is added to the lookup table automatically
and no other function needs to be modified in order to use it.

Once our little language has variables, loops, and conditionals
it can do everything that any programming language can do.
However,
writing programs will still be painful
because our little language isn't extensible:
there's no way for users to define new operations within the language itself.

Doing this makes the code less than 60 lines longer:

1.  Instead of using a single dictionary to store an environment
    we use a list of dictionaries.
    The first dictionary is the global environment;
    the others store variables belonging to active function calls.

2.  When we get or set a variable,
    we check the most recent environment first
    (i.e., the one that's last in the list);
    if the variable isn't there we look in the global environment.
    We *don't* look at the environments in between.

3.  A function definition looks like:

    ```python
    ["def", "same", ["num"], ["get", "num"]]
    ```

    It has a name, a (possibly empty) list of parameter names,
    and a single instruction as a body
    (which will usually be a `"seq"` instruction).

4.  Functions are stored in the environment like any other value.
    The value stored for the function defined above would be:

    ```python
    ["func", ["num"], ["get", "num"]]
    ```

    We don't need to store the name: that's recorded by the environment,
    just like it is for any other variable.

5.  A function call looks like:

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

Here's the implementation of `do_def`:

[% excerpt f="func.py" keep="def" %]

And here's the implementation of `do_call`:

[% excerpt f="func.py" keep="def" %]

Our test program looks like this:

[% excerpt f="func.tll" %]

and its output is:
{: .continue}

[% excerpt f="func.out" %]

Once again,
the key point is that
*this is how Python and other languages work*.

## Exercises {: #interpreter-exercises}

### Arrays {: .exercise}

Implement fixed-size one-dimensional arrays:
`["array", "new", 10]` creates an array of 10 elements,
while other instructions get and set particular array elements by index.

### While Loops {: .exercise}

1.  Add a `while` loop using a Python `while` loop.

1.  Add a `while` loop using recursion.

### Loop Counter {: .exercise}

The `"repeat"` instruction runs some other instruction(s) several times,
but there is no way to access the loop counter inside those instructions.
Modify `"repeat"` so that programs can do this.
(Hint: allow people to create a new variable to hold the loop counter's current value.)

### Better Error Handling {: .exercise}

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

### Early Return {: .exercise}

Add a `"return"` instruction to TLL that ends a function call immediately
and returns a single value.

### Variable Arguments {: .exercise}

Add variable-length parameter lists to functions.

### Nested Scopes {: .exercise}

The interpreter allows users to define functions inside functions.
What variables can the inner function access when you do this?
What variables *should* it be able to access?
What would you have to do to enable this?
