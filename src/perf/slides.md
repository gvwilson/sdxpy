---
template: slides
title: "Performance Profiling"
---

## The Problem

-   We can build dataframes several different ways

-   Which will be most efficient?

-   Find out by doing experiments

---

## What Can Dataframes Do?

[%inc df_base.py %]

---

## Row-wise Storage

-   A list of dictionaries

[% figure
   slug="perf-row-storage"
   img="row_storage.svg"
   alt="Row-wise storage"
   caption="Row-wise storage of a dataframe"
%]

---

## Column-wise Storage

-   A dictionary of lists

[% figure
   slug="perf-col-storage"
   img="col_storage.svg"
   alt="Column-wise storage"
   caption="Column-wise storage of a dataframe"
%]

---

## Row-wise: Starting

[%inc df_row.py mark=top %]
[%inc util.py mark=match %]

---

## Row-wise Operations

[%inc df_row.py mark=simple %]

---

## Row-wise Equality

[%inc df_row.py mark=equal %]

-   Don't rely on implementation details of the other dataframe
-   We might want to compare this dataframe with one that's stored a different way

---

## Row-wise Selection

[%inc df_row.py mark=select %]

[% figure
   slug="perf-row-select"
   img="row_select.svg"
   alt="Row-wise selection"
   caption="Row-wise selection"
%]

---

## How to Filter?

-   User provides `func(red, green)` returning `True` or `False`

-   Need to match column names with parameters

[%inc test_df_row.py mark=fixture %]
[%inc test_df_row.py mark=filter %]

---

## How to Call?

-   Use `**` to [%g spread "spread" %] the row

---

## Row-wise Filter

[%inc df_row.py mark=filter %]

-   Spread the rows out to match

-   Convert the result to a row-wise dataframe

[% figure
   slug="perf-row-filter"
   img="row_filter.svg"
   alt="Row-wise filtering"
   caption="Row-wise filtering"
%]

---

## Column-Wise: Starting

[%inc df_col.py mark=top %]
[%inc util.py mark=eq %]

---

## Column-wise Operations

[%inc df_col.py mark=simple %]

-   Doesn't allow for empty dataframes

---

## Column-wise Selection

[%inc df_col.py mark=select %]

[% figure
   slug="perf-col-select"
   img="col_select.svg"
   alt="Column-wise selection"
   caption="Column-wise selection"
%]

---

## Column-wise Filter

[%inc df_col.py mark=filter %]

[% figure
   slug="perf-col-filter"
   img="col_filter.svg"
   alt="Column-wise filter"
   caption="Column-wise selection"
%]

---

## How to Compare?

-   Select is (probably) fast for column-wise but slow for row-wise

-   Filter is (probably) slower for column-wise than for row-wise

-   Overall performance will depend on the ratio of selects to filters

-   So we do experiments

---

## Experimental Setup

[%inc timing.py mark=create %]

---

## Experimental Setup

[%inc make.out %]

[%inc timing.py mark=filter %]

-   Should vary the filtering criteria, the proportion of rows kept, etc.

---

## So Which Is Better?

| nrow | ncol | filter_col | select_col | filter_row | select_row |
| ---: | ---: | ---------: | ---------: | ---------: | ---------: |
| 10 | 10 | 7.8e-05 | 8.8e-06 | 3.7e-05 | 2.1e-05 |
| 50 | 50 | 6.0e-4 | 1.9e-05 | 3.4e-4 | 2.4e-4 |
| 100 | 100 | 2.2e-3 | 3.5e-05 | 1.3e-3 | 8.4e-4 |
| 500 | 500 | 0.05 | 1.5e-4 | 0.03 | 0.02 |
| 1000 | 1000 | 0.21 | 3.0e-4 | 0.12 | 0.08 |
| 5000 | 5000 | 6.6 | 1.5e-3 | 3.5 | 2.1 |
| 10000 | 10000 | 25.4 | 3.0e-3 | 14.0 | 8.8 |

---

## So Which Is Better?

[% figure
   slug="perf-analysis"
   img="analysis.svg"
   alt="Comparing performance"
   caption="Comparing performance empirically"
%]

---

## Use Tools

-   A [%g profiler "profiler" %] measures where a program spends its time

[%inc profile.sh %]
[%inc profile.out head="10" %]

-   Uh, what is line 7 of `util.py` doing?

---

## The Offending Lines

-   A quarter of our total runtime is calling `dict_match` to check that
    all the rows in a row-wise dataframe
    have the same types for the same keys

-   Surely we can do better…

---

<!--# class="summary" -->

## Summary

[% figure
   slug="perf-concept-map"
   img="concept_map.svg"
   alt="Concept map of performance profiling"
   caption="Concept map."
%]
