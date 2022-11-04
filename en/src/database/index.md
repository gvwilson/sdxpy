---
title: "A Database"
syllabus:
- FIXME
---

-   [%i "Stack, Connor" %]Connor Stack[%/i%]'s [Let's Build a Simple Database][db_tutorial] tutorial
-   https://fly.io/blog/sqlite-internals-btree/
-   https://fly.io/blog/sqlite-internals-rollback-journal/

## In Memory {: #database-memory}

-   Fixed structure, single table
    -   `userid`: 32-bit integer
    -   `username`: 16-byte string (note: bytes not characters)
    -   `timestamp`: 32-bit integer
-   Use `struct` to pack and unpack
    -   Get rid of 0 bytes from username when unpacking

[% inc file="util.py" %]

-   `PageMemory` stores as many records as it can
    -   Its size matches that of the filesystem for maximum efficient

[% inc file="page_memory.py" %]

-   `DbMemory` handles an append-only set of pages
    -   Add a new page if necessary to store an additional record
    -   Calculate which page and where when retrieving a record

[% inc file="db_memory.py" %]

## On Disk {: #database-file}

-   `PageFile` knows which page it is and can save and load itself

[% inc file="page_file.py" %]

-   `DBFile` still keeps all pages in memory, but can also fill and flush
    -   Caches pages by page number
    -   `_ensure_space` adds a page if necessary
    -   `_ensure_in_memory` is mostly a placeholder for future work
        -   We didn't create it until we started on the next version
    -   The current page is the one with the highest page number

[% inc file="db_file.py" %]

## Swapping Pages {: #database-swap}

-   Use the same `PageFile` structure
-   `_ensure_in_memory` and `_ensure_space` now also call `_maintain_cache`
-   If there are too many pages, drop one
    -   But *not* the current page (yes, we made this mistake)
    -   And *not* the page that's just been added (yes, we made this mistake too)
    -   Not tracking how recently pages have been used: do that in exercises

[% inc file="db_swap.py" %]

[% fixme concept-map %]

## Exercises {: #database-exercises}
