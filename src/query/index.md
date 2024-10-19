---
title: "A Query Builder"
version: 2
abstract: >
    FIXME
syllabus:
-   FIXME
---

[%fixme "create query builder" %] [%issue 45 %]

-   SQL requires parts of query in an odd order
-   So create [%g active_record "active records" %] using the [%g builder_pattern "Builder" %] pattern
-   Does not scale up to more complex queries
    -   Have to build an expression tree in memory and rearrange clauses for that
-   Thanks to [Mike Bayer][bayer_mike] for advice
-   `select_all.py`: get all rows of table using reflection to get table name
-   `get_metadata.py`: cache table description and convert row tuples to dictionaries
-   `simpler_metadata.py`: let SQLite do that
-   `choose_columns.py`: select columns using immediate string formatting
    -   test get-all case as well as getting specific columns
    -   exercise: re-introduce cached metadata to do error handling
-   `delay_columns.py`: have `query` save the column names for later use in `run` method
    -   complicates things now, but becomes useful later
-   `aggregate.py`: add aggregation
    -   columns can now be string or aggregates
    -   exercise: add group-by
-   `insert.py`: insert values
    -   go back to keeping metadata in class (which may add startup overheads for large programs)
    -   exercise: handle insertion of multiple records
    -   exercise: handle insertion of objects with appropriately-named fields
