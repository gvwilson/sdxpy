---
title: "A Testing Framework"
syllabus:
- Functions are objects that can be saved in data structures or passed as arguments to other functions.
- Python stores variables in a structure like a dictionary.
- A unit test is a function that takes a fixture, performs an operation, and passes, fails, or produces an error.
- Use reflection to discover functions and other values in programs at runtime.
- Replace actual functions with mock objects temporarily to simplify testing.
---

We are going to write many small programs in the coming chapters
but not a lot of re-runnable tests.
That's OK for exploratory programming,
but if our software is going to be used instead of just read,
we should try to make sure it works.

A tool for writing and running [%g unit_test "unit tests" %] is a good first step.
Such a tool should:

-   find files containing tests;
-   find the tests in those files;
-   run the tests;
-   capture their results; and
-   report each test's result and a summary of those results.

Our design is inspired by [pytest][pytest],
which was in turn inspired by many tools built for other languages
from the 1980s onward [%b Meszaros2007 %].

## Functions as Objects {: #tester-funcobj}

[% fixme "explain that functions are objects" %]

## Finding Functions {: #tester-reflection}

The first thing we need to understand is how Python stores variables.
The answer is, "In a dictionary."
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

`globals` returns a copy of the dictionary that Python uses
to store all the variables at the top (global) level of your program.
Since we just started the interpreter,
what we get are the variables that Python defines automatically:
it uses double underscores like `__name__` for these variables,
but they're just string keys in a dictionary.

Let's define a variable of our own:

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

There's our variable `my_variable` and its value.

There's another function called `locals` that returns a dictionary full of
all the variables defined in the current (local) scope.
Let's create a function that takes a parameter,
creates a local variable,
and then shows what's in scope:

```python
def show_off(some_parameter):
    some_variable = some_parameter * 2
    print("local values", locals())

show_off("hello")
```

```txt
local values {'some_parameter': 'hello', 'some_variable': 'hellohello'}
```

The second thing we need to understand is that
a function is just another kind of object:
while a string object holds characters
and an image object holds pixels,
a function object holds instructions.
When we write:

```python
def example():
    print("in example")
```

what we're actually doing is saying,
"Please create an object containing the instructions to print a string
and assign it to the variable `example`."
Here's proof:

```python
alias = example
alias()
```

```text
in example
```

We can also assign to the original variable:

```python
def replacement():
    print("in replacement")

example = replacement
example()
```

```text
in replacement
```

Like other objects,
functions have attributes.
We can use `dir` (short for "directory") to get a list of their names:

```python
def example():
    "Docstring for example."
    print("in example")

print(dir(example))
```

```text
[
    '__annotations__', '__builtins__', '__call__', '__class__'
    '__closure__', '__code__', '__defaults__', '__delattr__'
    '__dict__', '__dir__', '__doc__', '__eq__', '__format__' '__ge__',
    '__get__', '__getattribute__', '__globals__' '__gt__', '__hash__',
    '__init__', '__init_subclass__' '__kwdefaults__', '__le__',
    '__lt__', '__module__', '__name__' '__ne__', '__new__',
    '__qualname__', '__reduce__', '__reduce_ex__' '__repr__',
    '__setattr__', '__sizeof__', '__str__', '__subclasshook__'
]
```

I don't know what all of these do,
but `__doc__` holds the documentation string (docstring) for the function
and `__name__` holds its original name:

```
print("docstring:", example.__doc__)
print("name:", example.__name__)
```

```text
docstring: Docstring for example.
name: example
```

If a program's variables are stored in a dictionary,
we can iterate over them.
Let's do that to find all the functions whose names start with `test_`:

```python
def test_addition():
    assert 2 + 2 == 4

def test_multiplication():
    assert 3 * 3 == 9

def test_remainder():
    assert 15 % 4 == 0 # this is wrong

def find_tests():
    result = []
    for (name, func) in globals().items():
        if name.startswith("test_"):
            result.append(func)
    return result

print("all the test functions", find_tests())
```

```text
all the test functions [
    <function test_addition at 0x1008d7d90>,
    <function test_multiplication at 0x1009fb010>,
    <function test_remainder at 0x1009fb0a0>
]
```

Remember, a function is just another kind of object in Python:
when we print the function out,
Python shows us its name and its address in memory.
If we have a function we can call it,
which means we can find all the `test_` functions in this file
and call them one by one.

We can do more than just call functions:
we can check if they run to completion or raise an exception
and report that:

```python
def test_addition():
    assert 2 + 2 == 4

def test_multiplication():
    assert 3 * 3 == 9

def test_remainder():
    assert 15 % 4 == 0 # this is wrong

def run_tests():
    for (name, func) in globals().items():
        if name.startswith("test_"):
            try:
                func()
                print(func.__name__, "passed")
            except AssertionError:
                print(func.__name__, "failed")

run_tests()
```

```text
test_addition passed
test_multiplication passed
test_remainder failed
```

Notice that all the `test_` functions can be called with no arguments.
If some of them required arguments,
we'd have to know what it expected and then call it with the right number of values.
On the other hand,
if we say that test functions all have the same signature (i.e., parameter list),
we can call them interchangeably.

## Structuring Tests {: #tester-structure}

As in other unit testing frameworks,
each test will be a function of zero arguments
so that the framework can run them all in the same way.
Each test will create a [%g fixture "fixture" %] to be tested
and use [%g assertion "assertions" %]
to compare the [%g actual_result "actual result" %]
against the [%g expected_result "expected result" %].
The outcome can be exactly one of:

-   [%g pass_test "Pass" %]:
    the test subject works as expected.

-   [%g fail_test "Fail" %]:
    something is wrong with the test subject.

-   [%g error_test "Error" %]:
    something is wrong in the test itself,
    which means we don't know whether the test subject is working properly or not.

To make this work,
we need some way to distinguish failing tests from broken ones.
Our solution relies on the fact that exceptions are objects
and that a program can use [%g introspection "introspection" %]
to determine the class of an object.
If a test [%g throw_exception "throws an exception" %] whose class is `AssertionError`,
then we will assume the exception came from
one of the assertions we put in the test as a check.
Any other kind of assertion indicates that the test itself contains an error.

To start,
let's record tests and what they mean.
We don't run tests immediately
because we want to wrap each one in our own [%g exception_handler "exception handler" %].
Instead,
the function `hope_that` saves a descriptive message and a function that implements a test
in an array:

[% inc file="dry_run.py" keep="save" %]

<div class="callout" markdown="1">

### Independence

Because we're appending tests to an array,
they will be run in the order in which they are registered,
but we shouldn't rely on that.
Every unit test should work independently of every other
so that an error or failure in an early test
doesn't affect the result of a later one.

</div>

The function `main` runs all registered tests:

[% inc file="dry_run.py" keep="main" %]

If a test completes without an exception, it passes.
If any of the `assert` calls inside the test raises an `AssertionError`,
the test fails,
and if it raises any other exception,
it's an error.
After all tests are run,
`main` reports the number of results of each kind.
{: .continue}

Let's try it out:

[% inc file="dry_run.py" keep="use" %]
[% inc file="dry_run.out" %]

## Discovery {: #tester-discovery}

This simple approach does what it's supposed to, but:

1.  It doesn't tell us which tests have passed or failed.

1.  The description of the test is separate from the test code.
    Some people argue that tests shouldn't need descriptions—that
    we should instead give them long names that describe what they're doing—but
    we should support string-style explanations for those who want them.

1.  It doesn't discover tests on its own:
    we have to remember to register the test using `hope_that`,
    which means that sooner or later (probably sooner)
    some of our tests won't be run.

1.  We don't have a way to test things that are supposed to raise `AssertionError`.
    Putting assertions into code to check that it is behaving correctly
    is called [%g defensive_programming "defensive programming" %];
    it's a good practice,
    but we should make sure those assertions are failing when they're supposed to,
    just as we should test our smoke detectors every once in a while.

We can solve several of these problems at once by looking up test functions dynamically.
Python stores the variables and functions we define in a dictionary.
We can get that dictionary by calling the function `globals`:

[% inc pat="show_globals.*" fill="py out" %]

We can loop over the keys of this dictionary and find things with particular names:

[% inc file="show_tests.py" omit="sign" %]
[% inc file="show_tests.out" %]

which means we can find all the tests in a module,
call them,
and keep track of their results:
{: .continue}

[% inc pat="discovery.*" fill="py out" %]

This approach is less typing and less fragile than our first,
but we can improve it by showing the test function's [%g docstring "docstring" %]
if it has one.
Again,
functions are just objects,
which means they can have attributes.
If we give a function a docstring:

```
def example():
   "This is documentation."""
   pass
```

then `example.__doc__` contains the string `"This is documentation."`

We can do more than just print these strings when reporting problems:
we can embed instructions for the test framework in them.
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

We can do more than look up functions in a running program:
we can change them,
and doing this can make testing much easier.
For example,
if our test checks the time of day,
we can temporarily replace the real `time.time` function
with one that returns a fixed value.
Similarly,
if a test needs data from a database,
we can temporarily replace the function that gets the data
with one that returns a known, fixed dataset in a fraction of the time.

Temporary replacements like this are called [%g mock_object "mock objects" %]
because they mimic the essential behavior of the real objects in the program.
We usually use objects even if the thing we're replacing is a function,
and rely on the fact that Python lets us create objects that can be called just like functions:

[% inc pat="callable.*" fill="py out" %]

Let's create a class that:

1.  Defines a `__call__` method so that instances can be called like functions.
2.  Declares the parameters of that method to be `*args*` and `**kwargs`
    so that it can be called with any number of regular or keyword arguments.
3.  Stores those arguments so we can see how the replaced function was called.
4.  Returns either a fixed value or a value produced by a user-defined function.

The whole thing looks like this:

[% inc file="mock_object.py" keep="fake" %]

For convenience,
let's also define a function that replaces some function we've already defined
with an instance of our `Fake` class.
This function takes either a fixed value or another function as an argument
and passes those to `Fake`'s constructor:

[% inc file="mock_object.py" keep="fixit" %]

Next,
we'll define a function that adds two numbers
and write a test for it:

[% inc file="mock_object.py" keep="test_real" %]

But we can also use `fixit` to replace the real `adder` function
with a mock object that always returns 99
and check that it actually does:

[% inc file="mock_object.py" keep="test_fixed" %]

Another test proves that our `Fake` class records
all of the calls:

[% inc file="mock_object.py" keep="test_record" %]

And finally,
the user can provide a function to calculate a return value:

[% inc file="mock_object.py" keep="test_calc" %]

We can run all of these tests using the same "lookup and call" trick
we developed earlier,
but there's a problem.
Every test except the first one replaces `adder` with a mock object
but doesn't put `adder` back when it's done.
As a result,
any test that *doesn't* replace `adder` will run with
whatever mock object was last put in place:

[% inc file="mock_object.out" %]

We could fix this by asking users to remember to swap things back when they're done,
but people are forgetful.
Instead,
we can set up a [%g context_manager "context manager" %] that does this automatically.
A context manager is a class that defines two methods called `__enter__` and `__exit__`.
If the class is called `C`,
then when Python encounters a `with` block like this:

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
5.  When the block finishes, call `name.__exit__()`.

The last step is guaranteed to happen
even if an exception occurred inside the block,
so the context manager always has a chance to clean up after itself.
{: .continue}

Here's a mock object that inherits all the capabilities of `Fake`
and adds the two methods needed by `with`:

[% inc file="mock_context.py" keep="contextfake" %]

And here's a test to prove that it works:
{: .continue}

[% inc file="mock_context.py" keep="test" %]

## Exercises {: #tester-exercises}

### Literal strings {: .exercise}

If we have defined a variable with the test-skipping marker,
why can't we use that variable as the function's docstring like this:

```python
TEST_SKIP = "test:skip"


def test_sign_negative():
    TEST_SKIP
    assert sign(-3) == -1
```
