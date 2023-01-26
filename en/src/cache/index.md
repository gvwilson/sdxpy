---
title: "A File Cache"
todo: true
syllabus:
-   Software systems often use caches to store a subset of files in order to use less disk space.
-   Caching systems can replace actual files with placeholders containing metadata.
-   Object-oriented systems are often implemented in stages to break large design problems into smaller, more manageable ones.
-   In a good design, derived classes only have to override a few (preferably none) of the methods implemented in parent classes.
-   Implementing a minimum testable class allows early testing of core functionality.
---

Data scientists often want to analyze the same files in several projects.
Those files might be too sensitive or too large to store in version control.
Even when that's not the case,
storing several copies eventually results in someone analyzing an out-of-date version of the data.

Tools like [Git LFS][git_lfs] and [DVC][dvc] are an alternative.
These tools replace the actual data file with a [%g placeholder_file "placeholder file" %]
that contains a unique ID,
such as a hash of the data file's contents
([%f cache-architecture %]).
The placeholder file is small,
so it can be committed to version control,
and if the file it refers to changes,
that change will be visible in the version control history.

[% figure
   slug="cache-architecture"
   img="cache_architecture.svg"
   alt="Cache architecture"
   caption="Architecture of a local file cache."
%]

The data file is stored on a server or in the cloud
and downloaded on demand.
Since the data file might be shared between several projects,
it is usually not downloaded into any particular project.
Instead,
it is stored in a [%g cache "cache" %]
that all projects have access to.
If the cache gets too large,
files in it can be deleted
and re-downloaded later.

This architecture has four parts:
the permanent archive of data files,
an index of all the files it contains,
the cache of locally-available files,
and the placeholder files that are actually saved in version control.
There are several ways to implement each of these,
so our implementation will give us a chance to explore some ideas in object-oriented programming.

## A File Index {: #cache-index}

Let's start by creating the index of archived files.
We need to record each file's unique identifier
and the time it was added to the archive;
we could define a class for this,
but since instances of that class are just passive data records,
we use a [%g named_tuple "named tuple" %] instead:

[% inc file="index_base.py" keep="tuple" %]

Next,
we create an [%g abstract_class "abstract class" %]
that defines the operation an index can do,
but doesn't actually implement them—or rather,
only implements the ones that can be defined in terms of lower-level operations
that derived class will implement:

[% inc file="index_base.py" keep="class" %]

The methods of `IndexBase` can:
{: .continue}

-   get and set the directory where the index file is stored;
-   check if a particular file is known (using its identifier, not its name);
-   get a list of all known files (again, by identifier rather than name); and
-   add an identifier to the index with a timestamp.

These methods rely on three abstract methods to
initialize the index if it doesn't already exist,
load the index,
and save the index.
Their definitions are:
{: .continue}

[% inc file="index_base.py" keep="abstract" %]

Finally,
we define a function `current_time`
that returns a time we can use in an index record.
Doing this gives us something that will be easy to mock for testing:

[% inc file="index_base.py" keep="time" %]

<div class="callout" markdown="1">

### Naming Things

The index stores files' unique IDs rather than their names
because the latter are unreliable.
A file may be moved or renamed several times within a project,
or may have different names in different projects;
our design therefore relies on something intrinsic to the file
rather than something under the user's control.

The price for this decision is that files' "names" are meaningless.
Whether we use sequence numbers or hashes,
remembering that `health_records.csv` is file 177234
increases the [%g cognitive_load "cognitive load" %] on our users.

</div>

By writing `IndexBase`,
we have turned a large, amorphous design problem
into a smaller and more focused one
([%f cache-methods %]).
For example,
if we decide to store the index as a JSON file or in a SQLite database,
we should only need to provide the methods to handle that file format;
we should not need to re-write or re-test any of the other methods.
This rule gives us a way to evaluate our designs:
the fewer methods we have to override,
the better the original division of labor was.

To try it out,
let's implement a concrete index class that stores data in a CSV file.
`load` checks that the cache directory exists
and that it contains an index file,
then reads that file and turns its contents into `CacheEntry` records:

[% inc file="index_csv.py" keep="load" %]

[% figure
   slug="cache-methods"
   img="cache_methods.svg"
   alt="Cache index methods"
   caption="Calling relationships between cache index methods."
%]

Similarly,
`save` checks that the cache directory exists
and then writes each record to the index file.
This method automatically creates the index file
if it doesn't already exist:

[% inc file="index_csv.py" keep="save" %]

Finally,
we need to write `_initialize_index`,
which is called by the `set_index_dir` method in the base class
rather than being invoked directly by the user.
While we're doing that,
we'll define the name for the index file
and write a helper method that produces its full path:

[% inc file="index_csv.py" keep="helper" %]

Time to do some testing.
As in [%x backup %],
we will use [pyfakefs][pyfakefs] instead of creating files on disk
and pytest's `fixture` decorator to set things up:

[% inc file="test_index_csv.py" keep="setup" %]

If we create a new cache,
it should be empty:

[% inc file="test_index_csv.py" keep="new" %]

If we add an entry,
it should still be there when we reload the index:
{: .continue}

[% inc file="test_index_csv.py" keep="save" %]

And if we check whether or not something is in the index,
the answer should be "yes" for things we've added
and "no" for things we haven't:

[% inc file="test_index_csv.py" keep="check" %]

## A Local Cache {: #cache-local}

Just as `IndexBase` defined the behavior every cache index must have,
`CacheBase` defines the required behavior of caches themselves.
As the listing below shows,
it is less than three dozen lines long:

[% inc file="cache_base.py" keep="class" %]

`CacheBase` encapsulates several design decisions.
Cached files are named <code><em>identifier</em>.cache</code>,
and are all stored in a single directory.
This scheme works well if the cache only ever has a few thousand files,
but if that number might grow into the tens or hundreds of thousands,
we might want to divide the cached files between several sub-directories
(which is what most browsers do).

All of `CacheBase`'s operations are implemented in terms of
an index derived from `IndexBase`,
a helper method that makes a file identifier by hashing the file's contents,
another helper method that constructs the path to a cached file,
and a single abstract method called `_add`
that actually adds a file to the cache.
`CacheBase` *doesn't* rely on how the index is implemented,
which means we can defer making that decision until we absolutely have to.
Equally,
encapsulating the specifics of file storage in a single method
allows us to do most of the implementation
before figuring that out.

With `CacheBase` in place,
we can create a class called `CacheFilesystem`
that copies files to the local cache
but doesn't actually archive them anywhere:

[% inc file="cache_filesystem.py" keep="class" %]

A file archiving system that doesn't actually archive files
isn't particularly useful in practice,
but it enables us to write some useful tests.
Developers often create
a [%i "minimum testable class" %][%g minimum_testable_class "minimum testable class" %][%/i%]
for this reason.
Just as creating an abstract base class that implements operations
in terms of a small number of methods
helps us break a design problem into smaller, more manageable pieces,
building a minimum testable class
enables us to check some things right away
so that we can focus later testing effort
on implementation-specific details.

By now our testing should look familiar.
We create a fixture for the filesystem as a whole
and another for the cache:

[% inc file="test_cache_filesystem.py" keep="setup" %]

and then write a test to check that
if we haven't ever added files to the cache,
no files are present:
{: .continue}

[% inc file="test_cache_filesystem.py" keep="empty" %]

We can then start testing that (for example)
if we add two files with different names,
the cache contains two files:

[% inc file="test_cache_filesystem.py" keep="two" %]

## A Limited Cache {: #cache-limit}

The next step is to archive all the files remotely
and only cache a few locally.
We will simulate remote storage using a second directory on our own machine,
and limit the number of files in the cache
rather than their total size;
we'll look at a size-based cache in the exercises.

<div class="callout" markdown="1">

### Figure It Out Later

As soon as we start storing files on remote servers,
we need to figure out how to [%g authentication "authenticate" %] the user,
i.e.,
how to establish that they are who they say they are.
Again,
building our system piece by piece lets us sort out other details now
and worry about those ones later.
We are taking a risk, though:
it's possible that we won't be able to extend our design to handle those extra requirements,
but will instead have to tear it down and start over.
Experience is the only reliable guide;
the real aim of lessons like this one is
to pass on experience so that the next person doesn't have to step on all the landmines themselves.

</div>

Our new class `CacheLimited` needs:

-   an index to keep track of files;
-   the path to the cache directory;
-   the path to the archive directory
    that we're using to simulate remote storage;
    and
-   the maximum number of files the cache is allowed to contain.

Its constructor is therefore:

[% inc file="cache_limited.py" keep="constructor" %]

At this point we are going to do something that
we said earlier we wouldn't need to do.
`CacheBase` defines a method `get_cache_path`,
and `CacheFilesystem` used that method without altering it.
In contrast,
our new `CacheLimited` class overrides it
to ensure there's a local copy of a file
whenever we want to read it.
In doing so,
`get_cache_path` ensures that
the cache has enough space for that file.
More specifically,
if we add a file when the cache is full,
`CacheLimited` will:

-   delete a file from the cache;
-   add the new file to the cache; and
-   add it to archival storage.

[% inc file="cache_limited.py" keep="get" %]

The method that ensures the cache has space for a new file
checks the cache's size
and removes a file if necessary:

[% inc file="cache_limited.py" keep="ensure" %]

We also need to implement `_add`
to handle the case of adding an entirely new file

[% inc file="cache_limited.py" keep="add" %]

The tests for `CacheLimited` look like those we've written before:

[% inc file="test_cache_limited.py" keep="example" %]

One difference is that they check the archive directory
as well as the cache directory.
To do this,
the tests may use a method like `_make_archive_path`
that isn't intended for general consumption.
Application programs should never do this,
but it's generally regarded as acceptable for tests
(not least because the alternative is
to make that "private" method generally available).

## Placeholders {: #cache-placeholders}

The last thing we need for a fully-functional repository-friendly file-caching system is
a reliable way to create the placeholder files
that take the place of actual data files in version control.
Each file holds a cache entry identifier,
so if we do our job properly,
users will never need to see these or remember them.

Python provides an `open` function for opening files,
so we will create a `cache_open` function to open cached files:

[% inc file="cache_io.py" keep="open" %]

If the actual file is called `a.txt`,
this function looks for `a.txt.cache`,
reads the file identifier from it,
uses that to find the path to the cached file,
and opens that file for reading.
We don't allow users to open files for writing,
since that would almost certainly put the file's contents
out of step with its identifier.
This restriction is similar to Python's requirement that
dictionaries' keys be [%g immutable "immutable" %];
we will explore alternatives in the exercises.

`cache_save` is the complement to `cache_open`.
Given the name of a local file that the user wants to cache,
this function saves it in the cache
and constructs a placeholder file:

[% inc file="cache_io.py" keep="save" %]

These two functions work as designed,
but neither should be used in production.
The problem is that neither guarantees
[%i "atomic operation" %][%g atomic_operation "atomic operation" %][%/i%]:
in both cases,
if something goes wrong part-way through the function,
the caching system can be left in an inconsistent state.
While there's no obvious way for these functions to fail mid-flight,
there's always the possibility of a power failure
or of the user typing Control-C to interrupt the program
at just the wrong spot.
Tools like [DVC][dvc] do a lot of extra work
to guarantee that this can't happen.

## Summary {: #cache-summary}

[% figure
   slug="cache-concept-map"
   img="cache_concept_map.svg"
   alt="Concept map for file cache"
   caption="Concepts for file cache."
%]

## Exercises {: #cache-exercises}

### An alternative index {: .exercise}

Create a new class `IndexJSON` that stores the index as a JSON file
instead of as CSV.
You should be able to use your new class with the existing cache classes
without changing the latter.

### Another alternative index {: .exercise}

Create a new class `IndexSQLite` that stores the index in a [SQLite][sqlite] database
instead of as CSV.
You should be able to use your new class with the existing cache classes
without changing the latter.

### Consolidation {: .exercise}

Write a tool that finds all the placeholder files in a project
and copies the files they refer to from the cache into the project,
deleting placeholders as it does so.

### Cache size {: .exercise}

1.  Modify the cache so that it only stores files up to a specified total size.
1.  How should the cache decide which files to delete
    when a new file would put it over its size limit?
1.  What should the cache do if someone tries to add a file
    that is larger than the size limit?

### Least recently used {: .exercise}

1.  Modify the cache and index to keep track of when files are used
    as well as when they are created.
1.  Modify the cache cleanup code to delete least recently used file
    when extra space is needed.

### Compressing files {: .exercise}

1.  Modify the system to compress files when they are archived.
    Use Python's [zipfile][py_zipfile] module to handle compression.

2.  Modify the system again so that users can specify
    whether files should be compressed in both the archive and the cache,
    only compressed in the archive,
    or never compressed.

### Reading cached files {: .exercise}

Modify `cache_open` so that files can be opened in binary mode
and so that the function can be used in `with` statements.
(Hint: look up [%g context_manager "context manager" %].)

### Storing files remotely {: .exercise}

1.  Create a small web server ([%x server%]) that accepts
    file upload and file download requests.
1.  Modify the cache so that it sends new files to the server
    and downloads files from the server on demand.

### Commenting {: .exercise}

1.  Modify the system so that users can add comments about files
    in the local placeholder files.

2.  Suppose two projects A and B are stored in separate version control repositories,
    but use the same data files.
    If comments are stored in placeholder files
    then comments saved in A won't be visible in B and vice versa.
    How could you modify your solution to part 1 to enable inter-project sharing of comments?

### Appending {: .exercise}

Modify the system so that users can append data to existing files:

1.  Each placeholder file stores the IDs of one or more cached files
    and the number of bytes in each.

2.  When a user wants to read from a file,
    they may specify a byte offset from the start of the (logical) file
    where reading is to start.

3.  When a user opens a file for appending,
    another chunk is created in the cache
    and writes are appended to it.
    When they close the file,
    an entry is added to the placeholder file
    with information about the new chunk.
