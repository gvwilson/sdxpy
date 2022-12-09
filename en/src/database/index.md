---
title: "A Database"
syllabus:
- FIXME
---

The introduction said that this book would focus on tools programmers use themselves,
so a database may seem a little out of place.
However,
issue trackers, logging frameworks, and many other tools are built on top of databases,
and their implementation is a good way to introduce a few new ideas.
This chapter therefore shows how to build a
[%i "log-structured database; database!log-structured" %][%g log_structured_db "log-structured database" %][%/i%]
with four key features:

1.  It uses [%i "row-wise storage; storage!row-wise" %][%g row_wise "row-wise" %][%/i%] storage
    ([%x dataframe %]),
    i.e.,
    the values in each record are stored together.

2.  The [%i "database index; index!database" %][%g index_database "index" %][%/i%]
    is stored in memory.

3.  Existing records are never overwritten.
    Instead,
    new data is appended to the end of the database.

Our implementation is based on
[%i "Stack, Connor" %]Connor Stack[%/i%]'s [Let's Build a Simple Database][db_tutorial] tutorial
and on [%i "Johnson, Nick" %]Nick Johnson[%/i%]'s article on
[log-structured storage][log_structured_storage].

## In Memory {: #database-memory}

To keep things simple,
our database will store a single table with three fields
([%f database-record %]):

-   `userid`: a 32-bit integer.
-   `machine`: a 16-byte string recording the name of a computer that user accessed.
    Note that the size is specified in bytes not characters;
    when we translate from [%i "Unicode" %]Unicode[%/i%] to bytes,
    we have to make sure the result is no larger than this.
-   `timestamp`: a 32-bit integer representing the time the user accessed the machine.

[% figure
   slug="database-record"
   img="database_record.svg"
   alt="Database record structure"
   caption="The structure of a single binary database record."
%]

As we saw in [%x binary %],
we can use Python's [struct][py_struct] module
to pack data into a binary record
and unpack those records to recover the values.
Let's define a couple of functions to do this,
along with a third function to report the size of each binary record:

[% inc file="util.py" omit="exception" %]

<div class="callout" markdown="1">

### Null bytes

The function `record_unpack`
includes the expression `machine.split(b"\0", 1)[0]`.
To see why,
have a look at this short program and its output:

[% inc pat="null_bytes.*" fill="py out" %]

`FORMAT` specifies that strings are stored in 8 bytes.
When we store a string that's shorter than this,
the struct module fills the trailing bytes with zero,
which is sometimes called a [%g null_byte "null byte" %].
When we unpack the data,
those null bytes are retained and wind up in our final string.
To get rid of them,
we have to split the buffer of packed data at the first null byte
and convert whatever comes before it
rather than converting the whole buffer.

</div>

Now that we have a way to represent records,
we need to think about how to store large numbers of them.
We will use fixed-size blocks of memory called
[%i "page (in database)" %][%g page "pages" %][%/i%] for this,
and pack as many records into each page as can fit
([%f database-packing %].

[% figure
   slug="database-packing"
   img="database_packing.svg"
   alt="Packing records into pages"
   caption="Packing database records into pages."
%]

Each time we want to append a record to the database,
we check how much space is left in the current page.
If the record fits, we add it;
if not,
we start a new page.
If an application wants a record,
it provides the record's index;
after checking that it's valid,
we multiply the index by the record size
to find the starting location of the record in memory.
The whole class is:

[% inc file="page_memory.py" %]

<div class="callout" markdown="1">

### Choosing a page size

Every computer's filesystem manages storage using pages
like the ones we've just created.
These pages are typically four kilobytes,
which means the basic unit of file I/O is that large.
Databases typically use the same size for their pages
to make data transfer as efficient as possible.

</div>

While `PageMemory` stores a page of records,
`DBMemory` stores a list of pages.
The last page in the list,
called the [%i "open page" %][%g open_page "open page" %][%/i%],
is the only one the database can write to.
When an application wants to add a record,
`DBMemory` either appends it to the open page
or adds a new page to the end of the list:

[% inc file="db_memory.py" keep="class" %]

Equally,
when an application wants to retrieve a record,
`DBMemory` figures out which page that record must lie in
and asks the page to get it:

[% inc file="db_memory.py" keep="get" %]

[% figure
   slug="database-retrieve"
   img="database_retrieve.svg"
   alt="Retrieving database records"
   caption="Retrieving records from a paged database."
%]

## On Disk {: #database-file}

A database that only stores things in memory isn't particularly useful.
What we want is something that will save data to disk automatically,
and reload data on demand.
Let's extend `PageMemory` to create a new class `PageFile`
that can do this:

[% inc file="page_file.py" %]

`PageFile` also keeps track of which page it is,
i.e.,
whether it is the first, the second, and so on.
Storing this information simplifies bookkeeping later on.
{: .continue}

`DBFile` is the counterpart to `PageFile`,
but after a bit of work we decided to write it from scratch
rather than extending `DBMemory`.
While the two database classes have some methods in common,
every single one of `DBMemory`'s would have to be overridden
to create `DBFile`.

`DBFile` still keeps all pages in memory,
but can also write them to disk and refill them when asked to.
It caches pages by page number:
`_ensure_space` adds a page if necessary;
the open page is the one with the highest page number at any time.
`_ensure_in_memory` is a placeholder for future work.
(We actually didn't create it until we started on the next version.)

[% inc file="db_file.py" %]

## Swapping Pages {: #database-swap}

Databases exist in part because many datasets won't fit in memory.
The third step in building our database is therefore
to store only a subset of pages in memory at any time.
We will use the same `PageFile` structure,
but modify `DBFile` so that
`_ensure_in_memory` and `_ensure_space` call a new method `_maintain_cache`.
If there are too many pages in memory when we try to read or add a record,
`_maintain_cache` drops a page–but not the current page (yes, we made this mistake).
And not the page that's just been added (yes, we made this mistake too).

[% inc file="db_swap.py" %]

While it's an improvement over its predecessors,
`DBSwap` does not track how recently pages have been used,
which means it is susceptible to [%i "thrashing" %][%g thrashing "thrashing" %][%/i%]:
we could load a page into memory,
dump it,
immediately re-load it,
dump it again,
and so on.
As in [%x cache %],
we will explore ways to address this in the exercises.

## Summary {: #database-summary}

[% figure
   slug="database-concept-map"
   img="database_concept_map.svg"
   alt="Concept map for databases"
   caption="Concepts for databases."
%]

## Exercises {: #database-exercises}
