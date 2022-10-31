---
title: "A Testing Framework"
syllabus:
-   Functions are objects you can save in data structures or pass to other functions.
-   Python stores local and global variables in dictionary-like structures.
-   A unit test function performs an operation on a fixture and passes, fails, or produces an error.
-   A program can introspect to find functions and other objects at runtime.
-   Temporarily replacing functions with mock objects can simplify testing.
-   Python defines protocols so that users' code can be triggered by keywords in the language.
---

We're going to write a lot of programs in this book,
which means we're going to write a lot of [%g unit_test "unit tests" %].
A tool to manage these should find and run tests automatically
so that we don't overlook them when we're tired,
distracted,
or up against a deadline.

Our design was inspired by [pytest][pytest],
which in turn was inspired by earlier tools [%b Meszaros2007 %].
It introduces the single most important idea in this book:

<div class="center" markdown="1">
  *A program is just another kind of data.*
</div>

## Storing and Running Tests {: #tester-funcobj}

The first thing we need to understand is that a function is an object.
While a string's bytes represent characters
and an image's bytes represent pixels,
a function's bytes represent instructions.
The code:

[% inc file="func_obj.py" keep="define_example" %]

tells Python to create an object in memory
that contains the instructions to print a string
and assign that object to the variable `example`."
We can create an [%g alias "alias" %] for the function
by assigning it to another variable:
{: .continue}

[% inc file="func_obj.py" keep="alias" %]
[% inc file="func_obj.out" %]

or replace the function by assigning a new value
to the original variable:
{: .continue}

[% inc file="replacement.py" keep="replacement" %]
[% inc file="replacement.out" %]

We can also store functions in a list just like numbers or strings:

[% inc pat="func_list.*" fill="py out" %]

When we loop over the list `everything`,
Python assigns each function to the variable `func` in turn.
We can then call the function as `func()`
just as we called `example` using `alias()`.
{: .continue}

With this in hand,
we can register tests by appending functions to a list:

[% inc file="dry_run.py" keep="save" %]

Each test does something to a [%g fixture "fixture" %]
and uses [%g assertion "assertions" %]
to compare the [%g actual_result "actual result" %]
against the [%g expected_result "expected result" %]:

[% inc file="dry_run.py" keep="tests" %]

The outcome of each test is exactly one of:

-   [%g pass_test "Pass" %]:
    the test subject works as expected.

-   [%g fail_test "Fail" %]:
    something is wrong with the test subject.

-   [%g error_test "Error" %]:
    something is wrong in the test itself,
    which means we don't know whether the test subject is working properly or not.

We need to distinguish failing tests from broken ones
in order to implement this classification scheme.
Our rule is that
if a test [%g throw_exception "throws" %] an `AssertionError`
then one of our checks is reporting a failure,
while any other kind of exception indicates that the test contains an error.

Putting this all together gives us a function `run_tests`
that runs all registered tests
and counts how many outcomes of each kind it sees:

[% inc file="dry_run.py" keep="run_tests" %]

If a test completes without an exception, it passes.
If any of the assertions inside it raise an `AssertionError` the test fails,
and if it raises any other exception it's an error.
After all tests are run,
`run_tests` reports the number of results of each kind:
{: .continue}

[% inc file="dry_run.out" %]

<div class="callout" markdown="1">

### Independence

We're appending tests to a list,
so they will be run in the order in which they are registered.
We should not rely on that:
every unit test should work independently
so that an error or failure in an early test
doesn't affect other tests' behavior.

</div>

## Finding Functions {: #tester-reflection}

Registering tests by hand is clumsy and error-prone:
sooner or later we'll add a test twice or forget to add it at all.
We would therefore like our tool to find tests for itself.
It can do this by exploiting the fact that
Python stores our variables in a structure similar to a dictionary.

Run the Python interpreter and call the `globals` function:

```
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

As the output shows,
`globals` returns a copy of the dictionary that Python uses
to store all the variables at the top (global) level of your program.
Since we just started the interpreter,
we see the variables that Python defines automatically.
(By convention,
Python uses double underscores for names that mean something special to it.)
{: .continue}

What happens when we define a variable of our own?

```
>>> my_variable = 123
>>> globals()
{
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': <class '_frozen_importlib.BuiltinImporter'>,
    '__spec__': None,
    '__annotations__': {},
    '__builtins__': <module 'builtins' (built-in)>,
    'my_variable': 123
}
```

Sure enough,
`my_variable` is now in the global dictionary.
{: .continue}

<div class="callout" markdown="1">

### Local Variables

Another function called `locals` returns
all the variables defined in the current (local) scope:

[% inc pat="show_locals.*" fill="py out" %]

</div>

If a program's variables are stored in a dictionary,
we can iterate over that dictionary's keys
to find all the functions whose names start with `test_`
and put them in a list:

[% inc pat="find_list_test_funcs.*" fill="py out" %]

Having a program find things in itself as it's running is called [%g introspection "introspection" %];
we will use it in several upcoming chapters.
Notice that when we print a function,
Python shows us its name and its address in memory.
We have no use for the address,
but we'll come back to the name shortly.
{: .continue}

Combining introspection with the pass-fail-error pattern of the previous section
gives us something that will look up test functions,
run them,
and summarize their results:

[% inc file="find_report_tests.py" keep="runner" %]
[% inc file="find_report_tests.out" %]

<div class="callout" markdown="1">

### Calling Conventions

We actually can't call a function we've found by introspection unless:

1.  we know its [%g function_signature "signature" %]
    (i.e, how many parameters of what type it needs in what order)
    or

2.  the function uses `*args*` or `**kwargs`
    to capture any number of "extra" arguments.

To keep things simple,
most testing frameworks require unit test functions to take no parameters
so that they can be called as `test()`.

</div>

## Going Further {: #tester-further}

The next step is to get our tool to tell us which tests have passed or failed
and to use test functions' docstrings to control which tests are run.
The key to doing both is the fact that functions can have attributes
just like any other object in Python.
The function `dir` (short for "directory") returns a list of those attributes' names:

[% inc pat="func_dir.*" fill="py out" %]

Most programmers never need to use most of these,
but `__doc__` holds the function's [%g docstring "docstring" %]
and `__name__` holds its original name:

[% inc file="func_attr.py" keep="print" %]
[% inc file="func_attr.out" %]

We can print each function's name when reporting problems,
but we can also embed instructions for the test framework in them.
For example,
we could decide that the string `"test:skip"` means "skip this test",
while `"test:fail"` means "we expect this test to fail".
Let's rewrite our tests to show this off:

[% inc file="docstring.py" keep="tests" %]

and then modify `run_tests` to look for these strings and act accordingly:
{: .continue}

[% inc file="docstring.py" keep="run" %]

The output is now:

[% inc file="docstring.out" %]

## Mock Objects

We can do more than look up functions:
we can change them to make testing easier.
For example,
if our test relies on the time of day,
we can temporarily replace the real `time.time` function
with one that returns a specific value.
Similarly,
if a test needs data from a database,
we can temporarily replace the function that gets the data
with one that returns a small, constant dataset
that has exactly the properties our test wants.

Temporary replacements like this are called [%g mock_object "mock objects" %]
because they mimic the essential behavior of the real objects in the program.
We usually use objects even if the thing we're replacing is a function;
we can do this because Python lets us create objects that can be called just like functions
by defining a `__call__` method:

[% inc pat="callable.*" fill="py out" %]

Let's create a class that:

1.  defines a `__call__` method so that instances can be called like functions;

2.  declares the parameters of that method to be `*args*` and `**kwargs`
    so that it can be called with any number of regular or keyword arguments;

3.  stores those arguments so we can see how the replaced function was called;
    and

4.  returns either a fixed value or a value produced by a user-defined function.

The class itself is only 11 lines long:

[% inc file="mock_object.py" keep="fake" %]

For convenience,
let's also define a function that replaces some function we've already defined
with an instance of our `Fake` class.
This function takes either a fixed value or another function as an argument
and passes those to `Fake`'s constructor:

[% inc file="mock_object.py" keep="fixit" %]

Next,
we define a function that adds two numbers
and write a test for it:

[% inc file="mock_object.py" keep="test_real" %]

We then use `fixit` to replace the real `adder` function
with a mock object that always returns 99:

[% inc file="mock_object.py" keep="test_fixed" %]

Another test proves that our `Fake` class records
all of the calls:

[% inc file="mock_object.py" keep="test_record" %]

And finally,
the user can provide a function to calculate a return value:

[% inc file="mock_object.py" keep="test_calc" %]

Mock objects are very useful,
but there's a problem with how we're using them.
Every test except the first one replaces `adder` with a mock object
that does something different.
As a result,
any test that *doesn't* replace `adder` will run with
whatever mock object was last put in place
rather than with the original `adder` function:

[% inc file="mock_object.out" %]

We could tell users they have to remember to put everthing back after each test,
but people are forgetful.
Instead,
we can create a [%g context_manager "context manager" %] that does this automatically.
A context manager is a class that defines two methods called `__enter__` and `__exit__`.
If the class is called `C`,
then when Python executes a `with` block like this:

```python
with C(…args…) as name:
    …do things…
```

it does the following:
{: .continue}

1.  Call `C`'s constructor with the given arguments.
2.  Assign the result to the variable `name`.
3.  Call `name.__enter__()`.
4.  Run the code inside the `with` block.
5.  Call `name.__exit__()` when the block finishes.

The last step is guaranteed to happen
even if an exception occurred inside the block
so that the context manager always has a chance to clean up after itself.
{: .continue}

Here's a mock object that inherits all the capabilities of `Fake`
and adds the two methods needed by `with`:

[% inc file="mock_context.py" keep="contextfake" %]

And here's a test to prove that it works:
{: .continue}

[% inc file="mock_context.py" keep="test" %]

<div class="callout" markdown="1">

### Protocols

`__enter__` and `__exit__` are an example of a [%g protocol "protocol" %]:
a rule that specifies how programs can provide operations
that Python will execute at specific moments.
Defining an `__init__` method for a class is another example:
if a class has a method with that name,
Python will call it automatically when constructing a new instance of that class.

</div>

## Exercises {: #tester-exercises}

### Why a copy? {: .exercise}

Why does the function `globals` return a copy of the dictionary
containing the program's global variables?
Why doesn't it return the dictionary itself so that programs can modify it?
Why use a function at all instead of simply using a variable called `__globals__`?

### Counting results {: .exercise}

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.

2.  Write unit tests to check that your answer to part 1 works correctly.

3.  Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.

### Literal strings {: .exercise}

If we have defined a variable with the test-skipping marker,
why can't we use that variable as the docstring for several functions like this:

```python
TEST_SKIP = "test:skip"

def test_sign_negative():
    TEST_SKIP
    assert sign(-3) == -1

def test_sign_positive():
    TEST_SKIP
    assert sign(3) == 1
```

### Failing on purpose {: .exercise}

Putting assertions into code to check that it is behaving correctly
is called [%g defensive_programming "defensive programming" %];
it's a good practice,
but we should make sure those assertions are failing when they're supposed to,
just as we should test our smoke detectors every once in a while.

Modify the tester so that
if a test function's docstring is `"test:assert"`,
the test passes if it raises an `AssertionErro`
and fails if it does not.
Tests whose docstring don't contain `"test:assert"`
should behave as before.

### Timing tests {: .exercise}

1.  Modify the testing tool so that it records how long it takes to run each test.
    (The function `time.time` may be useful.)

2.  Use Python's own [pytest][pytest] library to test your implementation.
    (Hint: you may want to replace `time.time` with a mock object for testing.)

### Timing blocks {: .exercise}

Create a context manager called `Timer` that reports how long it has been
since a block of code started running:

```python
# your class goes here

with Timer() as start:
    # ...do some lengthy operation...
    print(start.elapsed())  # time since the start of the block
```

### Approximately equal {: .exercise}

1.  Write a function `assert_approx_equal`
    that does nothing if two values are within a certain tolerance of each other
    but throws an exception if they are not:

        // throws exception
        assert_approx_equal(1.0, 2.0, 0.01, "Values are too far apart")

        // does not throw
        assert_approx_equal(1.0, 2.0, 10.0, "Large margin of error")

2.  Modify the function so that a default tolerance is used if none is specified:

        // throws exception
        assert_approx_equal(1.0, 2.0, "Values are too far apart")

        // does not throw
        assert_approx_equal(1.0, 2.0, "Large margin of error", 10.0)

3.  Modify the function again so that it checks the [%g relative_error "relative error" %]
    instead of the [%g absolute_error "absolute error" %].
    (The relative error is the absolute value of the difference between the actual and expected value,
    divided by the absolute value.)

### Capturing output {: .exercise}

1.  Read [the documentation][pytest_stdout]
    that explains how to capture [%g stdout "standard output" %]
    when using [pytest][pytest].

1.  Modify this chapter's testing tool so that
    users can check what a function prints to standard output
    as part of a unit test.

### Selecting tests {: .exercise}

Modify the testing tool so that if a user provides `-s pattern` or `--select pattern`
then it only runs tests that contain the string `pattern` in their name.

### Setup and teardown {: .exercise}

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
Add a similar way to register a teardown function.
