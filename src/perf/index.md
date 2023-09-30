---
syllabus:
-   Create abstract classes to specify interfaces.
-   Store two-dimensional data as rows or as columns.
-   Use reflection to match data to function parameters.
-   Measure performance to evaluate engineering tradeoffs.
depends:
-   reflect
---

One peril of publishing a book online is obsessing over analytics.
How many people visited the site today?
Which pages did they look at, and for how long?
Whether we use [%i "Excel" %], [%i "SQL" %], or Python,
we will almost certainly be analyzing tables
with named columns and multiple rows.
Such tables are called [%g dataframe "dataframes" %],
and their performance is important when we are working with large datasets.
This chapter therefore implements dataframes in two ways
and shows how to compare their performance.

## Options {: #perf-options}

To start,
let's create an [%i "abstract class" %]
that defines the methods our dataframe classes will support.
This class requires [%i "concrete class" "concrete classes" %]
to implement the eight methods shown below:

[% inc file="df_base.py" %]

<div class="callout" markdown="1">

### Docstrings Are Enough

Every method in Python needs a body,
so many programmers will write `pass` (Python's "do nothing" statement).
However,
a [%g docstring "docstring" %] also counts as a body,
so if we write those (which we should)
there's no need to write `pass`.

</div>

For our first usable implementation,
we will derive a class `DfRow` that uses
[%g row_wise "row-wise" %] storage
([%f perf-row-storage %]).
The dataframe is stored as a list of dictionaries,
each of which represents a row.
All of the dictionaries must have the same keys
so that the concept of "column" is meaningful,
and the values associated with a particular key must all have the same type.

[% figure
   slug="perf-row-storage"
   img="row_storage.svg"
   alt="Row-wise storage"
   caption="Storing a dataframe's data in rows."
%]

Our second implementation,
`DfCol`,
will use [%g column_wise "column-wise" %] storage
([%f perf-col-storage %]).
Each column is stored as a list of values,
all of which are of the same type.
The dataframe itself is a dictionary of such lists,
all of which have the same length
so that there are no holes in any of the rows.
How we store the data determines which methods are easy to implement
and which are hard,
and which are fast or slow.

[% figure
   slug="perf-col-storage"
   img="col_storage.svg"
   alt="Column-wise storage"
   caption="Storing a dataframe's data in columns."
%]

## Row-Wise Storage {: #perf-row}

We start by deriving `DfRow` from `DataFrame` and writing its constructor,
which takes a list of dictionaries as an argument,
checks that they're consistent with each other,
and saves them:

[% inc file="df_row.py" keep="top" %]

The [%i "helper function" %] to check that a bunch of dictionaries
all have the same keys and the same types of values associated with those keys is:

[% inc file="util.py" keep="match" %]

Notice that `DfRow`'s constructor compares all of the rows against the first row.
Doing this means that we can't create an empty dataframe,
i.e.,
one that has no rows.
This restriction wasn't part of our original design:
it's an accident of implementation that might surprise our users.
It's OK not to fix this while we're prototyping,
but we will look at ways to address it in the exercises.
{: .continue}

Four of the methods required by `DataFrame` are easy to implement
on top of row-wise storage,
though once again our implementation assumes there is at least one row:

[% inc file="df_row.py" keep="simple" %]

Checking equality is also relatively simple.
Two dataframes are the same if they have exactly the same columns
and the same values in every column:

[% inc file="df_row.py" keep="equal" %]

Notice that we use `other.cols()` and `other.get()`
rather than reaching into the other dataframe.
We are planning to implement dataframes in several different ways,
and we might want to compare instances of those different implementations.
Since they might have different internal data structures,
the only safe way to do this is
to rely on the interface defined in the [%i "base class" %].
{: .continue}

Our final operations are selection,
which returns a subset of the original dataframe's columns,
and filtering,
which returns a subset of its rows.
Since we don't know how many columns the user might want,
we give the `select` method a single parameter `*names`
that will capture zero or more positional arguments.
We then build a new list of dictionaries
that only contain the fields with those names ([%f perf-row-select %]:

[% inc file="df_row.py" keep="select" %]

[% figure
   slug="perf-row-select"
   img="row_select.svg"
   alt="Row-wise select"
   caption="Selecting columns from data stored as rows."
%]

We now need to decide how to filter rows.
Typical filtering conditions include,
"Keep rows where `red` is non-zero,"
"Keep rows where `red` is greater than `green`,"
and, "Keep rows where `red+green` is within 10% of `blue`."
Rather than trying to anticipate every possible rule,
we require users to define functions
whose parameters match the names of the table's columns.
For example,
if we have this test [%i "fixture" %]:

[% inc file="test_df_row.py" keep="fixture" %]

then we should be able to write this test:
{: .continue}

[% inc file="test_df_row.py" keep="filter" %]

We can implement this  by using `**` to [%i "spread" %] the row
across the function's parameters ([%x oop %]).
If there are keys in the row that don't match parameters in the function
or vice versa,
Python will throw an exception,
but that's probably what we want.
Using this,
the implementation of `DfRow.filter` is:

[% inc file="df_row.py" keep="filter" %]

Notice that the dataframe created by `filter`
re-uses the rows of the original dataframe ([%f perf-row-filter %]).
This is safe and efficient so long as dataframes are [%g immutable "immutable" %],
i.e.,
so long as their contents are never changed in place.
Most dataframe libraries work this way:
while recycling memory can save a little time,
it usually also makes bugs much harder to track down.

[% figure
   slug="perf-row-filter"
   img="row_filter.svg"
   alt="Row-wise filtering"
   caption="Filtering data stored as rows."
%]

## Column-Wise Storage {: #perf-col}

Having done all of this thinking,
our column-wise dataframe class is somewhat easier to write.
We start as before with its constructor:

[% inc file="df_col.py" keep="top" %]

and use a helper function `all_eq` to check that
all of the values in any column have the same types:
{: .continue}

[% inc file="util.py" keep="eq" %]

<div class="callout" markdown="1">

### One Allowable Difference

Notice that `DfCol`'s constructor does *not* have the same [%i "signature" %]
as `DfRow`'s.
At some point in our code we have to decide which of the two classes to construct.
If we design our code well that decision will be made in exactly one place
and everything else will rely solely on the common interface defined by `DataFrame`.
But since we have to type a different class name at the point of construction,
it's OK for the constructors to be different.

</div>

The four methods that were simple to write for `DfRow`
are equally simple to write for `DfCol`,
though once again our prototype implementation accidentally disallows empty dataframes:

[% inc file="df_col.py" keep="simple" %]

As with `DfRow`,
the method that checks equality relies on the internal details of its own class
but uses the interface defined by `DataFrame` to access the other object:

[% inc file="df_col.py" keep="equal" %]

To select columns,
we pick the ones named by the caller
and use them to create a new dataframe.
Again,
this recycles the existing storage:

[% inc file="df_col.py" keep="select" %]

[% figure
   slug="perf-col-select"
   img="col_select.svg"
   alt="Column-wise selection"
   caption="Column-wise selection."
%]

Finally,
we need to filter the rows of a column-wise dataframe.
Doing this is complex:
since values are stored in columns,
we have to extract the ones belonging to each row
to pass them into the user-defined filter function
([%f perf-col-filter %]).
And if that wasn't enough,
we want to do this solely for the columns that the user's function needs.

[% figure
   slug="perf-col-filter"
   img="col_filter.svg"
   alt="Packing column values into rows"
   caption="Extracting values from columns to create temporary rows."
%]

For now,
we will solve this problem
by requiring the user-defined filter function to define [%i "parameter" "parameters" %]
to match all of the dataframe's columns
regardless of whether they are used for filtering or not.
We will then build a temporary dictionary with all the values in a "row"
(i.e.,
the corresponding values across all columns)
and use `**` to spread it across the filter function.
[%x bonus %] looks at a safer, but more complex, way to do this.

[% inc file="df_col.py" keep="filter" %]

Time to write some tests.
This one checks that we can construct a dataframe with some values:

[% inc file="test_df_col.py" keep="test_two_pairs" %]

while this one checks that `filter` works correctly:
{: .continue}

[% inc file="test_df_col.py" keep="test_filter" %]

## Performance {: #perf-performance}

Our two implementations of dataframes have identical interfaces,
so how can we choose which to use?

<div class="callout" markdown="1">

### Transactions vs. Analysis

Regardless of data volumes,
different storage schemes are better (or worse) for different kinds of work.
[%g oltp "Online transaction processing" %] (OLTP)
refers to adding or querying individual records,
such as online sales.
[%g olap "online analytical processing" %] (OLAP),
on the other hand,
processes selected columns of a table in bulk to do things like find averages over time.
Row-wise storage is usually best for OLTP,
but column-wise storage is better suited for OLAP.
If data volumes are large,
[%g data_engineer "data engineers" %] will sometimes run two databases in parallel,
using [%g batch_processing "batch processing" %] jobs
to copy new or updated records from the OLTP databases over to the OLAP database.

</div>

To compare the speed of these classes,
let's write a short program to create dataframes of each kind
and time how long it takes to select their columns and filter their rows.
To keep things simple
we will create dataframes whose columns are called `label_1`, `label_2`, and so on,
and whose values are all integers in the range 0–9.
A thorough set of [%g benchmark "benchmarks" %]
would create columns with other datatypes as well,
but this example is enough to illustrate the technique.

[% inc file="timing.py" keep="create" %]

To time filtering,
we arbitrarily decide to keep rows with an even value in the first column:

[% inc file="timing.py" keep="filter" %]

Since `DfCol` and `DfRow` derive from the same base class,
`time_filter` doesn't care which we give it.
Again,
if we were doing this for real
we would look at actual programs
to see what fraction of rows filtering usually kept and simulate that.
{: .continue}

To time `select`,
we arbitrarily decide to keep one third of the columns:

[% inc file="timing.py" keep="select" %]

Finally,
we write a function that takes a list of strings like `3x3` or `100x20`,
creates dataframes of each size,
times operations,
and reports the results.
We call this function `sweep` because
executing code multiple times with different parameters to measure performance
is called [%g parameter_sweeping "parameter sweeping" %]:

[% inc file="timing.py" keep="sweep" %]

The results are shown in [%t perf-timing %] and [%f perf-analysis %].
For a \\( 1000 \times 1000 \\) dataframe
selection is over 250 times faster with column-wise storage than with row-wise,
while filtering is 1.8 times slower.

<div class="table" id="perf-timing" caption="Dataframe timings." markdown="1">
| nrow  | ncol  | filter col | select col | filter row | select row |
| ----- | ----- | ---------- | ---------- | ---------- | ---------- |
|    10 |    10 | 8.87e-05   | 7.70e-05   | 4.41e-05   | 2.50e-05   |
|   100 |   100 | 0.00275    | 4.10e-05   | 0.00140    | 8.76e      |
|  1000 |  1000 | 0.146      | 0.000189   | 0.0787     | 0.0508     |
| 10000 | 10000 | 19.0       | 0.00234    | 9.97       | 5.57       |
</div>

[% figure
   slug="perf-analysis"
   img="analysis.svg"
   alt="Performance curves"
   caption="Relative performance of row-wise and column-wise storage."
   cls="here"
%]

We can get much more insight by [%g profiling "profiling" %] our code
using Python [`cProfile`][py_cprofile] module,
which collects detailed information on how long each function runs
and reports the result:

[% inc file="profile.sh" %]
[% inc file="profile.out" head="10" %]

The profiler's output tells us
the number of times each function or method was called,
the total time spent in those calls (which is what we care about most),
the time spent per call,
and the cumulative time spent in that call and all the things it calls.
Right away we can see that the `dict_match` function
that checks the consistency of the rows in a row-oriented dataframe
is eating up a lot of time.
It's only called in the constructor,
but since we're constructing a new dataframe for each `filter` and `select`,
removing that safety check would speed things up.

Looking down a little further,
the [%i "dictionary comprehension" %] in `DfCol.filter` takes a lot of time as well.
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

## Summary {: #perf-summary}

[% figure
   slug="perf-concept-map"
   img="concept_map.svg"
   alt="Concept map for dataframes"
   caption="Concepts for dataframes."
   cls="here"
%]

## Exercises {: #perf-exercises}

### More Efficient Filtering {: .exercise}

Derive a class from `DfCol` and override its `filter` method
so that the user-defined filtering functions take zero or more columns
and an row index called `i_row` as parameters
and return `True` or `False` to signal whether the row passes the test.

1.  How much faster does this make filtering?

2.  When would it be useful for filtering functions
    to take no column at all as parameters?

### Empty Dataframes {: .exercise}

An empty dataframe is as reasonable and as useful as an empty string or an empty list.
`DfCol` can represent this,
but `DfRow` cannot:
if the list of dictionaries is empty,
we cannot ask for columns' names.
Derive another dataframe class from `DF` that uses row-wise storage
but can represent a dataframe with no rows.

### Unified Constructors {: .exercise}

Modify the constructors of `DfRow` and `DfCol` to have the same signatures.
Where and why might this be useful?

### Fixture Functions {: .exercise}

Read the documentation for the `@fixture` [%i "decorator" %] in [pytest][pytest]
and modify the tests in this chapter to use it.

### Using Arrays {: .exercise}

Derive another dataframe class from `DF`
that uses Python's [`array`][py_array] module for column-wise storage.
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

### Filtering by Strings {: .exercise}

Modify the comparison of filter and select to work with tables
that contain columns of strings instead of columns of numbers
and see how that changes performance.
For testing,
creating random 4-letter strings using the characters A-Z
and then filter by:

-   an exact match,
-   strings starting with a specific character, and
-   strings that contain a specific character

### Inspection {: .exercise}

Rewrite `DfCol.filter` using Python's [`inspect`][py_inspect] module
so that users' filtering functions
only need to define parameters for the columns of interest.

### Join Performance {: .exercise}

A [%i "join" %] combines data from two tables based on matching keys.
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

### Join Optimization {: .exercise}

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
