---
title: "A Dataframe"
syllabus:
-   Create abstract base classes to specify interfaces.
-   Store two-dimensional data as rows or as columns.
-   Use reflection to match data to function parameters.
-   Measure performance to evaluate engineering tradeoffs.
---

One of the drawbacks of publishing a book online is that
it gives you an excuse to obsess over analytics.
How many people visited the site today?
Which pages did they look at, and for how long?

Whether your analysis tool of choice is Python, R, SQL, or Excel,
you're almost certainly working with tables
with named columns that have the same type of value in every row.
Tables of this kind are called [%i "dataframe" %][%g dataframe "dataframes" %][%/i%],
and to explore how they work,
this chapter builds two implementations of them in Python:
one that stores values in columns,
the other that stores them in rows.
To help us decide which is better,
we'll compare their performance in a reproducible way.

## Storing Columns {: #dataframe-cols}

To start,
let's create an [%g abstract_class "abstract class" %]
that defines the methods our dataframe classes will support.
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

Every method in Python needs a body,
so many programmers will write `pass` (Python's "do nothing" statement).
However,
a [%i "docstring" %][%g docstring "docstring" %][%/i%] also counts as a body,
so if we write those (which we should)
there's no need to write `pass`.

</div>

We then derive a class `DfCol` that uses [%i "column-wise storage; storage!column-wise" %][%g column_wise "column-wise" %][%/i%] storage
([%f dataframe-colwise %]).
Each column is stored as a list of values,
all of which are of the same type.
The dataframe itself is a dictionary of such lists,
all of which have the same length
so that there are no holes in any of the rows:

[% inc file="df_col.py" keep="top" %]

[% figure
   slug="dataframe-colwise"
   img="dataframe_colwise.svg"
   alt="Column-wise storage"
   caption="Storing a dataframe's data in columns."
%]

Some methods are almost trivial to implement on top of this storage mechanism;
others are more difficult.
Three of the easy ones return the number of rows and columns
and the set of column names.
To get the number of rows
we check the length of an arbitrary column:

[% inc file="df_col.py" keep="simple" %]

Checking equality is also relatively simple.
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

and so is selecting a subset of columns:
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

Selecting columns was easy,
but filtering—i.e., selecting rows that pass some test—is not.
This is partly because the operation is intrinsically more complex:
we need to apply a user-defined function to each row
to see if we're supposed to keep it,
which is much more complicated than selecting a few columns by name
out of a dictionary.

However,
our storage mechanism makes the task more complex still.
Since values are stored in columns,
we have to extract the ones belonging to each row
to pass them into the user-defined function
([%f dataframe-col-to-row %]).
And if that wasn't enough,
we want to do this solely for the columns that the user's function needs.

[% figure
   slug="dataframe-col-to-row"
   img="dataframe_col_to_row.svg"
   alt="Packing column values into rows"
   caption="Extracting values from columns to create temporary rows."
%]

Our solution makes use of the fact that
Python's [inspect][py_inspect] module lets us examine objects in memory.
In particular, `inspect.signature` can tell us what parameters a function takes.
If, for example,
the user wants to compare the `red` and `blue` columns of a dataframe,
they can give us a function that has two parameters called `red` and `blue`.
We can then use those parameter names to figure out
which columns we need from the dataframe
([%f dataframe-inspect %]):

[% inc file="df_col.py" keep="filter" %]

Once we have build a temporary dictionary with the values in a row,
we pass that dictionary to the user's filter function using `**args`
to [%i "spreading (arguments)" %][%g spread "spread" %][%/i%] them,
i.e.,
to match them by name to the function's parameters.
{: .continue}

[% figure
   slug="dataframe-inspect"
   img="dataframe_inspect.svg"
   alt="Using inspection to identify columns"
   caption="Using runtime inspection of parameter names to select columns."
%]

<div class="callout" markdown="1">

### Would simpler be better?

Packing values and matching them to the parameters of the user's function
makes the code complex,
and probably slows filtering down.
We could instead just pass in the columns and the row index,
and require the user to refer to (for example) `red[i]` in their function
instead of just `red`.
However,
this would make those filtering functions a little harder to write,
and we'd have to trust the user to stick to our conventions
and only use element `i` of each row when filtering.
We will explore these tradeoffs in the exercises.

</div>

Time to write some tests.
This one checks that we can construct a dataframe with some values:

[% inc file="test_df_col.py" keep="test_two_pairs" %]

while this one checks that `filter` works correctly:
{: .continue}

[% inc file="test_df_col.py" keep="test_filter" %]

## Storing Rows

Column-wise storage makes selecting columns easy but filtering rows hard.
If we expect to do more filtering than selecting
it might be more efficient to use [%i "row-wise storage; storage!row-wise" %][%g row_wise "row-wise" %][%/i%] storage
([%f dataframe-rowwise %]).

[% figure
   slug="dataframe-rowwise"
   img="dataframe_rowwise.svg"
   alt="Row-wise storage"
   caption="Storing a dataframe's data in rows."
%]

The class `DfRow` is derived from the same abstract base class as `DfCol`
so that it has the same interface.
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
Filtering is much easier than it was with column-wise storage—we
simply pass each row to the user-supplied filter function
and keep the ones that pass:
{: .continue}

[% inc file="df_row.py" keep="select" %]

To select columns we must build a new list of dictionaries,
each of which has only some of the keys of the original:

[% inc file="df_row.py" keep="select" %]

These operations are the inverses of their `DfCol` counterparts:
we have to rearrange data to select
but can use the existing data as-is to filter.
{: .continue}

Since `DfCol` and `DfRow` have the same interface,
we can recycle the tests we wrote for the former.
We obviously need to change the objects we construct,
so let's use this opportunity to write helper functions
to create the dataframes we use in multiple tests:

[% inc file="test_df_row.py" keep="fixture" %]

With these functions in hand our tests look like:
{: .continue}

[% inc file="test_df_row.py" keep="test_two_pairs" %]

## Performance {: #dataframe-performance}

Our two implementations of dataframes have identical interfaces,
so how can we choose which to use?
Performance is one consideration,
particularly if we're expecting to work with large datasets.

<div class="callout" markdown="1">

### Transactions versus analysis

Regardless of data volumes,
different storage schemes are better (or worse) for different kinds of work.
[%i "online transaction processing (OLTP); OLTP (online transaction processing)" %][%g oltp "Online transaction processing" %][%/i%] (OLTP)
refers to adding or querying individual records,
such as online sales.
[%i "online analytical processing (OLAP); OLAP (online analytical processing)" %][%g olap "online analytical processing" %][%/i%] (OLAP),
on the other hand,
processes selected columns of a table in bulk to do things like find averages over time.
Row-wise storage is usually best for OLTP,
but column-wise storage is better suited for OLAP.
If data volumes are large,
[%i "data engineer" %][%g "data_engineer" "data engineers" %][%/i%] will sometimes run two databases in parallel,
using [%i "batch processing" %][%g batch_processing "batch processing" %][%/i%] jobs
to copy new or updated records from the OLTP databases over to the OLAP database.

</div>

To compare the speed of these classes,
let's write a short program to create dataframes of each kind
and time how long it takes to select their columns and filter their rows.
To keep things simple
we will create dataframes whose columns are called `label_1`, `label_2`, and so on,
and whose values are all integers in the range 0–9.
A thorough set of [%i "benchmarking" %][%g benchmark "benchmarks" %][%/i%]
would create columns of other kinds as well,
but this is enough to illustrate the technique.

[% inc file="timing.py" keep="create" %]

To time filtering,
we arbitrarily decide that we will keep rows with an even value in the first column:

[% inc file="timing.py" keep="filter" %]

Again,
if we were doing this for real
we would look at some actual programs
to see what fraction of rows filtering usually kept,
and simulate that.
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
creates dataframes of each size,
times operations,
and reports the results:

[% inc file="timing.py" keep="sweep" %]

This function is called `sweep` because
executing code multiple times with different parameters to measure performance
is called [%i "parameter sweeping" %][%g parameter_sweeping "parameter sweeping" %][%/i%].
{: .continue}

The results are shown in [%t dataframe-timing %].
For a 1000 by 1000 dataframe
selection is over 250 times faster with column-wise storage than with row-wise,
while filtering is 1.8 times slower.

<div class="table" id="dataframe-timing" caption="Dataframe timings" markdown="1">
| nrow  | ncol  | filter col | select col | filter row | select row |
| ----- | ----- | ---------- | ---------- | ---------- | ---------- |
|    10 |    10 | 8.87e-05   | 7.70e-05   | 4.41e-05   | 2.50e-05   |
|   100 |   100 | 0.00275    | 4.10e-05   | 0.00140    | 8.76e      |
|  1000 |  1000 | 0.146      | 0.000189   | 0.0787     | 0.0508     |
| 10000 | 10000 | 19.0       | 0.00234    | 9.97       | 5.57       |
</div>

We can get much more insight using Python [cProfile][py_cprofile] module,
which runs a program for us,
collects detailed information on how long functions ran,
and reports the result:

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
so removing that safety check would speed things up.

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

## Summary {: #dataframe-summary}

[% figure
   slug="dataframe-concept-map"
   img="dataframe_concept_map.svg"
   alt="Concept map for dataframes"
   caption="Concepts for dataframes."
%]

## Exercises {: #dataframe-exercises}

### More efficient filtering {: .exercise}

Derive a class from `DfCol` and override its `filter` method
so that the user-defined filtering functions take zero or more columns
and an row index called `i_row` as parameters
and return `True` or `False` to signal whether the row passes the test.

1.  How much faster does this make filtering?

2.  When would it be useful for filtering functions
    to take no column at all as parameters?

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
and modify the tests in this chapter to use it.

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

### Conversion {: .exercise}

Write a function to convert a `DfRow` into a `DfCol`
and another to do the opposite.
Which one is faster?
How does the difference in performance depend on
the size and shape of the dataframes being converted?

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
