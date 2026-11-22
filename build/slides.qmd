---
title: "A Build Manager"
---

<section class="slide" markdown="1">

## The Problem

-   `plot.py` produces `result.svg` from `collated.csv`

-   `analyze.py` produces `collated.csv` from `samples.csv` and `controls.csv`

-   Both `samples.csv` and `controls.csv` depends on `normalize.py` and `raw.csv`,
    but `normalize.py` takes a long time to run

-   How can we regenerate the files we need, but only when we need them?

</section>
<section class="slide" markdown="1">

## Make

-   [%g build_manager "Build managers" %]
    keep track of which files depend on which

    -   First tool of this kind was [Make][gnu_make]

    -   Many others now exist (e.g., [Snakemake][snakemake])

-   If a [%g build_target "target" %] is [%g build_stale "stale" %]
    with respect to any of its  [%g dependency "dependencies" %],
    run a [%g build_recipe "recipe" %] to refresh it

-   Run recipes in order

-   Run each recipe at most once

</section>
<section class="slide" markdown="1">

## Terminology

-   Targets and dependencies must form a [%g dag "directed acyclic graph" %]

-   A [%g topological_order "topological ordering" %] of a graph
    arranges nodes so that each one comes after everything it depends on

[% figure
   slug="build-dependencies"
   img="dependencies.svg"
   alt="Dependencies in a four-node graph"
   caption="Dependencies and topological order"
%]

</section>
<section class="slide" markdown="1">

## Representing Rules

1.  Invent a special-purpose syntax
    -   Fits the problem
    -   But you need a parser, auto-complete, a debugger, etc.
2.  Use existing syntax
    -   Get tooling for free
    -   But the semantics are invisible to those tools
-   We will use JSON

[%inc double_linear_dep.json %]

</section>
<section class="slide" markdown="1">

## Top-Down Design

-   Start with the big picture

[%inc build_simple.py mark=main %]

1.  Get the configuration
2.  Figure out the update order
3.  Refresh each file (for now, just print action)

</section>
<section class="slide" markdown="1">

## Configuration

[%inc build_simple.py mark=config %]

-   Use a dictionary comprehension
    -   Key is node name (for lookup)
    -   Value contains rule and dependencies

</section>
<section class="slide" markdown="1">

## Check and Build

[%inc build_simple.py mark=check %]

[% figure
   slug="build-diamond"
   img="diamond.svg"
   alt="Representing graph"
   caption="Representing dependency graph"
%]

</section>
<section class="slide" markdown="1">

## Topological Sorting

[% figure
   slug="build-topo-sort"
   img="topo_sort.svg"
   alt="Trace of topological sorting"
   caption="Topological sort"
%]

</section>
<section class="slide" markdown="1">

## Topological Sorting

[%inc build_simple.py mark=sort %]

</section>
<section class="slide" markdown="1">

## Testing

[%inc double_linear_dep.json %]
[%inc double_linear_dep.out %]

</section>
<section class="slide" markdown="1">

## Critique

1.  Configuration might not come directly from a JSON file
    -   So modify constructor to take config as input
2.  Printing actions to the screen isn't very useful
    -   So collect them and return an ordered list of commands
3.  `assert` isn't a friendly way to handle user errors
    -   Raise `ValueError`
4.  Topological sort isn't [% g stable_sort "stable" %]
    -   `dict` is ordered but `set` is not
    -   So sort node names when appending
5.  We might want to add other keys to rules
    -   So put that check in a separate method we can override

</section>
<section class="slide" markdown="1">

## Revise the Big Picture

[%inc build_better.py mark=main %]

</section>
<section class="slide" markdown="1">

## Revise Configuration

[%inc build_better.py mark=config %]

</section>
<section class="slide" markdown="1">

## Revise Topological Sort

[%inc build_better.py mark=sort %]

</section>
<section class="slide" markdown="1">

## Now It's Testable

[%inc test_build_better.py mark=test_circular %]

</section>
<section class="slide" markdown="1">

## Now It's Testable

[%inc test_build_better.py mark=test_no_dep %]

</section>
<section class="slide" markdown="1">

## And Extensible

[%inc build_time.py mark=class %]

</section>
<section class="slide" markdown="1">

## More Testing

[%inc test_build_time.py mark=tests %]

</section>
<section class="slide" markdown="1">

## Summary

[% figure
   slug="build-concept-map"
   img="concept_map.svg"
   alt="Concept map of build manager"
   caption="Concept map."
%]

</section>
