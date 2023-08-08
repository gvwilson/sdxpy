---
syllabus:
-   Database stores records so that they can be accessed by key.
-   Log-structured database appends new records to database and invalidates older versions of records.
-   Classes are data structures that can be saved like any other data.
-   The filesystem saves data in fixed-size pages.
-   We can improve the efficiency of a database by saving records in blocks.
status: "revised 2023-08-08"
depends:
-   persist
-   binary
-   reflect
---

Persisting objects ([%x persist %]) lets us save and restore program state,
but we often want to be able to look things up quickly
without reloading all of our data.
We would also like applications written in different languages
to be able to get at our data,
which might be easier if we choose a different storage format.

This chapter therefore builds a very simple
[%g log_structured_db "log-structured database" %].
The phrase "log-structured" means that records a log of operations,
i.e.,
every new [%i "record" %] is appended to the end of the database.
Programmers have invented many other ways to store large amounts of data,
but this is one of the easiest to understand.

## Starting Point {: #db-start}

Our starting point is
a simple [%g key_value_store "key-value store" %]
that lets us save records and look them up later.
To use it,
we have to provide a function that takes a record
and returns its key.
We store that function in the `Database` object for later use:

[% inc file="interface_original.py" %]

If we want a dictionary that only stores things in memory,
we can derive a class from `Database`
that uses a dictionary with the values returned by
the user's key function for lookup
([%f db-memory %]):

[% inc file="just_dict_original.py" %]

[% figure
   slug="db-memory"
   img="memory.svg"
   alt="In-memory database"
   caption="Storing a database as a single dictionary in memory."
%]

This simple class is enough to let us start writing some tests.
Let's create a class to store experimental records:

[% inc file="record_original.py" omit="omit" %]

and use the `pytest.fixture` [%i "decorator" %] ([%x protocols %])
to create a database and two records:
{: .continue}

[% inc file="test_db_original.py" keep="fixture" %]

Our first few tests are then:
{: .continue}

[% inc file="test_db_original.py" keep="test" %]

Our next step is to save the user's records in the database
without tying the database to a particular type of record.
The cleanest way to solve this problem is
to require records to know how to convert themselves into something storable.
Rather than passing a second function to the database's constructor
we will [%i "refactor" %] the database
so that we pass in the object that represents the record class:

[% inc file="interface.py" %]

We can now refactor our database
to use a [%i "static method" %] of the record class provided to its constructor
when it needs a key:

[% inc file="just_dict_refactored.py" %]

After a bit of refactoring,
our tests work as before.
{: .continue}

## Saving Records {: #db-save}

The next step in building a usable database is to have it store records
rather than just refer to the user's objects.
Since we don't want the database tied to any particular kind of record,
records must know how to pack and unpack themselves.
We could have use the techniques of [%x binary %],
but to make our test and sample output a little more readable,
we will pack numbers as strings
with a [%g null_byte "null byte" %] `\0` between each string:

[% inc file="record.py" keep="pack" %]

The corresponding method to unpack a stored record is:
{: .continue}

[% inc file="record.py" keep="unpack" %]

These records look like the example below
(which uses `.` to show null bytes):

[% inc pat="show_packed_records.*" fill="py out" %]

Notice that our packing and unpacking methods are static,
i.e.,
they're part of the class
but don't require an object to work.
More importantly,
they don't handle strings that contain null bytes.
This limitation wasn't part of our original design,
but is instead an accident of implementation.
We will look at ways around it in the exercises.
{: .continue}

To finish off,
we write methods to pack and unpack multiple records at once
by joining and splitting single-record data:

[% inc file="record.py" keep="multi" %]

and give our record class a static method
that calculates the size of a single record:
{: .continue}

[% inc file="record.py" keep="base" %]

<div class="callout" markdown="1">

### Tradeoffs

We're assuming that every record is the same size.
If we want to save records with variable-length fields such as strings,
we can either set a maximum size and always save that much data
or make our implementation more complicated (and probably slower)
by saving each record's size
and then scanning records in the same way that
we scanned the bytes making up [%i "Unicode" %] characters in [%x binary %].
The first choice spends space (i.e., memory and disk) to save time;
the second spends time to save space.
As [%b Bentley1982 %] pointed out over forty years ago,
a lot of performance optimizations in programming
come down to trading space for time or vice versa.

</div>

## A File-Backed Database {: #db-file}

We now have what we need to extend our dictionary-based implementation
to write records to a file and load them as needed:

[% inc file="file_backed.py" keep="core" %]

This implementation stores everything in a single file,
whose name must be provided to the database's constructor
([%f db-single-file %]).
If that file doesn't exist when the database object is created,
we use `Path.touch` to create an empty file;
either way,
we then load the entire database into memory.
When we add a record,
we save it in the dictionary
and call a [%i "helper method" %] `_save`
to write the entire database back to the file.
When we get a record,
we simply get it from the in-memory dictionary.

[% figure
   slug="db-single-file"
   img="single_file.svg"
   alt="Using a single file"
   caption="Saving the entire database in a single file."
%]

The two helper methods we need to make this work are:

[% inc file="file_backed.py" keep="helper" %]

It isn't very efficient—we are
loading the entire database the first time we want a single record,
and saving the entire database every time we add a record—but
we are getting closer to something we might actually use.

## Playing With Blocks {: #db-block}

How can we make our file-backed implementation more efficient?
One option would be to save each record in a file of its own,
in the same way that we saved each version of a file in [%x archive %].
However,
this strategy won't give us as much of a performance boost as we'd like.
The reason is that computers do file I/O in [%g page "pages" %]
that are typically two or four kilobytes in size.
Even when we want to read a single byte,
the operating system always reads a full page
and then gives us just the byte we asked for.

A more efficient strategy is
to group records together in [%g block_memory "blocks of memory" %],
each of which is the same size as a page,
and create an [%i "index (a database)" "index" %] in memory
to tell us which records are in which blocks.
When we add a record,
we only write its block to disk;
similarly,
when we need a record whose block isn't already in memory,
we only read that block.

At this point we need to address an issue we should have tackled earlier.
How do we handle updates to records?
For example,
suppose we already have a record with the ID 12345;
what do we do when we get another record with the same ID?
If we are storing the entire database in a single dictionary,
the dictionary takes care of that for us,
but if we are storing things in blocks,
we will have multiple dictionaries.

This is where the "log-structured" part of our design comes in.
Whenever we add a record to the database,
we append it to the current block
or start another block if the current one is full
([%f db-alloc %]).
We give each record a sequence number as we add it,
and our overall index keeps track of
the mapping from record IDs to sequence IDs.
Since we know how many records there are in a block,
we can quickly calculate which block contains
the record with a particular sequence ID.

[% figure
   slug="db-alloc"
   img="alloc.svg"
   alt="Mapping records to blocks"
   caption="Mapping records to blocks."
%]

Let's create a new in-memory database
using one dictionary for each block.
The constructor creates `self._next`
to store the sequence ID of the next record,
`self._index` to map record IDs to sequence IDs,
and a list `self._blocks` to store blocks:

[% inc file="blocked.py" keep="class" %]

To add a record, we:

1.  get the sequence ID for the record;

2.  store the key-to-sequence mapping in the index;

3.  find or create the right block; and

4.  add the record.

[% inc file="blocked.py" keep="add" %]

To get a record given a record ID,
we first ask if we even have that record.
If we do,
we:

1.  find its current sequence ID;

2.  find the corresponding block; and

3.  get the record.

[% inc file="blocked.py" keep="get" %]

The three helper methods that `add` and `get` rely on are:

[% inc file="blocked.py" keep="helper" %]

## Persisting Blocks {: #db-persist}

We now have working prototypes of the two parts of our design:
saving data to file
and dividing records into blocks.
In order to combine them,
we will inherit from our block-based implementation
and extend the `add` and `get` methods to save and load data:

[% inc file="blocked_file.py" keep="class" %]

We will explain the call to `self._build_index()` in a few paragraphs.

<div class="callout" markdown="1">

### One at a Time

Exploring ideas one at a time and then combining them
is a common tactic among experienced designers [%b Petre2016 %].
Creating classes like the all-in-one-file database
that we don't put into production
may feel like a waste of time,
but it usually saves us effort in the long run
by reducing [%i "cognitive load" %].

</div>

Saving a block is mostly a matter of bookkeeping at this point.
Given the record,
we figure out which block it does in,
save it,
pack the block,
and write the result to a file:

[% inc file="blocked_file.py" keep="save" %]

Loading involves almost the same steps,
but our implementation splits it into two pieces:

[% inc file="blocked_file.py" keep="load" %]

We put the code to load a single block in a method of its own
because we need to initialize the in-memory index when restarting the database:

[% inc file="blocked_file.py" keep="index" %]

An obvious extension to our design is to save the index
in a separate file
each time we add or modify a record.
However,
we should [%i "profiler" "profile" %] this change before putting it into production
to see if it actually improves performance ([%x perf %]),
since many small writes might cost more than one large multi-file read.
We would also have to do something
to avoid creating a [%i "race condition" %];
as in [%x archive %],
operating on two files (one for the index and one for the block)
could lead to harmful inconsistencies.

## Cleaning Up {: #db-cleanup}

The final step in our implementation is
to clean up blocks that are no longer needed
because we have a more recent version of every record they contain.
Reclaiming unused space this way is another form of
[%g garbage_collection "garbage collection" %].
Python and most other modern languages do it automatically
to recycle unused memory,
but it's our responsibility to do it for the files our database creates.

The steps in cleanup are:

1.  Calculate a new sequence ID for each record.

2.  Figure out which blocks contain records that we need to retain.

3.  Generate new block IDs for those blocks
    while also creating a set of IDs
    of blocks we can delete because all of their records are out of date.

4.  Delete and rename blocks.

5.  Generate a new in-memory index.

The implementation of these steps is mostly a matter of bookeeping:
{: .continue}

[% inc file="cleanup.py" keep="cleanup" %]

This method doesn't [%g compact "compact" %] storage,
i.e.,
it doesn't move records around
to get rid of stale blocks within records.
Production-quality databases do this periodically
in order to use the disk more efficiently;
we will explore this idea in the exercises.

## Summary {: #db-summary}

[% figure
   slug="db-concept-map"
   img="concept_map.svg"
   alt="Concept map for database"
   caption="Concept map for a log-structured database."
   cls="here"
%]

## Exercises {: #db-exercises}

### Packing Null Bytes {: .exercise}

Modify the experimental record class so that records are packed as strings
but can safely contain null bytes.

### Packing in Binary {: .exercise}

1.  Modify the experimental record class so that it packs itself in
a fixed-size binary record.

2.  How does this change the file I/O operations in the database class?

3.  Should those operations be moved into the record class or not?

### Implement Compaction {: .exercise}

Add a static method to the database that compacts blocks,
i.e.,
rewrites all of the blocks so that only live records are stored.

### Save the Index Separately {: .exercise}

1.  Modify the database so that it saves the entire index in single file.

2.  Design and run an experiment to determine
    if this change improves performance or not.
