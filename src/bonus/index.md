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

## Lazy Evaluation {: #bonus-lazy}

*This material extends [%x interp %].*

One way to evaluate a design is to ask how [%g extensibility "extensible" %] it is.
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

This is called [%g lazy_evaluation "lazy evaluation" %]
to distinguish it from the more usual [%g eager_evaluation "eager evaluation" %]
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
In a 32-bit [%g word_memory "word" %]
the [%i "IEEE 754 standard" %]IEEE 754[%/i%] standard calls for 1 bit of sign,
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
then 8+1 must be stored as either 8 or 10.
What should 8+1+1 be?
If we add from the left,
(8+1)+1 is 8+1 is 8,
but if we add from the right,
8+(1+1) is 8+2 is 10.
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
the [fractions][py_fractions] module,
which (as its name suggests) uses numerators and denominators
to avoid some precision issues.
[This post][textualize_fraction] describes one clever use of the module.
