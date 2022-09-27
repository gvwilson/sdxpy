---
title: "A File Cache"
syllabus:
- FIXME
---

-   Data scientists often want to analyze the same files in several projects
    -   Those files might be too sensitive or too large to store in version control
    -   And shouldn't be duplicated anyway
-   Tools like [Git LFS][git_lfs] and [DVC][dvc] are an alternative
    -   Replace the file with a marker containing a unique ID
    -   Store the file in the cloud using that ID
    -   Create a cache of recently-used files
-   Our system has several parts
    -   The permanent archive
    -   An index of all the files it contains
    -   The local cache
    -   The replacements in version control
-   Several ways to implement each of these
    -   Which gives us a chance to explore some ideas in object-oriented programming

## A File Index {: #cache-index}

-   `index_base.py`
-   Define a named tuple `CacheEntry` to record identifier (hash) and timestamp (when file added)
-   Create a base class that specifies all the operations a file index can do
    -   Get and set the directory where the index file is stored
    -   Check if a particular file is known (using its identifier, not its name)
    -   Get a list of all known files (by identifier, not name)
    -   Add an identifier to the index (with a timestamp)
    -   Three abstract methods:
	-   Initialize the index if it doesn't already exist
        -   Load the index
	-   Save the index
    -   Note: create a function `current_time` rather than using `datetime.now` to simplify mocking

-   `index_csv.py`
-   Specifies that the index is stored in `index.csv` in the index directory
-   Loads the index by reading the CSV file and converting rows to `CacheEntry`
-   Saves the index
-   Creates an empty CSV file if necessary

-   `test_index_csv.py`
-   Can we load the index immediately (i.e., is it automatically created)?
-   Can we save and inspect entries?

## A Local Cache {: #cache-local}

-   `cache_base.py` defines behavior every cache must have
    -   How are cached files named? (identifier plus `.cache` suffix)
    -   Add a local file to the cache if it isn't already there
        -   Relies on abstract method `_add` that does everything that won't be common to all implementations
    -   Get the path to a local (cached) copy of a file given its identifier
    -   Does the cache have a particular file and what files are known?
        -   Relies on the index
	-   Which is hidden from the user: has-a rather than is-a or exposing components
-   `cache_filesystem.py` copies files to the cache but doesn't do anything else
    -   Primarily for testing
    -   But useful in its own right (use it to share large files between projects on the same machine)
-   `test_cache_filesystem.py`
    -   Is the cache initially empty?
    -   Can we add files?
    -   Can we find files we've added?
-   Note: so far it's up to the user to remember the mapping between `name.txt` and `abcd1234`
    -   We'll fix this soon

## A Limited Cache  {: #cache-limit}

-   Next step is to store all the files remotely and only store a few locally
-   We will simulate cloud storage using a second directory on our own machine
-   And put a limit on the size of the local cache
    -   Should be based on total size of files
    -   For simplicity, we will limit it by the number of files
-   `CacheLimited` has two copies of `abcd1234.cache`
    -   One in the cache directory (which will be present in the final system)
    -   One in the archive directory (which will probably be remote in the final system)
-   If we add a file when the cache is full
    -   Delete a file from the cache
    -   Add the new file to the cache
    -   Add it to archival storage
-   If we try to access a file that isn't in the cache when the cache is full
    -   Delete a file from the cache
    -   Copy the file from archival storage to the cache
-   Where does the index live?
    -   For the moment we'll keep a single copy in the archive directory

## Markers {: #cache-markers}

-   Create files in repositories that hold metadata about actual file
    -   In our case, the cache entry identifier
-   `cache_save` saves the actual file in the cache and creates a marker file
    -   Users can now delete the actual file if they want
    -   Or at least add it to `.gitignore` or equivalent
-   `cache_open` opens cached file for reading
    -   Do *not* allow writing: that would put contents out of sync with identifier
    -   Equivalent to mutable dictionary keys

## Exercises {: #cache-exercises}

### An alternative index {: .exercise}

Create a new class `IndexJSON` that stores the index as a JSON file
instead of as CSV.
You should be able to use your new class with the existing cache classes
without changing the latter.

### Another alternative index {: .exercise}

Create a new class `IndexSQLite` that stores the index in a SQLite database
instead of as CSV.
You should be able to use your new class with the existing cache classes
without changing the latter.

### Least recently used {: .exercise}

1.  Modify the cache and index to keep track of when files are used
    as well as when they are created.
1.  Modify the cache cleanup code to delete least recently used file
    when extra space is needed.

### Cache size {: .exercise}

1.  Modify the cache so that it only stores files up to a specified total size.
1.  How should the cache decide which files to delete
    when a new file would put it over its size limit?
1.  What should the cache do if someone tries to add a file
    that is larger than the size limit?

### Reading cached files {: .exercise}

Modify `cache_open` so that files can be opened in binary mode
and so that the function can be used in `with` statements.
(Hint: look up [%g context_manager "context manager" %].)

### Storing files remotely {: .exercise}

1.  Create a small web server ([%x server%]) that accepts
    file upload and file download requests.
1.  Modify the cache so that it sends new files to the server
    and downloads files from the server on demand.
