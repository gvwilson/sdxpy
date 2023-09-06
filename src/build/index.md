---
syllabus:
-   Build managers track dependencies between files and update files that are stale.
-   Every build rule has a target, some dependencies, and a recipe for updating the target.
-   Build rules form a directed graph which must not contain cycles.
-   Pattern rules describe the dependencies and recipes for sets of similar files.
-   Pattern rules can use automatic variables to specify targets and dependencies in recipes.
depends:
-   persist
---

Suppose that `plot.py` produces `result.svg` from `collated.csv`,
that `collated.csv` is produced from `samples.csv` and `controls.csv` by `analyze.py`,
and that `samples.csv` depends on `normalize.py` and `raw.csv`.
If `raw.csv` changes we want to re-run all three programs;
if `controls.csv` changes,
on the other hand,
we only need to re-run the analysis and plotting programs.
If we try to keep track of this ourselves we will inevitably make mistakes;
instead,
we should use a [%g build_manager "build manager" %]
to keep track of which files depend on which
and what actions to take to create or update files.
This chapter shows how a simple build manager works,
and along the way introduces some algorithms for working with graphs.

## Concepts {: #build-concepts}

The first build manager,
[Make][gnu_make],
was written by a student intern at Bell Labs in the 1970s.
Many others now exist (such as [SCons][scons] and [Snakemake][snakemake]),
but all perform the same basic operations.
If a [%g build_target "target" %] is [%g build_stale "stale" %]
with respect to any of its  [%g dependency "dependencies" %],
the build manager runs a [%g build_recipe "recipe" %] to refresh it.

The build manager runs recipes in an order that respects dependencies,
and it only runs each recipe once (if at all).
In order for this to be possible,
targets and dependencies must form a [%g dag "directed acyclic graph" %],
i.e.,
there cannot be a [%g cycle "cycle" %] of links
leading from a [%i "node" %] back to itself.
The build manager constructs
a [%g topological_order "topological ordering" %] of that [%i "graph" %],
i.e.,
arranges nodes so that each one comes after everything it depends on,
and then builds what it needs to in that order
([%f build-dependencies %]).

[% figure
   slug="build-dependencies"
   img="dependencies.svg"
   alt="Dependencies in a four-node graph"
   caption="Dependencies and topological order"
%]

<div class="callout" markdown="1">

### A Bit of History

Make was created to manage programs in [%g compiled_language "compiled languages" %]
like [%i "C" %] and [%i "Java" %],
which have to be translated into lower-level forms before they can run.
There are usually two stages to the translation:
compiling each source file into some intermediate form,
and then [%g link "linking" %] the compiled modules
to each other and to libraries
to create a runnable program.
If a source file hasn't changed,
we don't need to recompile it before linking.
Skipping unnecessary work in this way can save a lot of time
when we are working with programs that contains thousands or tens of thousands of files.

</div>

## Initial Design {: #build-design}

Our first step is to decide how we are going to represent
[%g build_rule "build rules" %].
We could invent a special-purpose syntax to fit the problem,
but as we said in [%x parse %],
the world has enough data formats.
Instead,
we will represent our recipes as [%i "JSON" %].
For example,
this file describes two targets `A` and `B`
and states that the former depends on the latter:

[% inc file="double_linear_dep.json" %]

As in [%x archive %],
we will use [%i "successive refinement" %]
to create our first build manager.
Our `BuildBase` class takes a configuration file as a constructor argument,
loads it,
creates a topological ordering,
and then refreshes each target in order.
For now,
"refreshing" means "prints the update rule";
we will come back and make this more sophisticated later.

[% inc file="build_simple.py" keep="main" %]

To load a configuration file,
we read in the JSON,
build a set of known targets,
and then verify each rule using a helper method called `_check`:

[% inc file="build_simple.py" keep="config" %]

To check a rule,
we make sure the dictionary that represents it has the required keys
and that we have a rule for every dependency it mentions.
We also transform the rule's structure a bit to simplify later processing:
{: .continue}

[% inc file="build_simple.py" keep="check" %]

[% figure
   slug="build-diamond"
   img="diamond.svg"
   alt="Representing graph"
   caption="Representing dependency graph"
%]

<div class="callout" markdown="1">

### It's Not Extra Work

We have to implement the consistency checks for our build rules
because JSON is a generic format
that knows nothing about dependencies, rules, and required keys.
There is a format called [JSON Schema][json_schema] for specifying these things
and [a Python module][py_jsonschema] that implements its checks,
but using it here would trade seven lines of code
for ten minutes of explanation.
We will explore its use in the exercises,
but the most important point is that
whether we write code by hand
or use a library with a bit of configuration,
*someone* has to write these checks.

</div>

## Topological Sorting {: #build-sort}

The next step is to figure out a safe order in which to build things.
[%f build-topo-sort %] shows how our algorithm works:

1.  We find all the nodes in the dependency graph
    that don't have any outstanding dependencies.

2.  We append those to the result
    and then remove them from the dependencies of all the other nodes in the graph.

3.  If anything is still in the graph,
    we go back to the first step.

4.  If at any point the graph isn't empty but nothing is available,
    we have found a [%g circular_dependency "circular dependency" %],
    so we report the problem and fail.

[% figure
   slug="build-topo-sort"
   img="topo_sort.svg"
   alt="Trace of topological sorting"
   caption="Topological sort"
%]

The code that implements this algorithm is:

[% inc file="build_simple.py" keep="sort" %]

With all of this in place,
we can run our first test:

[% inc pat="double_linear_dep.*" fill="json out" %]

## A Better Design {: #build-better}

Our implementation works,
but we can do better:

1.  The configuration might not come directly from a JSON file—for example,
    it might be embedded in a larger file or generated by another program—so
    we should modify the constructor to take a configuration as input.

2.  Printing actions to the screen isn't very useful,
    so we should collect them and return an ordered list of
    the commands for the build manager.

3.  `assert` isn't a friendly way to handle user errors;
    we should raise `ValueError` (or a custom exception of our own)
    to indicate a problem.

4.  Our topological sort isn't [%g stable_sort "stable" %],
    i.e.,
    there's no way to predict the order in which two "equal" nodes
    will be added to the ordering.
    We will explore the reason for this in the exercises,
    but for now,
    we should sort node names when appending to the `result` list
    so that our tests can know what to check for.

5.  We might want to add other keys to rules,
    so we should put that check in a separate method that we can override.

The top level of our better build manager looks like this:

[% inc file="build_better.py" keep="main" %]

The revised configuration code is:
{: .continue}

[% inc file="build_better.py" keep="config" %]

and the updated topological sorting method is
{: .continue}

[% inc file="build_better.py" keep="sort" %]

We can now test that the code detects circularities in the dependency graph:

[% inc file="test_build_better.py" keep="test_circular" %]

and that it builds what it's supposed to:
{: .continue}

[% inc file="test_build_better.py" keep="test_no_dep" %]

We can also extend it.
For example,
suppose we only want to update targets that are older than their dependencies
(which is, after all, the whole point of a build manager).
If the targets are files,
we could their [%i "timestamp" "timestamps" %],
but for testing purposes
we would like to specify pretended times in the configuration:

[% inc file="test_build_time.py" keep="tests" %]

Starting from the class we have written so far,
we need to override three methods:
{: .continue}

[% inc file="build_time.py" keep="class" %]

<div class="callout" markdown="1">

### How We Actually Did It

Our final design uses
the [%g template_method_pattern "Template Method" %] pattern:
a method in a [%i "parent class" %] defines the [%i "control flow" %],
while [%i "child class" "child classes" %] implement those operations.
We didn't know in advance exactly
how to divide our code into methods;
instead,
as we were creating a class that loaded and used timestamps,
we reorganized the parent class
to create the [%g affordance "affordances" %] we needed.
Software design almost always works this way:
the first two or three times we try to extend something,
we discover changes that would make those tasks easier.
We should do less of this as time goes by:
if we are still doing large-scale [%i "refactor" "refactoring" %]
the tenth time we use something,
we should rethink our entire design.

</div>

<div class="pagebreak"></div>

## Summary {: #build-summary}

[% figure
   slug="build-concept-map"
   img="concept_map.svg"
   alt="Concept map of build manager"
   caption="Concept map"
   cls="here"
%]

## Exercises {: #build-exercises}

### Stable Sorting {: .exercise}

Recent versions of Python guarantee that
the entries in a `dict` preserve the order in which they were added,
but doesn't make any such guarantee for sets.
Explain why this makes it hard to test things that use sets.

### Checking Schema {: .exercise}

Rewrite the configuration validator to use [JSON Schema][json_schema]
via the associated [Python module][py_jsonschema].

### Handling Failure {: .exercise}

1.  Modify the build manager so that a configuration file can specify
    whether its rule should succeed or fail.
    (This isn't particularly useful in real life,
    but helps with testing.)

2.  Modify it so that if a rule fails,
    other buildable targets are still built
    (but anything that depends directly or indirectly on the target whose rule failed
    is *not* built).

3.  Write tests to check that this change works correctly.

### Merging Files {: .exercise}

1.  Modify the build manager so that it can read multiple build files
    and execute their combined rules.

2.  What does your solution do if two or more files specify rules
    for the same target?

### Using Hashes {: .exercise}

1.  Write a program called `build_init.py` that calculates a hash
    for every file mentioned in the build configuration
    and stores the hash along with the file's name in `build_hash.json`.

2.  Modify the build manager to compare the current hashes of files
    with those stored in `build_hash.json`
    to determine what is out of date,
    and to update `build_hash.json` each time it runs.

### Dry Run {: .exercise}

A [%g dry_run "dry run" %] of a build shows the rules that would be executed
but doesn't actually execute them.
Modify the build system in this chapter so that it can do dry runs.

### Phony Targets {: .exercise}

A [%g phony_target "phony target" %] is one that doesn't correspond to a file.
Developers often put phony targets in build files
to give themselves an easy way to re-run tests,
check code style,
and so on.
Modify the build system in this target so that
users can mark targets as phony.

### Multiple Build Files {: .exercise}

1.  Modify the tool built in this chapter so that
    one build file can import definitions and dependencies from another.

1.  How does your system prevent
    [%i "circular dependency" "circular dependencies" %]?
