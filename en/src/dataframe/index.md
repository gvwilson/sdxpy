---
title: "A Dataframe"
syllabus:
- Create abstract base classes to specify interfaces.
- Store two-dimensional data as rows or as columns.
- Use reflection to match data to function parameters.
- Measure performance to evaluate engineering tradeoffs.
---

Whether your tool of choice is Python, R, SQL, or Excel,
you're almost certainly doing data science on tables
with named columns that have the same type of value in every row.
To explore how they work,
we build two implementations of dataframes in Python:
one that stores values in columns,
the other that stores them in rows.
And to explain how to choose between them,
we measure their performance.

## Storing Columns {: #dataframe-cols}

We start by creating an [%g abstract_class "abstract class" %]
that defines the methods our two dataframe classes will support.
This class (unimaginatively called `DF`)
requires [%g concrete_class "concrete classes" %] to implement eight methods:

-   `ncol`: report the number of columns.
-   `nrow`: report the number of rows.
-   `cols`: return the set of column names.
-   `eq`: check whether this dataframe is equal to another.
-   `get`: get a scalar value from a specified column and row.
-   `set`: set the scalar value in a specified column and row.
-   `select`: create a new dataframe containing some or all of the original's columns.
-   `filter`: create a new dataframe containing some or all of the original's rows.

[% inc file="df_base.py" %]

<div class="callout" markdown="1">

### Docstrings are enough

[% fixme "method needs body but docstring is enough" %]

</div>

We then derive a class `DfCol` that uses [%g column_wise "column-wise" %] storage.
Each column is stored as a list of values,
all of which are of the same type.
The dataframe is a dictionary of such lists,
all of which have the same length:

[% inc file="df_col.py" keep="top" %]

Some methods are almost trivial to implement on top of this storage mechanism;
others are more difficult.
Three of the easy ones return the number of rows and columns
and the names of the columns:

[% inc file="df_col.py" keep="simple" %]

[% fixme "why pop" %]

Testing for equality is also relatively simple.
Two dataframes are the same if they have exactly the same columns
and the same values in every column:

[% inc file="df_col.py" keep="eq" %]

Notice that we use `other.cols()` and `other.get()`
rather than reaching into the other dataframe.
We defined the abstract base class because
we expect to implement dataframes in several different ways.
Those other ways will probably not use the same data structures,
so we can only rely on the interface defined in the base class.
{: .continue}

Getting individual values is straightforward:

[% inc file="df_col.py" keep="get" %]

Selecting a subset of columns is also straightforward:
{: .continue}

[% inc file="df_col.py" keep="select" %]

Notice,
though,
that the dataframe created by `select`
re-uses the columns of the original dataframe.
This is safe and efficient so long as columns are [%g immutable "immutable" %],
i.e.,
so long as their contents are never changed in place.
{: .continue}

Time to write some tests.
This one checks that we can construct a dataframe with some values:

[% inc file="test_df_col.py" keep="test_two_pairs" %]

while this one checks that `filter` works correctly:
{: .continue}

[% inc file="test_df_col.py" keep="test_filter" %]

## Storing Rows

Column-wise storage makes selecting columns easy but filtering rows hard.
If we expect to do more filtering than selecting
it might be more efficient to use [%g row_wise "row-wise" %] storage.
The class `DfRow` is derived from the same abstract base class `DF` as `DfCol`,
so it has to have the same interface.
However,
it stores data as a single list of dictionaries,
each with the same keys and the same types of values:

[% inc file="df_row.py" keep="top" %]

Notice that `DfRow`'s constructor *doesn't* have the same signature as `DfCol`.
At some point in our code we have to decide which of the two classes to construct.
If we design our code well that decision will be made in exactly one place
and everything else will rely solely on the common interface defined by `DF`.
But since we have to type something different at the point of construction,
it's OK for the constructors to be different.
{: .continue}

The basic operations `ncol`, `nrow`, and `cols` are straightforward:

[% inc file="df_row.py" keep="simple" %]

Whenever we need information about columns,
we look at the first row.
The assumption that there *is* a first row means we can't represent
an empty dataframe;
we'll explore this in the exercises.
{: .continue}

Getting values and checking for equality are also straightforward.
(See the source code for their implementation.)
Selecting and filtering are more interesting,
since they are the whole point of this implementation.
To select columns we must build a new list of dictionaries,
each of which has only some of the keys of the original:

[% inc file="df_row.py" keep="select" %]

To filter,
we simply pass each row to the user-supplied filter function:
{: .continue}

[% inc file="df_row.py" keep="filter" %]

These operations are the inverses of their `DfCol` counterparts:
we have to rearrange data to select
but can use the existing data as-is to filter
rather than vice versa.

Since `DfCol` and `DfRow` have the same interface,
we can recycle the tests we wrote for the former.
We obviously need to change the objects we construct,
so let's use this opportunity to write helper functions
to create the dataframes we use in multiple tests:

[% inc file="test_df_row.py" keep="fixture" %]

Creating fixtures in functions is so common
that [pytest][pytest] has built-in support for it;
we will explore this in the exercises.
With these functions in hand our tests look like:

[% inc file="test_df_row.py" keep="test_two_pairs" %]

## Performance {: #dataframe-performance}

So how do our two classes perform?
To find out,
let's write a short program to create dataframes of each kind
and then time how long it takes to select their columns and filter their rows.
To keep things simple
we will create dataframes whose columns are called `label_1`, `label_2`, and so on,
and whose values are all integers in the range 0–9.
A thorough set of [%g benchmark "benchmarks" %] would create columns of other kinds as well,
but this is enough to illustrate the technique.

[% inc file="timing.py" keep="create" %]

To time filtering,
we arbitrarily decide that we will keep rows an even value in the first column.
Again,
if we were doing this for real
we would look at some actual programs
to see what fraction of rows filtering usually kept,
and then model that.

[% inc file="timing.py" keep="filter" %]

Notice that `time_filter` doesn't know or care
whether it's being given a `DfCol` or a `DfRow`.
That's the whole point of deriving them from a base class:
we can use them interchangeably.
{: .continue}

Timing `select` is similar to timing `filter`.
Again,
we make an arbitrary decision about how many columns to keep
(in this case one third):

[% inc file="timing.py" keep="select" %]

Finally,
we write a function that takes a list of strings like `3x3` or `100x20`,
creates a dataframe of each kind and of each size,
times operations,
and reports the results:

[% inc file="timing.py" keep="sweep" %]

The results are shown in [%t dataframe-timing %].
For a 1000 by 1000 dataframe
selection is over 250 times faster with column-wise storage than with row-wise,
while filtering is 1.8 times slower.
[% fixme "do the math" %]

<div class="table" id="dataframe-timing" caption="Dataframe timings" markdown="1">
| nrow  | ncol  | filter col | select col | filter row | select row |
| ----- | ----- | ---------- | ---------- | ---------- | ---------- |
|    10 |    10 | 8.87e-05   | 7.70e-05   | 4.41e-05   | 2.50e-05   |
|   100 |   100 | 0.00275    | 4.10e-05   | 0.00140    | 8.76e      |
|  1000 |  1000 | 0.146      | 0.000189   | 0.0787     | 0.0508     |
| 10000 | 10000 | 19.0       | 0.00234    | 9.97       | 5.57       |
</div>

We can get much more insight using Python [cProfile][py_cprofile] module:

[% inc pat="profile.*" fill="sh out" %]

Ignoring the first two lines (which are the output of our program),
the table tells us:

-   the number of times each function or method was called;

-   the total time spent in those calls (which is what we care about most);

-   the time spent per call; and

-   the cumulative time spent in that call and all the things it calls,
    both per call and in total.

Right away we can see that the `dict_match` function
that checks the consistency of the rows in a row-oriented dataframe
is eating up a lot of time.
It's only called in the constructor,
but on the other hand,
we're constructing a new dataframe for each `filter` and `select`,
so removing that check would actually speed things up.

Looking down a little further,
the dictionary comprehension in `DfCol.filter` takes a lot of time as well.
That isn't surprising:
we're copying the values out of the columns into a temporary dictionary
for every row when we filter,
and building all those temporary dictionaries adds up to a lot of time.

<div class="callout" markdown="1">

### Engineering

If science is the use of the experimental method to investigate the world,
engineering is the use of the experimental method
to investigate and improve the things that people build.
Good software designers collect and analyze data all the time
to find out whether one website design works better than another [% b Kohavi2020 %]
or to improve the performance of CPUs [% b Patterson2017 %].
A few simple experiments like these can save weeks or months of misguided effort.

</div>

[% fixme concept-map %]

## Exercises {: #dataframe-exercises}

### Empty dataframes {: .exercise}

An empty dataframe is as reasonable and as useful as an empty string or an empty list.
`DfCol` can represent this,
but `DfRow` cannot:
if the list of dictionaries is empty,
we cannot ask for columns' names.
Derive another dataframe class from `DF` that uses row-wise storage
but can represent a dataframe with no rows.

### Unified constructors {: .exercise}

Modify the constructors of `DfRow` and `DfCol` to have the same signatures.
Where and why might this be useful?

### Fixture functions {: .exercise}

Read the documentation for the `@fixture` decorator in [pytest][pytest]
and the modify the tests in this chapter to use it.

### Using arrays {: .exercise}

Derive another dataframe class from `DF`
that uses Python's [array][py_array] module for column-wise storage.
How does it performance compared to other implementations?

### Crossover {: .exercise}

1.  At what ratio of filters to selects are `DfRow` and `DfCol` equally fast?
    (Your answer may depend on the size of the dataframe.)

2.  How does the relative performance of the two classes change
    if tables have a fixed number of columns (such as 10 or 20)
    but an increasing numbers of rows?
    Is this scenario more realistic?

### Filtering by strings {: .exercise}

Modify the comparison of filter and select to work with tables
that contain columns of strings instead of columns of numbers
and see how that changes performance.
For testing,
creating random 4-letter strings using the characters A-Z
and then filter by:

-   an exact match,
-   strings starting with a specific character, and
-   strings that contain a specific character

### Join performance {: .exercise}

A join combines data from two tables based on matching keys.
For example,
if the two tables are:

| Key | Left |
| --- | ---- |
| A   | a1   |
| B   | b1   |
| C   | c1   |

and:
{: .continue}

| Key | Right |
| --- | ----- |
| A   | a2    |
| A   | a3    |
| B   | b2    |

then the join is:
{: .continue}

| Key | Left | Right |
| --- | ---- | ----- |
| A   | a1   | a2    |
| A   | a1   | a3    |
| B   | b1   | b2    |

Write a test to compare the performance of row-wise vs. column-wise storage
when joining two tables based on matching numeric keys.
Does the answer depend on the fraction of keys that match?


### Join optimization {: .exercise}

The simplest way to [%g join "join" %] two tables is
to look for matching keys using a double loop.
An alternative is to build an [%g index_database "index" %] for each table
and then use it to construct matches.
For example, suppose the tables are:

| Key | Left |
| --- | ---- |
| A   | a1   |
| B   | b1   |
| C   | c1   |

and:
{: .continue}

| Key | Right |
| --- | ----- |
| A   | a2    |
| A   | a3    |
| B   | b2    |

The first step is to create a `Map` showing where each key is found in the first table:

```js
{A: [0], B: [1], C: [2]}
```

The second step is to create a similar `Map` for the second table:
{: .continue}

```js
{A: [0, 1], B: [2]}
```

We can then loop over the keys in one of the maps,
look up values in the second map,
and construct all of the matches.
{: .continue}

Write a function that joins two tables this way.
Is it faster or slower than using a double loop?
How does the answer depend on the number of keys and the fraction that match?
