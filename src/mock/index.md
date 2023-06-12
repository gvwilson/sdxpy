---
syllabus:
-   Temporarily replacing functions with mock objects can simplify testing.
-   Python defines protocols so that users' code can be triggered by keywords in the language.
---

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
([%f mock-timeline %]):

[% inc file="mock_object.py" keep="test_fixed" %]

[% figure
   slug="mock-timeline"
   img="timeline.svg"
   alt="Timeline of mock operation"
   caption="Timeline of mock operation."
%]

Another test proves that our `Fake` class records
all of the calls:

[% inc file="mock_object.py" keep="test_record" %]

And finally,
the user can provide a function to calculate a return value:

[% inc file="mock_object.py" keep="test_calc" %]

## Protocols {: #mock-protocols}

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

## Exercises {: #mock-exercises}

### Timing blocks {: .exercise}

Create a context manager called `Timer` that reports how long it has been
since a block of code started running:

```python
# your class goes here

with Timer() as start:
    # …do some lengthy operation…
    print(start.elapsed())  # time since the start of the block
```
