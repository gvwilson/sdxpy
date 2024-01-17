---
abstract: >
    Every programming language has tools to collect tests, run them, and report their results.
    This chapter shows how such tools are built,
    both to help programmers use them more effectively,
    and to illustrate the single most important idea in this book:
    that programs are just another kind of data.
syllabus:
-   Functions are objects you can save in data structures or pass to other functions.
-   Python stores local and global variables in dictionary-like structures.
-   A unit test performs an operation on a fixture and passes, fails, or produces an error.
-   A program can use introspection to find functions and other objects at runtime.
depends:
---

Not all software needs rigorous testing:
for example,
it's OK to check a one-off data analysis script
by looking at the output of each stage as we add it.
But we should all be grateful that
98% of the lines of code in the [SQLite][sqlite] database
are there to make the other 2% always do the right thing.

The examples in this book lie somewhere between these two extremes.
Together,
they are over 7000 lines long;
to make sure they work correctly,
we wrote several hundred [%g unit_test "unit tests" %] using [pytest][pytest].
We used this framework because it makes tests easier to write,
and because it runs them in a reliable, repeatable way
[%b Meszaros2007 Aniche2022 %].
Understanding how tools like this work will help you use them more effectively,
and will reinforce one of the big ideas of this book:
programs are just another kind of data.

## Storing and Running Tests {: #test-funcobj}

[% figure
   slug="test-func-list"
   img="func_list.svg"
   alt="A list of functions"
   caption="A list of functions."
%]

As we said in [%x oop %],
a function is just an object
that we can assign to a variable.
We can also store them in lists just like numbers or strings
([%f test-func-list %]):

[% inc pat="func_list.*" fill="py out" %]

However,
we have to be able to call the functions in the same way
in order for this trick to work,
which means they must have the same [%i "signature" %]:
{: .continue}

[% inc pat="signature.*" fill="py out" %]

Now suppose we have a function we want to test:

[% inc file="manual.py" keep="sign" %]

and some functions that test it
(two of which contain deliberate errors):
{: .continue}

[% inc file="manual.py" keep="tests" %]

Each test does something to a [%g fixture "fixture" %]
(such as the number 19)
and uses [%g assertion "assertions" %]
to compare the [%g actual_result "actual result" %]
against the [%g expected_result "expected result" %].
The outcome of each test can be:

-   [%g pass_test "Pass" %]:
    the test subject works as expected.

-   [%g fail_test "Fail" %]:
    something is wrong with the test subject.

-   [%g error_test "Error" %]:
    something is wrong in the test itself,
    which means we don't know if
    the thing we're testing is working properly or not.

We can implement this classification scheme as follows:

1.  If a test function completes without [%g raise_exception "raising" %]
    any kind of [%g exception "exception" %],
    it passes.
    (We don't care if it returns something,
    but by convention tests don't return a value.)

2.  If the function raises an `AssertionError` exception,
    then the test has failed.
    Python's `assert` statement does this automatically
    when the condition it is checking is false,
    so almost all tests use `assert` for checks.

3.  If the function raises any other kind of exception,
    then we assume the test itself is broken
    and count it as an error.

Translating these rules into code gives us the function `run_tests`
that runs every test in a list
and counts how many outcomes of each kind it sees:

[% inc file="manual.py" keep="run" %]

We use `run_tests` by putting all of our test functions into a list
and passing that to the test runner:

[% inc file="manual.py" keep="use" %]

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

Let's run the Python interpreter and call the `globals` function.
To make its output easier to read,
we will [%g pretty_print "pretty-print" %] it
using Python's [`pprint`][py_pprint] module:

[% inc pat="globals.*" fill="py out" %]

As the output shows,
`globals` is a dictionary containing
all the variables in the program's [%g "global" global %] [%g scope "scope" %].
Since we just started the interpreter,
all we see are the variables that Python defines automatically.
(By convention,
Python uses double underscores for names that mean something special to it.)
{: .continue}

What happens when we define a variable of our own?

[% inc pat="globals_plus.*" fill="py out" %]

Sure enough,
`my_variable` is now in the dictionary.
{: .continue}

If function names are just variables
and a program's variables are stored in a dictionary,
we can loop over that dictionary
to find all the functions whose names start with `test_`:

[% inc file="find_test_funcs.py" keep="main" %]
[% inc file="find_test_funcs.out" %]

The [%i "hexadecimal" %] numbers in the output show
where each function object is stored in memory,
which isn't particularly useful unless we're extending the language,
but at least it doesn't take up much space on the screen.
{: .continue}

Having a running program find things in itself like this
is called [%i "introspection" %],
and is the key to many of the designs in upcoming chapters.
Combining introspection with the pass-fail-error pattern of the previous section
gives us something that finds test functions,
runs them,
and summarizes their results:

[% inc file="runner.py" keep="run" %]
[% inc file="runner.out" %]

We could add many more features to this
(and [pytest][pytest] does),
but almost every modern test runner uses this design.
{: .continue}

## Summary {: #test-summary}

When reviewing the ideas introduced in this chapter ([%f test-concept-map %]),
it's worth remembering [Clarke's Third Law][clarkes_laws],
which states that
any sufficiently advanced technology is indistinguishable from magic.
The same is true of programming tricks like introspection:
the code that finds tests dynamically seems transparent
to an expert who understands that code is data,
but can be incomprehensible to a novice.
As we said in the discussion of comprehension curves in [%x intro %],
no piece of software can be optimal for both audiences;
the only solution to this problem is education,
which is why books like this one exist.
Please see [%x bonus %] for extra material related to these ideas.

[% figure
   slug="test-concept-map"
   img="concept_map.svg"
   alt="Concept map of test runner"
   caption="Concept map."
   cls="here"
%]

## Exercises {: #test-exercises}

### Looping Over `globals` {: .exercise}

What happens if you run this code?

```python
for name in globals():
    print(name)
```

What happens if you run this code instead?
{: .continue}

```python
name = None
for name in globals():
    print(name)
```

Why are the two different?
{: .continue}

### Individual Results {: .exercise}

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.

2.  Write unit tests to check that your answer works correctly.

### Setup and Teardown {: .exercise}

Testing frameworks often allow programmers to specify a `setup` function
that is to be run before each test
and a corresponding `teardown` function
that is to be run after each test.
(`setup` usually recreates complicated test fixtures,
while `teardown` functions are sometimes needed to clean up after tests,
e.g., to close database connections or delete temporary files.)

Modify the testing tool in this chapter so that
if a file of tests contains a function called `setup`
then the tool calls it exactly once before running each test in the file.
Add a similar way to [%g register_code "register" %] a `teardown` function.

### Timing Tests {: .exercise}

Modify the testing tool so that it records how long it takes to run each test.
(The function `time.time` may be useful.)

### Selecting Tests {: .exercise}

Modify the testing tool so that if a user provides `-s pattern` or `--select pattern`
on the command line
then the tool only runs tests that contain the string `pattern` in their name.

### Finding Functions {: .exercise}

Python is [%g dynamic_typing "dynamically typed" %],
which means it checks the types of values as code runs.
We can do this ourselves using the `type` function,
which shows that 3 is an integer:

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

1.  Modify the test runner in this chapter so that
    it *doesn't* try to call things whose names start with `test_`
    but which aren't actually functions.

2.  Should the test runner report these cases as errors?

### Local Variables {: .exercise}

Python has a function called `locals`
that returns all the variables defined in the current [%g local "local" %] scope.

1.  Predict what the code below will print *before* running it.
    When does the variable `i` first appear
    and is it still there in the final line of output?

2.  Run the code and compare your prediction with its behavior.

[% inc file="locals.py" %]
