---
title: "A Pipeline Runner"
syllabus:
- FIXME
---

Data science is all the rage these days.
No one can agree on exactly what it is,
but everyone's definition includes processing large datasets.
Data scientists usually do this with pipelines
that apply several operations to the data one after another.
In order to automate, share, and check their work,
they want the processing steps to be reproducible:
someone else,
somewhere else,
ought to be able to re-run the exact same steps
without consulting the original author.

This chapter builds a small toolkit for running pipelines
that is easy to extend
and that automatically records the [%g provenance "provenance" %]
of each output.
Since this isn't a book about data science,
we will use common text processing operations in our examples.
Please feel free to replace them with complicated mathematics.

## Pipelines as Lists {: #pipe-list}

Suppose we have five functions:

-  `read(filename)` reads a CSV file and returns a list of rows,
   each of which is a list of values.
-  `head(data, num)` returns the first `num` rows of a dataset.
-  `tail(data, num)` returns the last `num` rows.
-  `left(data, num)` and `right(data, num)` return
    the first and last `num` columns of the data respectively.

We can combine these functions in two ways.
The first uses nested function calls:

```python
left(tail(head(read("sample_data.csv"), 10), 5), 2)
```

but this quickly becomes hard to read.
(Quick, is the 10 being passed to `head` or to `tail`?)
The second uses temporary variables:
{: .continue}

```python
data = read("sample_data.csv")
data = head(data, 10)
data = tail(frame, 5)
data = left(data, 2)
```

which is easier to read when there are more than a handful of stages,
but can be error-prone.
(Did you notice that the code above is passing `frame` to `tail`
instead of `data`?)
{: .continue}

But a function is just another kind of object,
so we can put it in a list along with its arguments like this:

[% inc file="direct_list.py" omit="omit" %]

## Configuration {: #pipe-config}

Every function remembers the name it was given when it was defined:

[% inc pat="func_name.*" fill="py out" %]

so we can convert a list of functions into a lookup table:
{: .continue}

[% inc pat="func_table.*" fill="py out" %]

We should therefore be able to construct a pipeline
from a YAML file like this
without needing a long set of `if` statements
to match names to functions:

[% inc file="pipeline_manual.yml" %]

The code that runs the steps described in this pipeline
creates the lookup table
and then calls each stage with the given parameters:

[% inc file="pipeline_manual.py" keep="func" %]

## Collecting Functions {: #pipe-collect}

Our `pipeline` function works,
but the call to it isn't any prettier
than the nested function calls we set out to replace:

[% inc file="pipeline_manual.py" keep="call" %]

We could move the line that turns a list of functions into a dictionary
out of `pipeline`
and require the user to build that lookup table for us,
but there's a cleaner way.
Let's define a [%g decorator "decorator" %]
that adds a function to a lookup table:

[% inc file="decorated.py" keep="decorator" %]

We can then use this decorator
to mark the functions that we want to make available
to the pipeline:
{: .continue}

[% inc file="decorated.py" keep="sample" %]

and then in our pipeline code
we can import the `EXPORTS` table
(renaming it to make its purpose a little clearer):
{: .continue}

[% inc file="pipeline_decorated.py" keep="import" %]

The call to `pipeline` is then:
{: .continue}

[% inc file="pipeline_decorated.py" keep="call" %]

If we want to make functions from many files
available to our pipeline,
we'll have to merge their exported dictionaries.
We'll explore this in the exercises.

## Configuration and Provenance {: #pipe-provenance}

Our modified pipeline also doesn't allow for any global configuration
(i.e., parameters that are shared between stages)
and doesn't keep a record of what it actually did.
We will tackle these problems together.

First,
we want to be able to pass some global parameters to all stages of the pipeline
as well as local (per-stage) parameters.
When we're done,
our configuration file will like this:

[% inc file="pipeline_global.yml" %]

We don't want our generic `pipeline` function
to have to know about the functions it runs,
so let's modify all of the latter to take optional arguments
as shown below:

[% inc file="generic.py" keep="sample" %]

Our revised `pipeline` function is now:

[% inc file="pipeline_global.py" keep="func" %]

We also want to know what each run of a pipeline actually did.
Let's rewrite the runner to create a list of provenance records:

[% inc file="pipeline_provenance.py" keep="func" %]

The `run` function finds and runs the requested function,
then records its name,
its parameters,
how long it took to execute,
and how big its output was:

[% inc file="pipeline_provenance.py" keep="run" %]

If we run this and dump the provenance record as YAML we get:

[% inc file="pipeline_provenance.out" %]

Let's come back to configuration.
Right now we have put everything for our pipeline in one self-contained file,
but in real situations our pipelines will probably share a lot of settings.
Many large applicatons allow up to four layers of configuration:

1.  A system-wide configuration file for general settings.

2.  A user-specific configuration file for personal preferences.

3.  A job-specific file with settings for a particular run.

4.  Command-line options to change things that commonly change.

This is sometimes called [%g overlay_configuration "overlay configuration" %]
because each level overrides the ones before it.
It's more complex that our example needs,
but is worth building to see how it's done:

[% inc file="load_config.py" %]

[% fixme concept-map %]

## Exercises {: #pipe-exercises}

### Merging functions

Modify the pipeline code so that it can load runnable functions from many different files.
What should you do if two or more files export functions with the same names?

### Error handling

Our pipeline doesn't catch exceptions or do any other error handling.
Modify it so that it does.
