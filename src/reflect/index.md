---
syllabus:
-   Temporarily replacing functions with mock objects can simplify testing.
-   Python defines protocols so that users' code can be triggered by keywords in the language.
-   We can use decorators to wrap functions after defining them.
-   Defining a decorator that has parameters is much more complicated
    than defining one that doesn't.
depends:
-   func
-   oop
---

This book is supposed to teach software design
by implementing small versions of real-world tools,
but we have reached a point where we have to learn a little more about Python
in order to proceed.
The same thing happened in [%b Wilson2022b %],
which had to explain how [%g promise "promises" %] work
to make later examples approachable;
as in that book,
the explanations below refer back to what we've already seen
about how languages themselves work.

## Mock Objects {: #reflect-mock}

[%x func %] showed that functions are bound to names
just like other values are bound to other variables.
We can use this fact to change functions at runtime to make testing easier.
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
([%f reflect-timeline %]):

[% inc file="mock_object.py" keep="test_fixed" %]

[% figure
   slug="reflect-timeline"
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

## Protocols {: #reflect-protocols}

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

## Decorators {: #reflect-decorator}

Python programs rely on several other protocols,
each of which gives user-level code a way to interact with
some aspect of the Python [%i "interpreter" %][%/i%].
One of the most widely used is called a [%g decorator "decorator" %],
which allows us to wrap one function with another.

In order to understand how decorators work,
we must take another look at [%i "closure" %]closures[%/i%],
which were introduced in [%x func %].
Suppose we want to create a function called `logging`
that prints a message before and after
each call to some other arbitrary function.
We could try to do it like this:

[% inc file="wrap_infinite.py" %]

but when we try to call `original` we wind up in an infinite loop.
The wrapped version of our function refers to `original`,
but Python looks that up at the time of call,
which means it calls the wrapped function instead
([%f reflect-bad-wrapping %]).

[% figure
   slug="reflect-bad-wrapping"
   img="bad_wrapping.svg"
   alt="The wrong way to wrap a function"
   caption="Accidentally creating infinite recursion when wrapping a function."
%]

We can solve the problem of infinite recursion by creating a closure:

[% inc pat="wrap_capture.*" fill="py out" %]

Doing this also gives us a way to pass extra arguments
when we create the wrapped function:

[% inc pat="wrap_param.*" fill="py out" %]

Wrapping functions like this is so useful
that Python has built-in support for doing it.
We define the decorator function that does the wrapping as before,
but then use `@wrap` to apply it
rather than `name = wrap(name)`:

[% inc pat="decorator_simple.*" fill="py out" %]

If we want to pass parameters at the time we apply the decorator,
though,
it seems like we're stuck,
because a Python decorator must take exactly one argument,
which must be the function we want to decorate.

If we want to pass extra parameters,
we need to call a function that returns a function of one parameter
that we can then use as a decorator.
This means that we need to define a function inside a function *inside another function*
to create a closure that captures the parameters:

[% inc pat="decorator_param.*" fill="py out" %]

<div class="callout" markdown="1">

### Design Flaw

Decorators didn't need to be this complicated.
In order to define a method that takes \\( N \\) parameters in Python,
we have to write a function of \\( N+1 \\) parameters,
the first of which represents the object for which the method is being called.
Python could have done the same thing with decorators,
i.e.,
allowed people to define a function of \\( N+1 \\) parameters
and have `@` fill in the first automatically:

[% inc file="alternative_design.py" %]

But this isn't the path Python took,
and as a result,
decorators are much harder to learn and use than they could have been.

</div>

## Iterators {: #reflect-iterator}

As a last example of how protocols work,
consider the `for` loop.
A statement like `for thing in collection`
assigns each item in `collection` to the variable `thing` one at a time,
possibly in a predetermined order.
Python implements this using a two-part [%g iterator "iterator" %] protocol:

1.  If an object has an `__iter__` method,
    that method is called to create an iterator object.

2.  That iterator object must have a `__next__` method,
    which must return a value each time it is called.
    When there are no more values to return,
    it must raise a `StopIteration` exception.

For example,
suppose we have a class that stores a list of strings
and we want to return the characters from the strings in order.
(We will use a [%i "buffer" %][%/i%] class like this
to store text for viewing in [%x viewer %].)
In our first attempt,
each object is its own iterator,
i.e.,
each object keeps track of what value to return next when looping:

[% inc file="naive_iterator.py" keep="body" %]

The `advance` method moves the column marker forward within the current row,
advancing the row and resetting the column to 0 when it reaches
the end of the current line:

[% inc file="naive_iterator.py" keep="advance" %]

Our first test seems to work:

[% inc file="test_naive_iterator.py" keep="success" %]

However,
our iterator doesn't work if the buffer contains an empty string:
{: .continue}

[% inc file="test_naive_iterator.py" keep="failure" %]

It also fails when we use a nested loop:
{: .continue}

[% inc file="test_naive_iterator.py" keep="nested" %]

We can fix the first problem with more careful bookkeeping—we leave that
as an exercise—but
fixing the second problem requires us to re-think our design.
The problem is that we only have one pair of variables
(the `_row` and `_col` attributes of the buffer)
to store the current location,
but two loops trying to use them.
What we need to do instead is
create a separate object for each loop to use:

[% inc file="better_iterator.py" keep="buffer" %]

Each [%i "cursor" %][%/i%] keeps track of the current location
for a single loop
using code identical to what we've already seen
(including the same bug with empty strings):

[% inc file="better_iterator.py" keep="cursor" omit="advance" %]

With this change in place,
our test of nested loops pass.
{: .continue}

## Summary {: #reflect-summary}

[% figure
   slug="reflect-concept-map"
   img="concept_map.svg"
   alt="Concept map of mocks, protocols, and iterators"
   caption="Concept map"
%]

## Exercises {: #reflect-exercises}

### Timing Blocks {: .exercise}

Create a context manager called `Timer` that reports how long it has been
since a block of code started running:

```python
# your class goes here

with Timer() as start:
    # …do some lengthy operation…
    print(start.elapsed())  # time since the start of the block
```

### Handling Empty Strings {: .exercise}

Modify the iterator example so that it handles empty strings correctly,
i.e.,
so that iterating over the list `["a", ""]` produces `["a"]`.
