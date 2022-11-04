---
title: "A Build Manager"
syllabus:
- FIXME
---

Programs in [%i "compiled language" "language!compiled" %][%g compiled_language "compiled languages" %][%/i%]
like [%i "C" %]C[%/i%] and [%i "Java" %]Java[%/i%]
have to be translated into lower-level forms before they can run.
There are usually two stages to the translation:
compiling each source file into some intermediate form,
and then [%i "linking (compiled language)" "compiled language!linking" %][%g link "linking" %][%/i%] the compiled modules
to each other and to libraries
to create a runnable program
([% f builder-compiling %]).

[% figure
   slug="builder-compiling"
   img="compiling.svg"
   alt="Compiling and linking"
   caption="Compiling source files and linking the resulting modules."
%]

If a source file hasn't changed,
there's no need to recompile it before linking.
A [%i "build manager" %][%g build_manager "build manager" %][%/i%] takes a description of what depends on what,
figures out which files are out of date,
determines an order in which to rebuild things,
and then does whatever is required and only what is required [% b Smith2011 %].

The first build manager,
[%i "Make" %][Make][gnu_make][%/i%],
was created to handle compilation of C programs,
but build managers are used to update packages,
regenerate websites ([%x templating %]),
or re-create documentation from source code.
This chapter creates a simple build manager to illustrate how they work.

## Structure {: #builder-structure}

The input to a build manager is a set of rules,
each of which has:

-   a [%i "build target" "target!build" %][%g build_target "target" %][%/i%],
    which is the file to be updated;

-   some [%i "dependency (in build)" "build!dependency" %][%g dependency "dependencies" %][%/i%],
    which are the things that file depends on;
    and

-   a [%i "recipe (in build)" "build!recipe" %][%g build_recipe "recipe" %][%/i%]
    that specifies how to update the target
    if it is out of date compared to its dependencies.

The target of one rule can be a dependency of another rule,
so their relationships form a [%i "directed acyclic graph (DAG)" "DAG" %][%g dag "directed acyclic graph" %][%/i%]
([% f builder-dependencies %]).
The graph is directed because "A depends on B" is a one-way relationship,
while "acyclic" means it cannot contains loops:
if something depends on itself we can never finish updating it.

[% figure
   slug="builder-dependencies"
   img="dependencies.svg"
   alt="Respecting dependencies"
   caption="How a build manager finds and respects dependencies."
%]

We say that a target is [%i "stale (in build)" "build!stale" %][%g build_stale "stale" %][%/i%]
if it is older than any of its dependencies.
When this happens,
we use the recipes to bring it up to date.
Our build manager therefore must:

1.  Read a file containing rules.

1.  Construct the dependency graph.

1.  Figure out which targets are stale.

1.  Build those targets,
    making sure to build things *before* anything that depends on them is built.

<div class="callout" markdown="1">

### Topological order

A [%i "topological order" %][%g topological_order "topological ordering" %][%/i%] of a graph
arranges the nodes so that every node comes after everything it depends on.
For example,
if A depends on both B and C,
then (B, C, A) and (C, B, A) are both valid topological orders of the graph.

</div>

## Representing Rules {: #builder-rules}

We will store our rules in [%g yaml "YAML" %] files like this:

[% inc file="three_simple_rules.yml" %]

We could equally well have used [%g json "JSON" %],
but it wouldn't have made sense to use [%g csv "CSV" %]:
rules have a nested structure,
and CSV doesn't represent nesting gracefully.
{: .continue}

We would normally implement all of the methods required by the builder at once,
but to make the evolving code easier to follow we will write them them one by one.
Let's start by writing a class that loads a configuration file:

[% inc file="config_loader.py" keep="body" %]

We need to check each rule because YAML is a generic file format
that doesn't know anything about the extra requirements of our rules:

[% inc file="config_loader.py" keep="check" %]

The next step is to turn the configuration into a graph in memory.
We derive a class from `ConfigLoader` so that we can recycle the code we've already written
and call a couple of methods that we are planning to add:

[% inc file="graph_creator.py" keep="body" %]

We use the [networkx][networkx] module to manage nodes and links
rather than writing our own classes for graphs,
and store the recipe to rebuild a node in that node:

[% inc file="graph_creator.py" keep="build" %]

`networkx` provides implementations of some common graph algorithms,
including one to find cycles,
so let's write that next:

[% inc file="graph_creator.py" keep="check" %]

Finally,
we write a `__str__` method so we can see what we've built:

[% inc file="graph_creator.py" keep="str" %]

When we run this with our three simple rules as input we get:

[% inc pat="graph_creator.*" fill="sh out" %]

Let's write a quick test to make sure the cycle detector works as intended:

[% inc file="circular_rules.yml" %]
[% inc pat="check_cycles.*" fill="sh out" %]

## Stale Files {: #builder-timestamp}

The next step is to figure out which files are out of date.
Make does this by comparing the [%i "timestamp!in build" "build!timestamp" %]timestamps[%/i%] of the files in question,
but this isn't always reliable:
[%i "clock synchronization (in build)" "build!clock synchronization" %]computers' clocks may be slightly out of sync[%/i%],
which can produce a wrong answer on a networked filesystem,
and the operating system may only report file update times to the nearest millisecond
(which seemed very short in 1970 but seems very long today).

More modern build systems store a [%i "hash code!in build" "build!hash code" %]hash[%/i%] of each file's contents
and compare the current hash to the stored one to see if the file has changed.
We looked at hashing in [%x backup %],
so we will use the timestamp approach here,
but instead of using a mock filesystem
we will load another configuration file that specifies fake timestamps for files:

[% inc file="add_timestamps.yml" %]

Since we want to associate those timestamps with files,
we add steps to the constructor and the `build` method
to read the timestamp file and add information to the graph's nodes:

[% inc file="add_timestamps.py" keep="body" %]

and then implement `add_timestamps`:
{: .continue}

[% inc file="add_timestamps.py" keep="timestamps" %]

Before we move on,
let's make sure that adding timestamps works as we want:

[% inc pat="add_timestamps.*" fill="sh out" %]

## Updating Files {: #builder-update}

To figure out which recipes to execute and in which order,
we set the pretended current time to the latest time of any file,
then look at each file in topological order.
If a file is older than any of its dependencies,
we update the file *and* its pretended timestamp
to trigger an update of anything that depends on it.
First,
we add a step to `build`:

[% inc file="update_timestamps.py" keep="body" %]

Next,
we implement the `run` method.
We can pretend that updating a file always takes one unit of time,
so we advance our fictional clock by one for each build.
Using `networkx.topological_sort` to create the topological order,
we get this:

[% inc file="update_timestamps.py" keep="run" %]

The `run` method:

1.  Gets a sorted list of nodes.

1.  Sets the starting time to be one unit past the largest file time.

1.  Checks each file in order.
    If that file is stale,
    we print the steps we would run and then update the file's timestamp.
    We only advance the notional current time when we do an update.

In order to check if a file is stale,
we see if any of its dependencies currently have timestamps
greater than or equal to the target's timestamp:

[% inc file="update_timestamps.py" keep="stale" %]

Our `update` method simply prints the actions it would take:

[% inc file="update_timestamps.py" keep="update" %]

When we run this,
it seems to do the right thing:

[% inc pat="update_timestamps.*" fill="sh out" %]

## Variables {: #builder-variables}

We don't want to have to write a hundred nearly-identical recipes
if our website has a hundred blog posts
or a hundred pages of documentation.
Instead,
we want to be able to write generic [%i "build!rule" "rule (in build)" %][%g build_rule "build rules" %][%/i%].
To do this we need:

-   a way to define a set of files;

-   a way to specify a generic rule;
    and

-   a way to fill in parts of that rule.

We will achieve this by overriding `build_graph` to replace variables in recipes with values.
Once again,
object-oriented programming helps us change only what we need to change,
provided we divided our problem into sensible chunks in the first place.

Make provides
[%i "automatic variable (in build)" "build!automatic variable" %][%g automatic_variable "automatic variables" %][%/i%]
with names like `$<` and `$@`
to represent the parts of a rule.
Our variables will be more readable:
we will use `@TARGET` for the target,
`@DEPENDENCIES` for the dependencies (in order),
and `@DEP[1]`, `@DEP[2]`, and so on for specific dependencies
([% f builder-pattern-rules %]).

[% figure
   slug="builder-pattern-rules"
   img="pattern_rules.svg"
   alt="Pattern rules"
   caption="Turning patterns rules into runnable commands."
%]

Our variable expander looks like this:

[% inc file="expand_variables.py" keep="expand" %]

The first thing we do is test that it works when there *aren't* any variables to expand
by running it on the same example we used previously:

[% inc pat="expand_variables_no_vars.*" fill="sh out" %]

This is perhaps the most important reason to create tests:
they tell us if something we have added or changed
has broken something that used to work
so that we have a solid base for new code.
{: .continue}

[% inc file="three_variable_rules.yml" %]
[% inc pat="expand_variables_with_vars.*" fill="sh out" %]

## Generic Rules {: #builder-generic}

Now we need to add [%i "pattern rule (in build)" "build!pattern rule" %][%g pattern_rule "pattern rules" %][%/i%]:
Our test rules file is:

[% inc file="pattern_rules.yml" %]

and our first attempt at reading it extracts rules before expanding variables:
{: .continue}

[% inc file="pattern_attempt.py" keep="body" %]

However,
it doesn't work:

[% inc pat="pattern_attempt.*" fill="sh out" %]

After a bit of poking around we realize that
we're looking at the rule for `%.in`.
A bit more poking around and we realize that
when we created edges in the graph between a target and its dependencies,
`networkx` automatically added a node for the dependency
if one didn't exist yet.
As a result,
when we say that `%.out` depends on `%.in`,
we wind up with a node for `%.in` that doesn't have any recipes.

We can fix our problem by changing the `build_graph` method
so that it saves pattern rules in a dictionary
and then builds the graph from the non-pattern rules:

[% inc file="pattern_final.py" keep="build" %]

Expanding rules relies on two helper methods:

[% inc file="pattern_final.py" keep="expand" %]

The first helper finds rules:

[% inc file="pattern_final.py" keep="find" %]

and the second adds links and recipes to the graph:
{: .continue}

[% inc file="pattern_final.py" keep="fill" %]

We're finally ready to test:

[% inc pat="pattern_final.*" fill="sh out" %]

## Discussion {: #builder-discuss}

We have added a lot of steps to our original template method,
which makes it a bit of a stretch to claim that the overall operation hasn't changed.
Knowing what we know now,
we could go back and modify the original `SkeletonBuilder.build` method
to include those extra steps and provide do-nothing implementations.

The root of the problem is that we didn't anticipate all the steps that would be involved
when we wrote our template method.
It typically takes a few child classes for this to settle down;
if it never does,
then [%i "Template Method pattern" "design pattern!Template Method" %]Template Method[%/i%] is probably the wrong pattern for our situation.
Realizing this isn't a failure in initial design:
we always learn about our problem as we try to capture it in code,
and if we know enough to anticipate 100% of the issues that are going to come up,
it's time to put what we've learned in a library for future use.

[% fixme concept-map %]

## Exercises {: #builder-exercises}

### Handle failure {: .exercise}

1.  Modify the build manager to accommodate build steps that fail.

2.  Write tests to check that this change works correctly.

### Merge files {: .exercise}

Modify the build manager so that it can read multiple build files
and execute their combined rules.

### Conditional execution {: .exercise}

Modify the build manager so that:

1.  The user can pass `variable=true` and `variable=false` arguments on the command-line
    to define variables.

2.  Rules can contain an `if: variable` field.

3.  Those rules are only executed if the variable is defined and true.

Write tests to check that this works correctly.

### Define filesets {: .exercise}

Modify the build manager so that users can define sets of files:

```yml
fileset:
  name: everything
  contains:
    - X
    - Y
    - Z
```

and then refer to them later:
{: .continue}

```yml
- target: P
  depends:
  - @everything
```

### Globbing {: .exercise}

Modify the build manager so that it can dynamically construct a set of files:

```yml
glob:
  name: allAvailableInputs
  pattern: "./*.in"
```

and then refer to them later:
{: .continue}

```yml
- target: P
  depends:
  - @allAvailableInputs
```

### Use hashes {: .exercise}

1.  Write a program called `build_init.py` that calculates a hash
    for every file mentioned in the build configuration
    and stores the hash along with the file's name in `build_hash.json`.

2.  Modify the build manager to compare the current hashes of files
    with those stored in `build_hash.json`
    in order to determine what is out of date,
    and to update `build_hash.json` each time it runs.
