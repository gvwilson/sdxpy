---
title: "A Testing Framework"
syllabus:
-   Functions are objects you can save in data structures or pass to other functions.
-   Python stores local and global variables in dictionary-like structures.
-   A unit test function performs an operation on a fixture and passes, fails, or produces an error.
-   A program can introspect to find functions and other objects at runtime.
---

We're going to write a lot of programs in this book.
To make sure they work correctly,
we're also going to write a lot of [%g unit_test "unit tests" %] [%b Aniche2022 %].
Most developers don't enjoy doing this,
so good unit testing tools minimize the effort required.
One way they do this is to find and run tests automatically [%b Meszaros2007 %].
To show how,
this chapter builds a simple unit testing framework.
It also introduces the single most important idea in this book:

<div class="center" markdown="1">
  *Programs are just another kind of data.*
</div>

## Storing and Running Tests {: #tester-funcobj}

The first thing we need to understand is that a function is an object.
While the bytes in a string represent characters
and the bytes in an image represent pixels,
the bytes in a function are instructions
([%f tester-func-obj %]).
When Python executes the code below,
it creates an object in memory
that contains the instructions to print a string
and assigns that object to the variable `example`:

[% inc file="func_obj.py" keep="define_example" %]

[% figure
   slug="tester-func-obj"
   img="tester_func_obj.svg"
   alt="Bytes as characters, pixels, or instructions"
   caption="Bytes can be interpreted as text, images, instructions, and more."
%]

We can assign the function to another variable:

[% inc file="func_obj.py" keep="alias" %]
[% inc file="func_obj.out" %]

or replace the function by assigning a new value
to the original variable:
{: .continue}

[% inc file="replacement.py" keep="replacement" %]
[% inc file="replacement.out" %]

We can also store functions in a list just like numbers or strings
([%f tester-func-list %]):

[% inc pat="func_list.*" fill="py out" %]

[% figure
   slug="tester-func-list"
   img="tester_func_list.svg"
   alt="A list of functions"
   caption="A list of functions."
%]

When we loop over the list `everything`,
Python assigns each function to the variable `func` in turn.
We can then call the function as `func()`
just as we called `example` using `alias()`.
{: .continue}

Now suppose we have a function we want to test:

[% inc file="dry_run.py" keep="sign" %]

and some functions that test it
(two of which contain deliberate errors):
{: .continue}

[% inc file="dry_run.py" keep="tests" %]

We can put all the test functions in a list:

[% inc file="dry_run.py" keep="save" %]

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
if a test [%g throw_exception "throws" %] an `AssertionError`
then one of our checks is reporting a failure,
while any other kind of exception indicates that the test contains an error.

Translating that rules into code gives us the function `run_tests`
that runs every test in a list
and counts how many outcomes of each kind it sees:

[% inc file="dry_run.py" keep="run" %]

If a test completes without an exception, it passes.
If any of the assertions inside it raises an `AssertionError` the test fails,
and if it raises any other exception it's an error.
{: .continue}

[% inc file="dry_run.out" %]

<div class="callout" markdown="1">

### Independence

Our function runs tests in the order they appear in the list.
The tests should not rely on that:
every unit test should work independently
so that an error or failure in an early test
doesn't affect other tests' behavior.

</div>

## Finding Functions {: #tester-reflection}

Making lists of functions is clumsy and error-prone:
sooner or later we'll add a test twice or forget to add it at all.
We'd therefore like our test runner to find tests for itself,
which it can do by exploiting the fact that
Python stores variables in a structure similar to a dictionary.

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
`globals` is a dictionary containing
all the variables at the top (global) level of the program.
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
`my_variable` is now in the dictionary.
{: .continue}

<div class="callout" markdown="1">

### Local Variables

Another function called `locals` returns
all the variables defined in the current (local) [%g scope "scope" %]:

[% inc pat="show_locals.*" fill="py out" %]

</div>

If function names are just variables
and a program's variables are stored in a dictionary,
we can loop over that dictionary
to find all the functions whose names start with `test_`:

[% inc file="find_list_test_funcs.py" keep="main" %]
[% inc file="find_list_test_funcs.out" %]

Notice that when we print a function,
Python shows us its name and its address in memory.
{: .continue}

Having a program find things in itself like this at runtime
is called [%g introspection "introspection" %].
Combining introspection with the pass-fail-error pattern of the previous section
gives us something that finds test functions,
runs them,
and summarizes their results:

[% inc file="find_report_tests.py" keep="runner" %]
[% inc file="find_report_tests.out" %]

<div class="callout" markdown="1">

### Calling Conventions

We actually can't call a function we've found by introspection unless:

1.  we know its [%g signature "signature" %]
    (i.e, how many parameters of what type it needs in what order)
    or

2.  the function uses `*args*` or `**kwargs` to capture "extra" arguments.

To keep things simple,
most unit testing frameworks require test functions to take no parameters
so that they can be called as `test()`.

</div>

## Going Further {: #tester-further}

Since functions are objects,
they can have attributes.
The function `dir` (short for "directory") returns a list of those attributes' names:

[% inc pat="func_dir.*" fill="py out" %]

Most programmers never need to use most of these,
but `__name__` holds the function's original name
and `__doc__` holds its [%i "docstring" %][%g docstring "docstring" %][%/i%]:

[% inc file="func_attr.py" keep="print" %]
[% inc file="func_attr.out" %]

We can modify our test runner to use this for reporting tests' results
using the function's `__name__` attribute
instead of the key in the `globals` dictionary:

[% inc file="with_name.py" keep="run" %]
[% inc file="with_name.out" %]

More usefully,
we can say that if a test function's docstring contains the string `"test:skip"`
then we should skip the test,
while `"test:fail"` means we expect this test to fail.
Let's rewrite our tests to show this off:

[% inc file="docstring.py" keep="tests" %]

and then modify `run_tests` to look for these strings and act accordingly:
{: .continue}

[% inc file="docstring.py" keep="run" %]

The output is now:

[% inc file="docstring.out" %]

Instead of (ab)using docstrings like this,
we can add attributes of our own to test functions.
Let's say that if a function has an attribute called `skip` with the value `True`
then the function is to be skipped,
while if it has an attribute called `fail` whose value is `True`
then the test is expected to fail.
Our tests become:

[% inc file="attribute.py" keep="tests" %]

We can write a helper function called `classify` to classify tests.
Note that it uses `hasattr` to check if an attribute is present
before trying to get its value:

[% inc file="attribute.py" keep="classify" %]

Finally,
our test runner becomes:

[% inc file="attribute.py" keep="run" %]

## Finding Test Files {: #tester-files}

[pytest][pytest] and tools like it do one more thing that our testing framework doesn't:
find files that contain tests.
For example,
if we run `pytest` on the command line,
it finds all the Python files in or below the current directory whose names start with `test_`
and runs the tests they contain.
In order to do this ourselves,
we need to:

1.  find files whose names match a pattern,
2.  load them into memory,
3.  find the test functions they contain, and
4.  run those tests (which we already know how to do).

Python's [glob][py_glob] module can do the first step.
If we have this directory structure:

[% inc pat="show_try_glob.*" fill="sh out" %]

then a single call to `glob.glob` will find all the files whose names end with `.txt`:
{: .continue}

[% inc pat="try_glob.*" fill="py sh out" %]

We can use a similar call with a different pattern
to find all the files whose names match a pattern like `test_*.py`.
{: .continue}

Once we have them,
we can use Python's `importlib` module to load them
in the same way that an `import` statement would.
Importing a module can be a complex process—for example,
the source might be a zip file containing several modules—so doing an import ourselves
is a three-step process:

1.  Build a specification of what we're going to import.
2.  Build a Python module in memory from that spec.
3.  Execute the code in the module,
    which is what actually creates the module's variables, functions, and so on.

Here's an example program that takes a path to a Python file
and the name of a variable at the top level of that file,
loads the file,
and displays the variable's value:

[% inc file="import_example.py" %]

If the file we want to load is:
{: .continue}

[% inc file="sample_dir/test_up.py" %]

we can run our example importer like this:
{: .continue}

[% inc pat="import_example.*" fill="sh out" %]

Notice that we use `getattr` to look up the variable we want.
A module is just another data structure in memory,
but it's not a dictionary,
so we can't use `module[name]` to get the things it contains.
Instead,
we use `getattr` (short for "get attribute")
to do the equivalent of `module.name`.

<div class="callout" markdown="1">

### Any Sufficiently Premature Technology

[Clarke's Third Law][clarkes_laws] is that
any sufficiently advanced technology is indistinguishable from magic.
The same is true of technologies that we encounter
before we have the background knowledge they depend on.
The three lines that import a Python file as a module
will seem reasonable (and possibly even a little dull)
once we know more about how programming languages work.
Until we do,
the sensible strategy is to copy, paste, and move on.
Even the most experienced programmers do this when working in a new domain:
it's easier to learn things once we have more context,
so setting a problem aside and returning to it later can save a lot of time.

</div>

## Summary {: #tester-summary}

[% figure
   slug="tester-concept-map"
   img="tester_concept_map.svg"
   alt="Concept map of unit testing tool"
   caption="Unit tester concept map."
%]

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
the test passes if it raises an `AssertionError`
and fails if it does not.
Tests whose docstring don't contain `"test:assert"`
should behave as before.

### Timing tests {: .exercise}

Modify the testing tool so that it records how long it takes to run each test.
(The function `time.time` may be useful.)
Use Python's own [pytest][pytest] library to test your implementation.

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
Add a similar way to register a `teardown` function.

### Parameterized tests {: .exercise}

Modify the testing framework so that
if a test function has an attribute called `cases`,
the test function is run once for each case.
For example,
if the user writes:

```python
def test_subtract(fixture, expected):
    assert fixture[0] - fixture[1] == expected
test_subtract.cases = [
    # fixture  expected
    [[5, 2],   3],
    [[2, 5],   -3],
    [[0, 0],   0]
]
```

then the test framework effectively runs:
{: .continue}

```python
test_subtract([5, 2], 3)
test_subtract([2, 5], -3)
test_subtract([0, 0], 0)
```

Make sure that all the tests run even if some fail or have errors.

### Capturing output {: .exercise}

1.  Read [the documentation][pytest_stdout]
    that explains how to capture [%g stdout "standard output" %]
    when using [pytest][pytest].

1.  Modify this chapter's testing tool so that
    users can check what a function prints to standard output
    as part of a unit test.

### Discovering test files {: .exercise}

1.  Write a program that finds all the files in or below the current directory
    whose names match the pattern `test_*.py`.

1.  Extend the program so that it loads each file
    to create a dictionary with filenames as keys and modules as values.

1.  Use Python's `dir` function and a loop to find
    all the functions in each module whose names begin with `test_`.

1.  Run these functions and report whether they pass, fail, or have an error.
