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

We're going to write a lot of programs in this book.
To make sure they work correctly,
we're going to write a lot of [%g unit_test "unit tests" %] using [pytest][pytest].
Like the earlier tools that inspired it [%b Meszaros2007 %],
pytest finds and runs tests automatically;
to show how,
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

## Mock Objects {: #tester-mock}

We can do more than look up functions:
we can change them to make testing easier.
For example,
if the function we want to test uses the time of day,
we can temporarily replace the real `time.time` function
with one that returns a specific value
so we know what result to expect:

[% inc file="mock_time.py" %]

Temporary replacements like this are called [%g mock_object "mock objects" %]
because we usually use objects even if the thing we're replacing is a function.
We can do this because Python lets us create objects
that can be "called" just like functions.
If an object `obj` has a `__call__` method,
then `obj(…)` is automatically turned into `obj.__call__(…)`.
For example,
the code below defines a class `Adder` whose instances add a constant to their input:

[% inc pat="callable.*" fill="py out" %]

Let's create a reusable mock object class that:

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
with an instance of our `Fake` class:

[% inc file="mock_object.py" keep="fixit" %]

To show how this works,
we define a function that adds two numbers
and write a test for it:

[% inc file="mock_object.py" keep="test_real" %]

We then use `fixit` to replace the real `adder` function
with a mock object that always returns 99
([%f tester-mock-timeline %]):

[% inc file="mock_object.py" keep="test_fixed" %]

[% figure
   slug="tester-mock-timeline"
   img="tester_mock_timeline.svg"
   alt="Timeline of mock operation"
   caption="Timeline of mock operation."
%]

Another test proves that our `Fake` class records
all of the calls:

[% inc file="mock_object.py" keep="test_record" %]

And finally,
the user can provide a function to calculate a return value:

[% inc file="mock_object.py" keep="test_calc" %]

## Protocols {: #tester-protocols}

Mock objects are very useful,
but the way we're using them is going to cause strange errors.
The problem is that
every test except the first one replaces `adder` with a mock object
that does something different.
As a result,
any test that *doesn't* replace `adder` will run with
whatever mock object was last put in place
rather than with the original `adder` function.

We could tell users it's their job to put everything back after each test,
but people are forgetful.
It would be better if Python did this automatically;
luckily for us,
it provides a [%g protocol "protocol" %] for exactly this purpose.
A protocol is a rule that specifies how programs can tell Python
to do specific things at specific moments.
Giving a class a `__call__` method is an example of this:
when Python sees `thing(…)`,
it automatically checks if `thing` has that method.
Defining an `__init__` method for a class is another example:
if a class has a method with that name,
Python calls it automatically when constructing a new instance of that class.

What we want for managing mock objects is
a [%g context_manager "context manager" %]
that replaces the real function with our mock at the start of a block of code
and then puts the original back at the end.
The protocol for this relies on two methods called `__enter__` and `__exit__`.
If the class is called `C`,
then when Python executes a `with` block like this:

```python
with C(…args…) as name:
    …do things…
```

it does the following:
{: .continue}

1.  Call `C`'s constructor to create an object that it associates with the code block.
2.  Call that object's `__enter__` method
    and assign the result to the variable `name`.
3.  Run the code inside the `with` block.
4.  Call `name.__exit__()` when the block finishes.

Here's a mock object that inherits all the capabilities of `Fake`
and adds the two methods needed by `with`:

[% inc file="mock_context.py" keep="contextfake" %]

Notice that `__enter__` doesn't take any extra parameters:
anything it needs should be provided to the constructor.
On the other hand,
`__exit__` will always be called with three values
that tell it whether an exception occurred,
and if so,
what the exception was.

Here's a test to prove that our context manager works:
{: .continue}

[% inc file="mock_context.py" keep="test" %]

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
Add a similar way to register a `teardown` function.
