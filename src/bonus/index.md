---
status: "awaiting revision"
---

Each of the chapters in this book has been designed to fit into an hour (and a bit).
This appendix presents material that extends core ideas
but would bust that [%g attention_budget "attention budget" %].

## Using Function Attributes {: #bonus-attributes}

*This material extends [%x test %].*

Since functions are objects,
they can have attributes.
The function `dir` (short for "directory") returns a list of those attributes' names:

[% inc pat="func_dir.*" fill="py out" %]

Most programmers never need to use most of these,
but `__name__` holds the function's original name
and `__doc__` holds its [%i "docstring" %]:

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

## Lazy Evaluation {: #bonus-lazy}

*This material extends [%x interp %].*

One way to evaluate a design is to ask how [%i "extensibility" "extensible" %] it is.
The answer for our interpreter is now, "Pretty easily."
For example,
we can add a `comment` "operation" that does nothing and returns `None`
simply by writing `do_comment` function:

[% inc file="stmt.py" keep="comment" %]

An `if` statement is a bit more complex.
If its first argument is true it evaluates and returns its second argument
(the "if" branch).
Otherwise,
it evaluates and returns its second argument (the "else" branch):

[% inc file="stmt.py" keep="if" %]

As we said in [%x func %],
this is called [%i "lazy evaluation" %]
to distinguish it from the more usual [%i "eager evaluation" %]
that evaluates everything up front.
`do_if` only evaluates what it absolutely needs to;
most languages do this so that we can safely write things like:
{: .continue}

[% inc file="lazy.py" %]

If the language always evaluated both branches
then the code shown above would fail whenever `x` was zero,
even though it's supposed to handle that case.
In this case it might seem obvious what the language should do,
but most languages use lazy evaluation for `and` and `or` as well
so that expressions like:
{: .continue}

```python
thing and thing.part
```

will produce `None` if `thing` is `None`
and `reference.part` if it isn't.
{: .continue}

## Dynamic Loading {: #bonus-load}

*This material extends [%x template %].*

[% fixme "Explain how to load modules dynamically given a list of names." %]

## Extension {: #bonus-extension}

*This material extends [%x lint %].*

It's easy to check a single style rule by extending `NodeVisitor`,
but what if we want to check dozens of rules?
Traversing the AST dozens of times would be inefficient.
And what if we want people to be able to add their own rules?
Inheritance is the wrong tool for this:
if several people each create their own `NodeVisitor` with a `visit_Name` method,
we'd have to inherit from all those classes
and then have the new class's `visit_Name` call up to all of its parents' equivalent methods.

One way around this is to [%g method_injection "inject" %] methods into classes
after they have been defined.
The code fragment below creates a new class called `BlankNodeVisitor`
that doesn't add anything to `NodeVisitor`,
then uses `setattr` to add a method to it after it has been defined
([%f bonus-injection %]):

[% inc file="injection.py" keep="attach" %]

[% figure
   slug="bonus-injection"
   img="injection.svg"
   alt="Method injection"
   caption="Adding methods to classes after their definition."
%]

This trick works because classes and objects are just specialized dictionaries
(for some large value of "just").
If we create an object of `BlankNodeVisitor` and call its `visit` method:

[% inc file="injection.py" keep="main" %]

then the inherited `generic_visit` method does what it always does.
When it encounters a `Name` node,
it looks in the object for something called `visit_Name`.
Since it doesn't find anything,
it looks in the object's class for something with that name,
finds our injected method,
and calls it.

With a bit more work we could have our injected method save and then call
whatever `visit_Name` method was there when it was added to the class,
but we would quickly run into a problem.
As we've seen in earlier examples,
the methods that handle nodes are responsible for deciding
whether and when to recurse into those nodes' children.
If we pile method on top of one another,
then either each one is going to trigger recursion
(so we recurse many times)
or there will have to be some way for each one to signal
whether it did that
so that other methods don't.

To avoid this complication,
most systems use a different approach.
Consider this class:

[% inc file="register.py" keep="class" %]

The `add_handler` method takes three parameters:
the type of node a callback function is meant to handle,
the function itself,
and an optional extra piece of data to pass to the function
along with an AST node.
It saves the handler function and the data in a lookup table
indexed by the type of node the function is meant to handle.
Each of the methods inherited from `NodeVisitor`
then looks up handlers for its node type and runs them.

So what do handlers look like?
Each one is a function that takes a node and some data as input
and does whatever it's supposed to do:

[% inc file="register.py" keep="handler" %]

Setting up the visitor is a bit more complicated,
since we have to create and [%i "register (in code)" "register" %] the handler:

[% inc file="register.py" keep="main" %]

However,
we can now register as many handlers as we want
for each kind of node.
{: .continue}

## Tracing Inheritance {: #bonus-inheritance}

*This material extends [%x lint %].*

For our last example of finding things,
let's build a tool that tells us which methods are defined in which classes.
(We used a tool like this when writing this book
to keep track of examples that evolved step by step.)
Here's a test file that defines four classes,
each of which defines or redefines some methods:

[% inc file="inheritance_example.py" %]

As before,
our class's constructor creates a stack to keep track of where we are.
It also creates a couple of dictionaries to keep track of
how classes inherit from each other
and the methods each class defines:

[% inc file="inheritance.py" keep="init" %]

When we encounter a new class definition,
we push its name on the stack,
record its parents,
and create an empty set to hold its methods:

[% inc file="inheritance.py" keep="classdef" %]

When we encounter a function definition,
the first thing we do is check the stack.
If it's empty,
we're looking at a top-level function rather than a method,
so there's nothing for us to do.
(We actually should recurse through the function's children,
since it's possible to define classes inside functions,
but we'll leave as an exercise.)
If this function definition is inside a class,
on the other hand,
we add its name to our records:

[% inc file="inheritance.py" keep="methoddef" %]

Once we're done searching the AST we print out a table
of the classes and methods we've seen ([%t linter-inheritance %]).
We could make this display easier to read—for example,
we could sort the classes from parent to child
and display methods in the order in which they were first defined—but
none of that requires us to inspect the AST.

<div class="table" id="linter-inheritance" caption="Inheritance and methods" markdown="1">
| | GrandChild | LeftChild | Parent | RightChild |
| --- | --- | --- | --- | --- |
| blue | X | X |   | X
| green |   | X | X |
| orange | X |   |   |
| red | X |   | X | X
</div>

## Inspecting Functions {: #bonus-inspect}

*This material extends [%x perf %].*

A better implementation of filtering would make use of the fact that
Python's [`inspect`][py_inspect] module lets us examine objects in memory.
In particular, `inspect.signature` can tell us what parameters a function takes:

[% inc pat="inspect_func.*" fill="py out" %]

If, for example,
the user wants to compare the `red` and `blue` columns of a dataframe,
they can give us a function that has two parameters called `red` and `blue`.
We can then use those parameter names to figure out
which columns we need from the dataframe.
We will explore this in the exercises.
{: .continue}

## User-Defined Classes {: #bonus-extend}

*This material extends [%x persist %].*

It's time to extend our framework to handle user-defined classes.
We'll start by refactoring our code so that the `save` method doesn't get any larger:

[% inc file="extend.py" keep="save_base" omit="omit_extension" %]

The method to handle built-in types is:
{: .continue}

[% inc file="extend.py" keep="save_builtin" %]

and the one that handles aliases is:
{: .continue}

[% inc file="extend.py" keep="save_aliased" %]

None of this code is new:
we've just moved things into methods
to make each piece easier to understand.
{: .continue}

So how does a class indicate that it can be saved and loaded by our framework?
Our options are:

1.  Require it to inherit from a [%i "base class" %] that we provide
    so that we can use `isinstance` to check if an object is persistable.
    This approach is used in strictly-typed languages like Java,
    but method #2 below is considered more [%g pythonic "Pythonic" %].

2.  Require it to implement a method with a specific name and signature
    without deriving from a particular base class.
    This approach is called [%g duck_typing "duck typing" %]:
    if it walks like a duck and quacks like a duck, it's a duck.
    Since option #1 would require users to write this method anyway,
    it's the one we'll choose.

3.  Require users to [%i "register (in code)" "register" %]
    a [%g helper_class "helper class" %]
    that knows how to save and load objects of the class we're interested in.
    This approach is also commonly used in strictly-typed languages
    as a way of adding persistence after the fact
    without disrupting the class hierarchy;
    we'll explore it in the exercises.

To implement option #2,
we specify that if a class has a method called `to_dict`,
we'll call that to get its contents as a dictionary
and then persist the dictionary.
Before doing that,
though,
we will save a line indicating that
this dictionary should be used to reconstruct an object
of a particular class:

[% inc file="extend.py" keep="save_extension" %]

Loading user-defined classes requires more work
because we have to map class names back to actual classes.
(We could also use [%i "introspection" %]
to find *all* the classes in the program
and build a lookup table of the ones with the right method;
we'll explore that in the exercises.)
We start by modifying the loader's constructor
to take zero or more extension classes as arguments
and then build a name-to-class lookup table from them:

[% inc file="extend.py" keep="load_constructor" %]

The `load` method then looks for aliases,
built-in types,
and extensions in that order.
Instead of using a chain of `if` statements
we loop over the methods that handle these cases.
If a method decides that it can handle the incoming data
it returns a result;
if it can't,
it raises a `KeyError` exception,
and if none of the methods handle a case
we fail:

[% inc file="extend.py" keep="load_load" %]

The code to handle built-ins and aliases is copied from our previous work
and modified to raise `KeyError`:

[% inc file="extend.py" keep="inherited" %]

The method that handles extensions
checks that the value on the line just read indicates an extension,
then reads the dictionary containing the object's contents
from the input stream
and uses it to build an [%i "instance" %] of the right class:

[% inc file="extend.py" keep="load_extension" %]

Here's a class that defines the required method:

[% inc file="user_classes.py" keep="parent" %]

and here's a test to make sure everything works:

[% inc file="test_extend.py" keep="test_parent" %]

<div class="callout" markdown="1">

### What's in a Name?

The first version of these classes used the word `"extension"`
rather than `"@extension"`.
That led to the most confusing bug in this whole chapter.
When `load` reads a line,
it runs `self._builtin` before running `self._extension`.
If the first word on the line is `"extension"` (without the `@`)
then `self._builtin` constructs the method name `_extension`,
finds that method,
and calls it
as if we were loading an object of a built-in type:
which we're not.
Using `@extension` as the leading indicator
leads to `self._builtin` checking for `"_@extension"` in the loader's attributes,
which doesn't exist,
so everything goes as it should.

</div>

## Big and Little Endian {: #bonus-endian}

This is called [%g little_endian "little-endian" %] and is used by all Intel processors.
Some other processors put the most significant byte first,
which is called [%g big_endian "big-endian" %].
There are pro's and con's to both, which we won't go into here.
What you *do* need to know is that if you move data from one architecture to another,
it's your responsibility to flip the bytes around,
because the machine doesn't know what the bytes mean.
This is such a pain that the `struct` module and other libraries like it 
will do things for you if you ask it to.
If you're using `struct`,
the first character of a format string optionally indicates the byte order
([%t bonus-endian-formats %]).

<div class="table" id="bonus-endian-formats" caption="`struct` package endian indicators" markdown="1">
| Character | Byte order | Size     | Alignment     |
| --------- | ---------- | -------- | ------------- |
| `@`       | native     | native   | native        |
| `=`       | native     | standard | none          |
| `<`       | little     | endian   | standard none |
| `>`       | big        | endian   | standard none |
| `!`       | network    | standard | none          |
</div>

## Floating Point Numbers {: #bonus-float}

*This material extends [%x binary %].*

The rules for floating point numbers make Unicode look simple.
The root of the problem is that
we cannot represent an infinite number of real values
with a finite set of bit patterns.
And no matter what values we represent,
there will be an infinite number of values between each of them that we can't.

<div class="callout" markdown="1">

### Go To the Source

The explanation that follows is simplified to keep it manageable;
please read [%b Goldberg1991 %] for more detail.

</div>

Floating point numbers are represented by a sign,
a [%g mantissa "mantissa" %],
and an [%g exponent "exponent" %].
In a 32-bit [%i "word (of memory)" "word" %]
the [%i "IEEE 754 standard" "IEEE 754" %] standard calls for 1 bit of sign,
23 bits for the mantissa,
and 8 bits for the exponent.
We will illustrate how it works using a much smaller representation:
no sign,
3 bits for the mantissa,
and 2 for the exponent.
[%f bonus-floating-point %] shows the values this scheme can represent.

[% figure
   slug="bonus-floating-point"
   img="floating_point.svg"
   alt="Representing floating point numbers"
   caption="Representing floating point numbers."
%]

The IEEE standard avoids the redundancy in this representation by shifting things around.
Even with that,
though,
formats like this can't represent a lot of values:
for example,
ours can store 8 and 10 but not 9.
This is exactly like the problem hand calculators have
with fractions like 1/3:
in decimal, we have to round that to 0.3333 or 0.3334.

But if this scheme has no representation for 9
then \\( 8+1 \\) must be stored as either 8 or 10.
What should \\( 8+1+1 \\) be?
If we add from the left,
\\( (8+1)+1 \\( is \\( 8+1 \\) is 8,
but if we add from the right,
\\( 8+(1+1) \\) is \\( 8+2 \\) is 10.
Changing the order of operations makes the difference between right and wrong.

The authors of numerical libraries spend a lot of time worrying about things like this.
In this case
sorting the values and adding them from smallest to largest
gives the best chance of getting the best possible answer.
In other situations,
like inverting a matrix, the rules are much more complicated.

Another observation about our number line is that
while the values are unevenly spaced,
the *relative* spacing between each set of values stays the same:
the first group is separated by 1,
then the separation becomes 2,
then 4,
and so on.
This observation leads to a couple of useful definitions:

-   The [%g absolute_error "absolute error" %] in an approximation
    is the absolute value of the difference
    between the approximation and the actual value.

-   The [%g relative_error "relative error" %]
    is the ratio of the absolute error
    to the absolute value we're approximating.

For example,
being off by 1 in approximating 8+1 and 56+1 is the same absolute error,
but the relative error is larger in the first case than in the second.
Relative error is almost always more useful than absolute:
it makes little sense to say that we're off by a hundredth
when the value in question is a billionth.

One implication of this is that
we should never compare floating point numbers with `==` or `!=`
because two numbers calculated in different ways
will probably not have exactly the same bits.
It's safe to use `<`, `>=`, and other orderings,
though,
since they don't depend on being the same down to the last bit.

If we do want to compare floating point numbers
we can use something like [the `approx` class][pytest_approx] from [pytest][pytest]
which checks whether two numbers are within some tolerance of each other.
A completely different approach is to use something like
the [`fractions`][py_fractions] module,
which (as its name suggests) uses numerators and denominators
to avoid some precision issues.
[This post][textualize_fraction] describes one clever use of the module.

## Generating Test Cases {: #bonus-theorem}

Theorem provers like Z3 and [PicoSAT][picosat]
are far more powerful than most programmers realize.
Borrowing an example from [Andreas Zeller's][zeller_andreas],
we can use theorem provers to generate test cases.
Suppose we have a function that classifies triangles as equilateral,
scalene,
or isosceles.
We can set up some integer variables:

[% inc file="equilateral.py" keep="setup" %]

and then ask it to create an equilateral triangle
based solely on the definition:
{: .continue}

[% inc file="equilateral.py" keep="equilateral" %]
[% inc file="equilateral.out" %]

The same technique can generate a test case for scalene triangles:

[% inc file="scalene.py" keep="scalene" %]
[% inc file="scalene.out" %]

and isosceles triangles:
{: .continue}

[% inc file="isosceles.py" keep="isosceles" %]
[% inc file="isosceles.out" %]

## Exercises {: #bonus-exercises}

### Roundoff {: .exercise}

1.  Write a program that loops over the integers from 1 to 9
    and uses them to create the values 0.9, 0.09, and so on.
1.  Calculate the same values by subtracting 0.1 from 1,
    then subtracting 0.01,
    and so on.
1.  Calculate the absolute and relative differences between corresponding values
    (which should be identical).
1.  Repeat the exercise using the `Fraction` class
    from the [`fractions`][py_fractions] module.

### Fallback {: .exercise}

1.  Modify `LoadExtend` so that
    if the user didn't provide the class needed to reconstruct some archived data,
    the `load` method returns a simple dictionary instead.

1.  Why is this a bad idea?

### Removing Exceptions {: .exercise}

Rewrite `LoadExtend` so that it doesn't use exceptions
when `_aliased`, `_builtin`, and `extension` decide
they aren't the right method to handle a particular case.
Is the result simpler or more complex than the exception-based approach?

### Helper Classes {: .exercise}

Modify the framework so that
if a user wants to save and load instances of a class `X`,
they must register a class `Persist_X` with the framework
that does the saving and loading for `X`.

### Self-Referential Objects {: .exercise}

Suppose an object contains a reference to itself:

```python
class Example:
    def __init__(self):
        self.ref = None

ex = Example()
ex.ref = ex
```

1.  Why can't `SaveExtend` and `LoadExtend` handle this correctly?

1.  How would they have to be changed to handle this?
