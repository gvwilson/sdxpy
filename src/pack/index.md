---
title: "A Package Manager"
version: 1
abstract: >
    Most languages have an online archive from which people can download packages,
    each of which has a name, one or more versions, and a list of dependencies.
    In order to install a package,
    we need to figure out exactly what versions of its dependencies to install;
    this chapter explores how to find a workable installation or prove that there isn't one.
syllabus:
-   Software packages often have multiple versions, which are usually identified by multi-part semantic version numbers.
-   A package manager must find a mutually-compatible set of dependencies in order to install a package.
-   Finding a compatible set of packages is equivalent to searching a multi-dimensional space.
-   The work required to find a compatible set of packages can grow exponentially with the number of packages.
-   Eliminating partially-formed combinations of packages can reduce the work required to find a compatible set.
-   An automated theorem prover can determine if a set of logical propositions can be made consistent with each other.
-   Most package managers use some kind of theorem prover to find compatible sets of packages to install.
depends:
-   dup
---

Inspired by the [%i "Comprehensive TeX Archive Network" %] ([CTAN][ctan]),
most languages have an online archive from which people can download packages,
such as Python's [PyPI][pypi].
Each [%i "package" %] typically has a name,
one or more versions,
and a list of [%i "dependency" dependencies %] (which are also versioned).
In order to install a package,
we need to figure out exactly what versions of its dependencies to install:
if A and B require different versions of C,
we might not be able to use A and B together.

This chapter explores how to find a workable installation or prove that there isn't one.
It is based in part on [this tutorial][package_manager_tutorial]
by [%i "Nison, Maël" "Maël Nison" url="nison_mael" %]
and on [Andreas Zeller's][zeller_andreas]
lecture on [academic prototyping][academic_prototyping];
interested readers might also enjoy
[Michael Reim's][reim_michael] [history of Unix packaging][unix_packaging].

## Semantic Versioning {: #pack-semver}

Most software projects use
[%g semantic_versioning "semantic versioning" %]
for software releases.
Each version is three integers X.Y.Z,
where X is the major version,
Y is the minor version,
and Z is the [%g patch "patch" %].

A package's authors increment its major version number
when a change to the package breaks
[%g backward_compatible "backward compatibility" %],
i.e., if code built for the old version will fail or behave unpredictably with the new one.
The minor version number is incremented when changes won't break any existing code,
and the patch number is changed for bug fixes that don't add any new features.

The notation for specifying ranges of versions looks like arithmetic:
`>=1.2.3` means "any version from 1.2.3 onward",
`<4` means "any version before 4.anything",
and `1.0-3.1` means "any version in the specified range (including patches)".
Note that version 2.1 is greater than version 1.99:
no matter how large a minor version number becomes,
it never spills over into the major version number.

It isn't hard to compare simple semantic version identifiers,
but handling [the whole standard][semver_spec]
is almost as tricky as handling dates and times correctly.
Our examples therefore number versions with plain integers;
we recommend the [`semantic-version`][py_semver] package
for working with the real thing.

## Exhaustive Search {: #pack-exhaustive}

To avoid messing around with parsers,
we store the [%i "manifest" %]
of available packages as JSON:

[%inc triple.json %]

The keys in the main dictionary identify packages
(which we've called `A`, `B`, and `C` for simplicity).
Each package has a dictionary whose keys are version numbers,
and each version has a dictionary showing
which versions of which other packages are dependencies
([%f pack-manifest %]).
It's a complex data structure,
but all of the detail is necessary.

[% figure
   slug="pack-manifest"
   img="manifest.svg"
   alt="Manifest structure"
   caption="Structure of version dependency manifest."
%]

<div class="callout" markdown="1">

### Comments

We have been advising you since [%x parse %] not to design your own data format,
but if you do,
please include a single standard way for people to add comments.
[%i "YAML" %] has this,
but [%i "JSON" %]
and [%i "CSV" %] don't.

</div>

Imagine that each package we need is an axis on a multi-dimensional grid
([%f pack-allowable %]),
so each point on the grid is a possible combination of package versions.
We can exclude regions of this grid using the constraints on the package versions;
the points that are left represent legal combinations.

[% figure
   slug="pack-allowable"
   img="allowable.svg"
   alt="Allowable versions"
   caption="Finding allowable combinations of package versions."
%]

How much work is it to check all of these possibilities?
Our example has \\( 3×3×2=18 \\) combinations.
If we were to add another package to the mix with two versions,
the [%g search_space "search space" %] would double;
add another,
and it would double again,
which means that if each package has approximately \\( c \\) version
and there are \\( N \\) packages,
the [%i "big-oh notation" "work grows" %] as \\( O(c^N) \\).
This exponential behavior is called
[%g combinatorial_explosion "combinatorial explosion" %],
and it makes brute-force solutions impractical even for small problems.
We will implement it as a starting point
(and to give us something to test more complicated solutions against),
but then we will need to find a more efficient approach.

<div class="callout" markdown="1">

### Reproducibility

There may not be a strong reason
to prefer one mutually-compatible set of packages over another,
but a package manager should resolve the ambiguity the same way every time.
It might not be what everyone wants,
but at least they will be unhappy for the same reasons everywhere.
This is why `pip list` (and similar commands for other package managers)
produce a listing of the exact versions of packages that have been installed:
a spec written by a developer that lists allowed ranges of versions specifies what we *want*,
while the listing created by the package manager specifies exactly what we *got*.
If we want to reproduce someone else's setup for debugging purposes,
we should install what is described in the latter file.

</div>

Our brute-force program generates all possible combinations of package versions,
then eliminates ones that aren't compatible with the manifest.
Its main body is just those steps in order
with a few `print` statements to show the results:

[%inc exhaustive.py mark=main %]

To generate the possibilities,
we create a list of the available versions of each package,
then use Python's [`itertools`][py_itertools] module
to generate the [%g cross_product "cross product" %]
that contains all possible combinations of items
([%f pack-product %]):

[%inc exhaustive.py mark=possible %]

[% figure
   slug="pack-product"
   img="product.svg"
   alt="Generating a cross product"
   caption="Generating all possible combinations of items."
%]

To check a candidate against the manifest,
we compare every entry X against every other entry Y:

1.  If X and Y are the same package, we keep looking.
    We need this rule because we're comparing every entry against every entry,
    which means we're comparing package versions to themselves.
    We could avoid this redundant check by writing a slightly smarter loop,
    but there's no point optimizing a horribly inefficient algorithm.

2.  If package X's requirements say nothing about package Y,
    we keep searching.
    This rule handles the case of X not caring about Y,
    but it's also the reason we need to compare all against all,
    since Y might care about X.

3.  Finally, if X does depend on Y,
    but this particular version of X doesn't list this particular version of Y
    as a dependency,
    we can rule out this combination.

4.  If we haven't ruled out a candidate after doing all these checks,
    we add it to the list of allowed configurations.

Sure enough,
these rules find 3 valid combinations among our 18 possibilities:

[%inc exhaustive.py mark=compatible %]
[%inc exhaustive.out %]

## Generating Possibilities Manually {: #pack-manual}

Our brute-force code uses `itertools.product`
to generate all possible combinations of several lists of items.
To see how it works,
let's rewrite `make_possibilities` to use a function of our own:

[%inc manual.py mark=start %]

The first half creates the same list of lists as before,
where each sub-list is the available versions of a single package.
It then creates an empty [%g accumulator "accumulator" %]
to collect all the combinations
and calls a [%i "recursion" "recursive function" %]
called `_make_possible` to fill it in.
{: .continue}

Each call to `_make_possible` handles one package's worth of work
([%f pack-recursive %]).
If the package is X,
the function loops over the available versions of X,
adds that version to the combination in progress,
and calls itself with the remaining lists of versions.
If there aren't any more lists to loop over,
the recursive calls must have included exactly one version of each package,
so the combination is appended to the accumulator.

[%inc manual.py mark=make %]
[%inc manual.out %]

[% figure
   slug="pack-recursive"
   img="recursive.svg"
   alt="Generating a cross product recursively"
   caption="Generating all possible combinations of items recursively."
%]

`_make_possible` uses recursion instead of nested loops
because we don't know how many loops to write.
If we knew the manifest only contained three packages,
we would write a triply-nested loop to generate combinations,
but if there were four,
we would need a quadruply-nested loop,
and so on.
This [%g recursive_enumeration_pattern "Recursive Enumeration" %]
[%i "design pattern" %]
uses one recursive function call per loop
so that we automatically get exactly as many loops as we need.

## Incremental Search {: #pack-incremental}

Generating an exponentiality of combinations
and then throwing most of them away
is inefficient.
Instead,
we can modify the recursive generator
to stop if a partially-generated combination of packages isn't legal.
Combining generation and checking made the code more complicated,
but as we'll see,
it leads to some significant improvements.

The main function for our modified program
is similar to its predecessor.
After loading the manifest,
we generate a list of all package names.
Unlike our earlier code,
the entries in this list don't include versions
because we're going to be checking those as we go:

[%inc incremental.py mark=main %]

Notice that
we reverse the list of packages before starting our search
if the user provides an extra command-line argument.
We'll use this to see how ordering affects efficiency.
{: .continue}

Our `find` function now has five parameters:

1.  The manifest that tells us what's compatible with what.

2.  The names of the packages we haven't considered yet.

3.  An accumulator to hold all the valid combinations we've found so far.

4.  The partially-completed combination we're going to extend next.

5.  A count of the number of combinations we've considered so far,
    which we will use as a measure of efficiency.

[%inc incremental.py mark=find %]

The algorithm combines the generation and checking we've already written:

1.  If there are no packages left to consider—i.e.,
    if `remaining` is an empty list—then
    what we've built so far in `current` must be valid,
    so we append it to `accumulator`.

2.  Otherwise,
    we put the next package to consider in `head`
    and all the remaining packages in `tail`.
    We then check each version of the `head` package in turn.
    If adding it to the current collection of packages
    wouldn't cause a problem,
    we continue searching with that version in place.

How much work does incremental checking save us?
Using the same test case as before,
we only create 11 candidates instead of 18,
so we've reduced our search by about a third:

[%inc incremental.sh %]
[%inc incremental.out %]

If we reverse the order in which we search,
though,
we only generate half as many candidates as before:
{: .continue}

[%inc incremental_reverse.sh %]
[%inc incremental_reverse.out %]

## Using a Theorem Prover {: #pack-smt}

Cutting the amount of work we have to do is good:
can we do better?
The answer is yes,
but the algorithms involved are complicated and the jargon almost impenetrable.
To give you a taste of how they work,
we will solve our example problem using the [Z3 theorem prover][z3].

Installing packages and proving theorems
may not seem to have a lot to do with each other,
but an automated theorem prover's purpose is
to determine how to make a set of logical propositions consistent with each other,
or to prove that doing so is impossible.
If we frame our problem as,
"Is there a choice of package versions
that satisfies all the inter-package dependencies at once?",
then a theorem prover is exactly what we need.

To start,
let's import a few things from `z3`
and create three [%g boolean_value "Boolean variables" %]:

[%inc z3_setup.py %]

Our three variables don't have values yet—they're not
either true or false.
Instead,
each one represents all the possible states a Boolean could be in.
If we had asked `z3` to create one of its special integers,
it would have given us something that initially encompassed
all possible integer values.
{: .continue}

Instead of assigning values to `A`, `B`, and `C`,
we specify constraints on them,
then ask `z3` whether it's possible to find a set of values,
or [%g model "model" %],
that satisfies all those constraints at once.
For example,
we can ask whether it's possible for `A` to equal `B`
and `B` to equal `C` at the same time.
The answer is "yes",
and the solution the solver finds is to make them all `False`:

[%inc z3_equal.py mark=solve %]
[%inc z3_equal.out %]

What if we say that `A` and `B` must be equal,
but `B` and `C` must be unequal?
In this case,
the solver finds a solution in which `A` and `B` are `True`
but `C` is `False`:

[%inc z3_part_equal.py mark=solve %]
[%inc z3_part_equal.out %]

Finally,
what if we require `A` to equal `B` and `B` to equal `C`
but `A` and `C` to be unequal?
No assignment of values to the three variables
can satisfy all three constraints at once,
and the solver duly tells us that:

[%inc z3_unequal.py mark=solve %]
[%inc z3_unequal.out %]

Returning to package management,
we can represent the versions from our running example like this:

[%inc z3_triple.py mark=setup %]

We then tell the solver that we want one of the available versions of package A:
{: .continue}

[%inc z3_triple.py mark=top %]

and that the three versions of package A are mutually exclusive:
{: .continue}

[%inc z3_triple.py mark=exclusive %]

We need equivalent statements for packages B and C;
we'll explore in the exercises
how to generate all of these from a package manifest.
{: .continue}

Finally,
we add the inter-package dependencies
and search for a result:

[%inc z3_triple.py mark=depends %]
[%inc z3_triple.out %]

The output tells us that the combination of A.3, B.3, and C.2
will satisfy our constraints.
{: .continue}

We saw earlier,
though,
that there are three solutions to our constraints.
One way to find the others is to ask the solver
to solve the problem again
with the initial solution ruled out.
We can repeat the process many times,
adding "not the latest solution" to the constraints each time
until the problem becomes unsolvable:

[%inc z3_complete.py mark=all %]
[%inc z3_complete.out %]

## Summary {: #pack-summary}

[%f pack-concept-map %] summarizes the key ideas introduced in this chapter.
The most important thing to take away is that
modern theorem provers can solve many more problems than most programmers realize.
While formulating problems in ways that theorem provers understand can be challenging,
solving those problems ourselves is usually much harder.

[% figure
   slug="pack-concept-map"
   img="concept_map.svg"
   alt="Concept map for package manager."
   caption="Concepts for package manager."
   cls="here"
%]

## Exercises {: #pack-exercises}

### Comparing Semantic Versions {: .exercise}

Write a function that takes an array of semantic version specifiers
and sorts them in ascending order.
Remember that `2.1` is greater than `1.99`.

### Parsing Semantic Versions {: .exercise}

Write a parser for a subset of the [semantic versioning specification][semver_spec].

### Using Scoring Functions {: .exercise}

Many different combinations of package versions can be mutually compatible.
One way to decide which actual combination to install
is to create a [%g scoring_function "scoring function" %]
that measures how good or bad a particular combination is.
For example,
a function could measure the "distance" between two versions as:

-   100 times the difference in major version numbers;

-   10 times the difference in minor version numbers
    if the major numbers agree;
    and

-   the difference in the patch numbers
    if both major and minor numbers agree.

Implement this function
and use it to measure the total distance between
the set of packages found by the solver
and the set containing the most recent version of each package.
Does it actually solve the original problem?
{: .continue}

### Regular Releases {: .exercise}

Some packages release new versions regularly,
e.g.,
Version 2023.1 is released on March 1 of 2023,
Version 2023.2 is released on September 1 of that year,
version 2024.1 is released on March 1 of the following year,
and so on.

1.  How does this make package management easier?

2.  How does it make it more difficult?

### Searching Least First {: .exercise}

Rewrite the constraint solver so that it searches packages
by looking at those with the fewest available versions first.
Does this reduce the amount of work done for the small examples in this chapter?
Does it reduce the amount of work done for larger examples?

### Using Exclusions {: .exercise}

1.  Modify the constraint solver so that
    it uses a list of package exclusions instead of a list of package requirements,
    i.e.,
    its input tells it that version 1.2 of package Red
    can *not* work with versions 3.1 and 3.2 of package Green
    (which implies that Red 1.2 can work with any other versions of Green).

2.  Explain why package managers aren't built this way.

### Generating Constraints {: .exercise}

Write a function that reads a JSON manifest describing package compatibilities
and generates the constraints needed by the Z3 theorem prover.

### Buildability {: .exercise}

1.  Convert the build dependencies from one of the examples in [%x build %]
    to a set of constraints for Z3
    and use the solution to find a legal build order.

2.  Modify the constraints to introduce
    a [%i "circular dependency" %]
    and check that the solver correctly determines
    that there is no legal build order.
