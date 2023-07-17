---
syllabus:
-   Functions are objects you can save in data structures or pass to other functions.
-   Python stores local and global variables in dictionary-like structures.
-   A unit test function performs an operation on a fixture and passes, fails, or produces an error.
-   A program can introspect to find functions and other objects at runtime.
---

Not all software needs rigorous testing:
the best way to check a one-off data analysis script,
for example,
is to build it incrementally,
looking at the output of each new stage as it's added.
But we should all be grateful that
98% of the code in the [SQLite][sqlite] database
is there to make the other 2% always does the right thing.

We're going to write a lot of programs in this book.
To make sure they work correctly,
we're also going to write a lot of [%g unit_test "unit tests" %]
[%b  Meszaros2007 Aniche2022 %].
To make those tests easier to write (so that we actually write them)
we use a unit testing framework that finds and run tests automatically.
Our tool is inspired by [pytest][pytest],
and introduces the single most important idea in this book:

<div class="center" markdown="1">
  *Programs are just another kind of data.*
</div>

## Storing and Running Tests {: #test-funcobj}

The first thing we need to understand is that a function is an [%i "object" %].
While the bytes in a string represent characters
and the bytes in an image represent pixels,
the bytes in a function are instructions
([%f test-func-obj %]).
When Python executes the code below,
it creates an object in memory
that contains the instructions to print a string
and assigns that object to the variable `example`:

[% inc file="func_obj.py" keep="def" %]

[% figure
   slug="test-func-obj"
   img="func_obj.svg"
   alt="Bytes as characters, pixels, or instructions"
   caption="Bytes can be interpreted as text, images, instructions, and more."
%]

We can create an [%g alias "alias" %] for the function
by assigning it to another variable,
and then call the function by referencing that second variable:
{: .continue}

[% inc file="func_obj.py" keep="alias" %]
[% inc file="func_obj.out" %]

This doesn't alter or erase
the connection between the function and the original name.
{: .continue}

<div class="callout" markdown="1">

### Checking Types

Python is a [%g dynamic_typing "dynamically typed" %] language,
which means that it checks the types of values as the program is running.
We can do this ourselves using its built-in `type` function,
which will tell us that `3` is an integer:

[% inc pat="type_int.*" fill="py out" %]

or that a function is a function:
{: .continue}

[% inc pat="type_func.*" fill="py out" %]

However,
built-in functions have a different type:
{: .continue}

[% inc pat="type_len.*" fill="py out" %]

so it's safer to use `callable` to check if something can be called:
{: .continue}

[% inc pat="callable.*" fill="py out" %]

</div>

Since functions are objects,
we can store them in a list just like numbers or strings
([%f test-func-list %]):

[% inc pat="func_list.*" fill="py out" %]

However,
we have to know how to call the functions in order for this trick to work,
which means they must have the same [%i "signature" %]:
{: .continue}

[% inc pat="signature.*" fill="py out" %]

[% figure
   slug="test-func-list"
   img="func_list.svg"
   alt="A list of functions"
   caption="A list of functions."
%]

When we loop over the list `everything`,
Python assigns each function to the variable `func` in turn.
We can then call the function as `func()`
just as we called `example` using `alias()`.
In order for this to work,
though,
all of the functions in the list must have the same [%i "signature" %],
i.e.,
they must all take the same number of parameters
in the same order
so that we can call them interchangeably.

Now suppose we have a function we want to test:

[% inc file="manual.py" keep="sign" %]

and some functions that test it
(two of which contain deliberate errors):
{: .continue}

[% inc file="manual.py" keep="tests" %]

We can put all the test functions in a list:

[% inc file="manual.py" keep="save" %]

Each test does something to a [%g fixture "fixture" %]
(such as the number -3)
and uses [%g assertion "assertions" %]
to compare the [%g actual_result "actual result" %]
against the [%g expected_result "expected result" %].
The outcome of each test is exactly one of:

-   [%g pass_test "Pass" %]:
    the test subject works as expected.

-   [%g fail_test "Fail" %]:
    something is wrong with the test subject.

-   [%g error_test "Error" %]:
    something is wrong in the test itself,
    which means we don't know if
    the thing we're testing is working properly or not.

To implement this classification scheme
we need to distinguish failing tests from broken ones.
Our rule is that
if a test [%g throw_exception "throws" %] an `AssertionError` [%i "exception" %]
then one of our checks is reporting a [%i "failure" %],
while any other kind of exception indicates that the test contains an error.

Translating that rules into code gives us the function `run_tests`
that runs every test in a list
and counts how many outcomes of each kind it sees:

[% inc file="manual.py" keep="run" %]

If a test completes without an exception, it passes.
If any of the assertions inside it raises an `AssertionError` the test fails,
and if it raises any other exception it's an error.
{: .continue}

[% inc file="manual.out" %]

<div class="callout" markdown="1">

### Independence

Our function runs tests in the order they appear in the list.
The tests should not rely on that:
every unit test should work independently
so that an error or failure in an early test
doesn't affect other tests' behavior.

</div>

## Finding Functions {: #test-reflection}

Making lists of functions is clumsy and error-prone:
sooner or later we'll add a function to `TESTS` twice
or forget to add it at all.
We'd therefore like our test runner to find tests for itself,
which it can do by exploiting the fact that
Python stores variables in a structure similar to a [%i "dictionary" %].

Run the Python interpreter and call the `globals` function:

[% inc pat="globals.*" fill="py out" %]

As the output shows,
`globals` is a dictionary containing
all the variables at the top (global) level of the program.
Since we just started the interpreter,
we see the variables that Python defines automatically.
(By convention,
Python uses double underscores for names that mean something special to it.)
{: .continue}

What happens when we define a variable of our own?

[% inc pat="globals_plus.*" fill="py out" %]

Sure enough,
`my_variable` is now in the dictionary.
{: .continue}

<div class="callout" markdown="1">

### Local Variables

Another function called `locals` returns
all the variables defined in the current (local) [%g scope "scope" %].

</div>

If function names are just variables
and a program's variables are stored in a dictionary,
we can loop over that dictionary
to find all the functions whose names start with `test_`:

[% inc file="find_test_funcs.py" keep="main" %]
[% inc file="find_test_funcs.out" %]

Notice that when we print a function,
Python shows us its name and its address in memory.
{: .continue}

Having a program find things in itself like this at [%i "runtime" %]
is another example of [%i "introspection" %]
([%x parse %]).
Combining introspection with the pass-fail-error pattern of the previous section
gives us something that finds test functions,
runs them,
and summarizes their results:

[% inc file="runner.py" keep="run" %]
[% inc file="runner.out" %]

## Origins {: #test-origins}

[Clarke's Third Law][clarkes_laws] is that
any sufficiently advanced technology is indistinguishable from magic.
The same is true of technologies that we encounter
before we have the background knowledge they depend on.
The code that finds tests dynamically seems reasonable
(and possibly even a little dull)
to an expert who understands how programming languages work,
but is incomprehensible magic to a novice.

We didn't invent any of the ideas we just presented.
Instead,
we did what you are doing now:
we read what other programmers had written
and tried to make sense of the key ideas.

The problem is that "making sense" depends on who we are.
When we use a low-level language,
we incur the [%g cognitive_load "cognitive load" %]
of assembling micro-steps into something more meaningful.
When we use a high-level language,
on the other hand,
we incur a similar load translating functions of functions of functions
into actual operations on actual data.

More experienced programmers are more capable at both ends of the curve,
but that's not the only thing that changes.
If a novice's comprehension curve looks like the lower one in [%f test-comprehension %],
then an expert's looks like the upper one.
Experts don't just understand more at all levels of abstraction;
their *preferred* level has also shifted
so they find \\(\sqrt{x^2 + y^2}\\) easier to read
than the medieval expression
"the side of the square whose area is the sum of the areas of the two squares
whose sides are given by the first part and the second part".

[% figure
   slug="test-comprehension"
   img="comprehension.svg"
   alt="Comprehension curves"
   caption="Novice and expert comprehension curves."
%]

This curve means that for any given task,
the code that is quickest for a novice to comprehend
will almost certainly be different from the code that
an expert can understand most quickly.
In an ideal world our tools would automatically re-represent programs at different levels
just as we could change the colors used for syntax highlighting.
But today's tools don't do that,
and any IDE smart enough to translate between comprehension levels automatically
would also be smart enough to write the code without our help.

*Please see [%x bonus %] for extra material related to these ideas.*

## Summary {: #test-summary}

[% figure
   slug="test-concept-map"
   img="concept_map.svg"
   alt="Concept map of test runner"
   caption="Concept map"
%]

## Exercises {: #test-exercises}

### Why a Copy? {: .exercise}

Why does the function `globals` return a copy of the dictionary
containing the program's global variables?
Why doesn't it return the dictionary itself so that programs can modify it?
Why use a function at all instead of simply using a variable called `__globals__`?

### Looping Over `globals` {: .exercise}

What happens if you run:

```python
for name in globals():
    print(name)
```

What happens if you run:

```python
name = None
for name in globals():
    print(name)
```

Why?

### Counting Results {: .exercise}

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.

2.  Write unit tests to check that your answer to part 1 works correctly.

### Setup and Teardown {: .exercise}

Testing frameworks often allow programmers to specify a `setup` function
that is to be run before each test
and a corresponding `teardown` function
that is to be run after each test.
(`setup` usually re-creates complicated test fixtures,
while `teardown` functions are sometimes needed to clean up after tests,
e.g., to close database connections or delete temporary files.)

Modify the testing tool in this chapter so that
if a file of tests contains a function called `setup`
then the tool calls it exactly once before running each test in the file.
Add a similar way to [%g register_code "register" %] a `teardown` function.

### Module Names {: .exercise}

Our last test runner generated names `m0`, `m1`, and so on
so that each [%i "module" %] would have a unique name.
What happens if we don't do this?
I.e.,
what happens if we use the same constant string for all modules that we load?

### Timing Tests {: .exercise}

Modify the testing tool so that it records how long it takes to run each test.
(The function `time.time` may be useful.)

### Selecting Tests {: .exercise}

Modify the testing tool so that if a user provides `-s pattern` or `--select pattern`
then it only runs tests that contain the string `pattern` in their name.
