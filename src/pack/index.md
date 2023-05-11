---
syllabus:
-   Software packages often have multiple versions, which are usually identified by multi-part semantic version numbers.
-   A package manager must find a mutually-compatible set of dependencies in order to install a package.
-   Finding a compatible set of packages is equivalent to searching a multi-dimensional space.
-   The work required to find a compatible set of packages can grow exponentially with the number of packages.
-   Eliminating partially-formed combinations of packages can reduce the work required to find a compatible set.
-   An automated theorem prover can determine if a set of logical propositions can be made consistent with each other.
-   Most package managers use some kind of theorem prover to find compatible sets of packages to install.
---

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

1.  Implement this function
    and use it to measure the total distance between
    the set of packages found by the solver
    and the set containing the most recent version of each package.

2.  Explain why this doesn't actually solve the original problem.

### Regular Releases {: .exercise}

Some packages release new versions on a regular cycle,
e.g.,
Version 2021.1 is released on March 1 of 2021,
Version 2021.2 is released on September 1 of that year,
version 2022.1 is released on March 1 of the following year,
and so on.

1.  How does this make package management easier?

2.  How does it make it more difficult?

### Searching Least first {: .exercise}

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
    a [%g circular_dependency "circular dependency" %]
    and check that the solver correctly determines
    that there is no legal build order.
