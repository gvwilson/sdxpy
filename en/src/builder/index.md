---
title: "A Build Manager"
syllabus:
-   Build managers track dependencies between files and update files that are stale.
-   Every build rule has a target, some dependencies, and a recipe for updating the target.
-   Build rules form a directed graph which must not contain cycles.
-   Pattern rules describe the dependencies and recipes for sets of similar files.
-   Pattern rules can use automatic variables to specify targets and dependencies in recipes.
---

We wrote programs in [%x interpreter %] as lists of lists
which we then interpreted directly.
Programs in [%i "compiled language" "language!compiled" %][%g compiled_language "compiled languages" %][%/i%]
like [%i "C" %]C[%/i%] and [%i "Java" %]Java[%/i%],
on the other hand,
have to be translated into lower-level forms before they can run.
There are usually two stages to the translation:
compiling each source file into some intermediate form,
and then [%i "linking (compiled language)" "compiled language!linking" %][%g link "linking" %][%/i%] the compiled modules
to each other and to libraries
to create a runnable program
([% f builder-compiling %]).
If a source file hasn't changed,
we don't need to recompile it before linking.
Skipping unnecessary work in this way can save a lot of time
when we are working with programs that contains thousands or tens of thousands of files.

[% figure
   slug="builder-compiling"
   img="builder_compiling.svg"
   alt="Compiling and linking"
   caption="Compiling source files and linking the resulting modules."
%]

[%i "build manager" %][%g build_manager "Build managers" %][%/i%]
were invented to keep track of all of this automatically.
A build manager takes a description of what depends on what,
figures out which files are out of date,
determines an order in which to rebuild things,
and then does whatever is required and only what is required [% b Smith2011 %].
The first build manager,
[%i "Make" %][Make][gnu_make][%/i%],
was built to manage C programs,
but build managers are used to update packages,
regenerate websites ([%x templating %]),
re-create documentation from source code,
and run tests.
This chapter creates a simple build manager to illustrate how they work.

## Structure {: #builder-structure}

The input to a build manager is
a set of [%i "build rule" "rule!build" %][%g build_rule "build rules" %][%/i%],
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
   img="builder_dependencies.svg"
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

We would normally implement all of the builder's methods at once,
but we will instead write them them one by one to make the evolving code easier to follow.
Let's start by defining a class that loads a configuration file:

[% inc file="config_loader.py" keep="body" %]

We also need a method to check each rule because YAML is a generic file format
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

`networkx` implements some common graph algorithms,
including one to find cycles,
so let's add that next:

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
so we will use the timestamp approach here.
We should also test using a mock filesystem,
but for variety's sake
we will load another configuration file that specifies timestamps for files:

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

To check if a file is stale,
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
if our program has a hundred files
or our website has a hundred blog posts.
Instead,
we want to write generic [%i "build!rule" "rule (in build)" %]build rules[%/i%].
To do this we need:

-   a way to define a set of files;

-   a way to specify a generic rule;
    and

-   a way to fill in parts of that rule.

We will achieve this by overriding `build_graph` to replace variables in recipes with values.
Once again,
object-oriented programming lets us change only what we need to,
provided we divided our problem into sensible chunks in the first place.

<div class="callout" markdown="1">
### Extensibility and Experience

[%x interpreter %] said that one way to evaluate a program's design
is to ask how [%g extensibility "extensible" %] it is.
In practice,
extensibility usually comes from experience:
we can't know what [%g affordance "affordances" %] to provide
until we've tried extending our code in different ways a couple of times.
We [%g refactor "refactored" %] the examples in this book several times
as we wrote the explanations
so that early versions left room for later ones.
Don't be surprised or disappointed if you have to do this for your own code;
after you've extended and refactored something two or three times,
it usually settles down into its final form.
</div>

Make provides
[%i "automatic variable (in build)" "build!automatic variable" %][%g automatic_variable "automatic variables" %][%/i%]
with cryptic names like `$<` and `$@`
to represent the parts of a rule.
Our variables will be more readable:
we will use `@TARGET` for the target,
`@DEPENDENCIES` for the dependencies (in order),
and `@DEP[1]`, `@DEP[2]`, and so on for specific dependencies
([% f builder-pattern-rules %]).

[% figure
   slug="builder-pattern-rules"
   img="builder_pattern_rules.svg"
   alt="Pattern rules"
   caption="Turning patterns rules into runnable commands."
%]

Our variable expander looks like this:

[% inc file="expand_variables.py" keep="expand" %]

After adding this,
we immediately test that it works when there *aren't* any variables to expand
by running it on the same example we used previously:

[% inc pat="expand_variables_no_vars.*" fill="sh out" %]

This is perhaps the most important reason to create tests:
they tell us if something we have added or changed
has caused a [%g regression "regression" %],
i.e., has broken something that used to work.
If so,
the problem will be easier to fix while
the breaking change is still fresh in our minds.
{: .continue}

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

After a bit of poking around with a [%i debugger %]debugger[%/i%]
we realize that
the failure occurs when we're looking at the rule for `%.in`.
When we create edges in the graph between a target and its dependencies,
`networkx` automatically adds a node for the dependency
if one didn't exist yet.
As a result,
when we say that `%.out` depends on `%.in`,
we wind up with a node for `%.in` that doesn't have any recipes.

We can fix our problem by changing the `build_graph` method
so that it saves pattern rules in a dictionary
and then builds the graph from the non-pattern rules:

[% inc file="pattern_final.py" keep="build" %]

Expanding rules relies on two helper methods:
{: .continue}

[% inc file="pattern_final.py" keep="expand" %]

The first helper finds rules:
{: .continue}

[% inc file="pattern_final.py" keep="find" %]

and the second adds links and recipes to the graph:
{: .continue}

[% inc file="pattern_final.py" keep="fill" %]

We're finally ready to test:

[% inc pat="pattern_final.*" fill="sh out" %]

## Discussion {: #builder-discuss}

Our design uses the [%i "Template Method pattern" "design pattern!Template Method" %]Template Method[%/i%] pattern:
a method in a parent class defines the overall order of operations,
while child classes implement those operations without changing the flow of control.
We have added a lot of steps to our original template method,
which makes it a bit of a stretch to claim that the overall operation hasn't changed.
Knowing what we know now,
we could go back and modify the original `SkeletonBuilder.build` method
to include those extra steps and provide do-nothing implementations.

The root of the problem is that we didn't anticipate all the steps that would be involved
when we wrote our template method.
As we said earlier,
we typically have to refactor our base code
the first two or three times we try to extend it.
If it never settles down,
then Template Method is probably the wrong pattern for our situation.
Realizing this isn't a failure in initial design:
we always learn about our problem as we try to capture it in code,
and if we know enough to anticipate 100% of the issues that are going to come up,
it's time to put what we've learned in a library for future use.

## Summary {: #builder-summary}

[% figure
   slug="builder-concept-map"
   img="builder_concept_map.svg"
   alt="Concept map for build manager"
   caption="Concepts for build manager."
%]

## Exercises {: #builder-exercises}

### Reporting {: .exercise}

1.  Modify the build manager so that it expands all pattern rules
    and prints out a fully-expanded YAML build file.

2.  Test your extension by having the build manager read and execute
    the file it just created.

### Handle failure {: .exercise}

1.  Modify the build manager so that if a recipe fails,
    other targets that don't depend on it are still built.

2.  Write tests to check that this change works correctly.

### Dry run {: .exercise}

1.  Modify the build manager so that it can show what recipes it would execute
    without actually executing them.
    (Doing this is called a [%g dry_run "dry run" %].)

2.  Write tests to make sure that dry runs don't change any files.

### Merge files {: .exercise}

1.  Modify the build manager so that it can read multiple build files
    and execute their combined rules.

2.  What does your solution do if two or more files specify rules
    for the same target?
    What does the *existing* code do?

### Specific targets {: .exercise}

Modify the build manager so that users can specify
which targets they want to update.
The build manager should only execute recipes needed to update those targets.

### Phony targets {: .exercise}

A [%g phony_target "phony target" %] is one that doesn't create or modify a file.
Programmers often put phony targets in build files
to do tasks like executing tests in a reproducible way.
Modify the build manager so that
users can specify and run phony targets.

### Conditional execution {: .exercise}

Modify the build manager so that:

1.  The user can pass `name=true` and `name=false` arguments on the command-line
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
