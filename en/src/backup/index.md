---
title: "Versioned File Backups"
syllabus:
-   Version control tools use hashing to uniquely identify each saved file.
-   Cryptographic hash functions create identifiers that are randomly distributed and depend on every bit in their input.
-   Hash functions often have streaming interfaces that can process files incrementally.
-   Each snapshot of a set of files is recorded in a manifest.
-   Using a mock filesystem to test version control is safer and faster than using the real thing.
---

We've written almost a thousand lines of Python so far.
We could recreate it if we had to,
but we'd rather not find ourselves in that situation.
We'd also like to be able to see what we've changed,
and to collaborate with other people.
A [%i "version control system" %][%g version_control_system "version control system" %][%/i%]
like [%i "Git" "version control system!Git" %][Git][git][%/i%]
solves all of these problems at once.
It keeps track of changes to files
so that we can see what we've changed,
recover old versions,
and merge our changes with those made by other people.

The core of a modern version control tool
is a way to archive files that:

1.  records which versions of which files existed at the same time
    (so that we can go back to a consistent previous state), and

1.  stores any particular version of a file only once,
    so that we don't waste disk space.

This chapter builds a tool that does both tasks.
It won't create and merge branches,
but that's a relatively straightforward extension:
if you would like to see how it works,
please see [%i "Cook, Mary Rose" %][Mary Rose Cook's][cook_mary_rose][%/i%] [Gitlet][gitlet]
or [%i "Polge, Thibault" %]Thibault Polge[%/i%]'s [Write yourself a Git][write_yourself_a_git].

## Identifying Unique Files {: #backup-unique}

To avoid storing redundant copies of files,
we need a way to know when two files contain the same data.
We can't rely on names because files can be renamed or moved over time;
we could compare the files byte by byte,
but a quicker way is to use a [%i "hash function" %][%g hash_function "hash function" %][%/i%]
that turns arbitrary data into a fixed-length string of bits
([% f backup-hash-function %]).

[% figure
   slug="backup-hash-function"
   img="backup_hash_function.svg"
   alt="Hash functions"
   caption="How hash functions speed up lookup."
%]

A hash function always produces the same [%i "hash code" %][%g hash_code "hash code" %][%/i%] for a given input.
A [%i "cryptographic hash function" "hash function!cryptographic" %][%g cryptographic_hash_function "cryptographic hash function" %][%/i%]
has two extra properties:

1.  The outputs look like random numbers:
    they are unpredictable and evenly distributed
    (i.e., the odds of getting any specific hash code are the same).

1.  The output depends on the entire input:
    changing even a single byte almost certainly changes the hash code.

It's easy to write a bad hash function,
but very hard to write one that meets these two conditions.
We will therefore use Python's [hashlib][py_hashlib] module
to calculate [%i "hash code!SHA256" "SHA256 hash code" %][%g sha256 "SHA256" %][%/i%] hashes of our files.
These are not random enough to keep data secret from a patient, well-funded attacker,
but that's not what we're using them for:
we just want hashes that are random enough to make
[%i "hash function!collision" "collision (in hashing)" %][%g collision "collision" %][%/i%]
extremely unlikely.

<div class="callout" markdown="1">

### The Birthday Problem

The odds that two people share a birthday are 1/365 (ignoring February 29).
The odds that they *don't* are therefore 364/365.
When we add a third person,
the odds that they don't share a birthday with either of the preceding two people are 363/365,
so the overall odds that nobody shares a birthday are (364/365)×(363/365).
If we keep going,
there's a 50% chance of two people sharing a birthday in a group of just 23 people,
and a 99.9% chance with 70 people.

The same math can tell us how many files we need to hash before there's a 50% chance of a collision.
According to [Wikipedia][birthday_problem],
the answer is approximately \\(4{\times}10^{38}\\) files.
We're willing to take that risk…

</div>

To calculate the hash of a file,
we create an object that keeps track of the current state of the hashing calculation
and then feed it some bytes.
When we are done,
we call its `hexdigest` method to  get the final result:

[% inc pat="hash_stream.*" fill="py sh out" %]

To prove that it really does generate a unique code,
let's calculate the hash of the novel *Dracula*:

[% inc pat="hash_stream_dracula.*" fill="sh out" %]

<div class="callout" markdown="1">

### Streaming

This chunk-at-a-time interface is called
a [%i "streaming API" "execution!streaming" %][%g streaming_api "streaming" %][%/i%] [%g api "API" %]
because it processes a stream of data one piece at a time
rather than requiring all of the data to be in memory at once.
Many applications use streams
so that programs don't have to read large files into memory.

</div>

## Saving Files {: #backup-files}

Many files only change occasionally after they're created, or not at all.
It would be wasteful for a version control system to make copies
each time the user saved a snapshot of a project,
so instead our tool will copy each unique file to something like `abcd1234.bck`,
where `abcd1234` is the hash of the file's contents.
It will then keep a record of the filenames and hash keys in each snapshot.
The hash keys tell it which unique files are part of the snapshot,
while the filenames tell us what each file's contents were called when the snapshot was made
(so that files can be moved or renamed).
To restore a particular snapshot,
we will copy the `.bck` files back to where they were
([% f backup-storage %]).

[% figure
   slug="backup-storage"
   img="backup_storage.svg"
   alt="Backup file storage"
   caption="Organization of backup file storage."
%]

The first step is to find all the files in or below a given directory
that we need to save.
The simple pattern matching in Python's [glob][py_glob] module
can do this for us.
If we have this directory structure:

[% inc pat="show_try_glob.*" fill="sh out" %]

then a single call to `glob.glob` will find all the files with two-part names:
{: .continue}

[% inc pat="try_glob.*" fill="py sh out" %]

Let's combine this with our hashing function
to create a table of files and hashes:

[% inc pat="hash_all.*" fill="py sh out" %]

## Testing {: #backup-test}

Before we go any further
we need to figure out how we're going to test our code.
The obvious approach is to create directories and sub-directories
containing some files we can use as [%i "fixture" %]fixtures[%/i%].
However,
we are going to change or delete those files
as we back things up and restore them.
To make sure early tests don't contaminate later ones
we would have to re-create those files and directories after each test.

A better approach is to use a [%i "mock object" %][%g mock_object "mock object" %][%/i%]
instead of the real filesystem ([%x tester %]).
The [pyfakefs][pyfakefs] module replaces key functions like `read`
with functions that act the same
but act on "files" stores in memory
([% f backup-mock-fs %]).
Using it prevents our tests from accidentally disturbing the filesystem;
it also makes tests much faster
since in-memory operations are thousands of times faster than ones that touch the disk.

[% figure
   slug="backup-mock-fs"
   img="backup_mock_fs.svg"
   alt="Mock filesystem"
   caption="Using a mock filesystem to simplify testing."
%]

If we `import pyfakefs`,
we automatically get a fixture called `fs`
that we can use to create files.
We tell [pytest][pytest] we want to use this fixture
by passing it as an argument to our testing function:

[% inc file="test_mock_fs.py" %]

We can use `fs` to create more complicated fixtures of our own
with multiple directories and files:

[% inc file="test_mock_tree.py" %]

and then test that `hash_all` finds all the files:
{: .continue}

[% inc file="test_hash_all.py" omit="change" %]

and that hashes change when files change:
{: .continue}

[% inc file="test_hash_all.py" keep="change" %]

## Tracking Backups {: #backup-track}

The second part of our backup tool keeps track of which files have and haven't been backed up already.
It stores backups in a directory that contains files like `abcd1234.bck`
(the hash followed by `.bck`)
and CSV [%g manifest "manifests" %] that describe the contents of particular snapshots.
The latter are named `ssssssssss.csv`,
where `ssssssssss` is the [%g utc "UTC" %] [%g timestamp "timestamp" %] of the backup's creation.

<div class="callout" markdown="1">

### Time of check/time of use

Our naming convention for index files will fail if we try to create more than one backup per second.
This might seem very unlikely,
but many faults and security holes are the result of programmers assuming things weren't going to happen.

We could try to avoid this problem by using a two-part naming scheme `ssssssss-a.csv`,
`ssssssss-b.csv`, and so on,
but this leads to a [%i "race condition" %][%g race_condition "race condition" %][%/i%]
called [%i "race condition!time of check/time of use" "time of check/time of use" %][%g toctou "time of check/time of use" %][%/i%].
If two users run the backup tool at the same time,
they will both see that there isn't a file (yet) with the current timestamp,
so they will both try to create the first one.
We will look at better schemes in the exercises.

</div>

This function creates a backup:

[% inc file="backup.py" keep="backup" %]

When writing the manifest,
we check that the backup directory exists,
create it if it does not,
and then save the manifest as CSV:
{: .continue}

[% inc file="backup.py" keep="write" %]

We then copy those files that *haven't* already been saved:
{: .continue}

[% inc file="backup.py" keep="copy" %]

Finally,
we could call `time.time()` directly to get the current time,
but we will wrap it up to give ourselves something
that we can easily replace with a mock for testing:
{: .continue}

[% inc file="backup.py" keep="time" %]

Let's do one test with real files:

[% inc pat="test_backup_manual.*" fill="sh out" %]

The rest of our tests use a fake filesystem
and a mock replacement for the `current_time` function
(so that we know what the manifest file will be called).
The setup is:

[% inc file="test_backup.py" keep="setup" %]

and an example of a single test is:
{: .continue}

[% inc file="test_backup.py" keep="test" %]

## Summary {: #backup-summary}

[% figure
   slug="backup-concept-map"
   img="backup_concept_map.svg"
   alt="Concept map of file backup"
   caption="Concept map for hashing-based file backup."
%]

## Exercises {: #backup-exercises}

### Odds of collision {: .exercise}

If hashes were only 2 bits long,
then the chances of collision with each successive file
assuming no previous collision are:

| Number of Files | Odds of Collision |
| --------------- | ----------------- |
| 1               | 0%                |
| 2               | 25%               |
| 3               | 50%               |
| 4               | 75%               |
| 5               | 100%              |

A colleague of yours says this means that if we hash four files,
there's only a 75% chance of any collision occurring.
What are the actual odds?

### Streaming I/O {: .exercise}

Write a small program using `fs.createReadStream` and `fs.createWriteStream`
that copies a file piece by piece
instead of reading it into memory and then writing it out again.

### Sequencing backups {: .exercise}

Modify the backup program so that manifests are numbered sequentially
as `00000001.csv`, `00000002.csv`, and so on
rather than being timestamped.
Why doesn't this solve the time of check/time of use race condition mentioned earlier.

### JSON manifests {: .exercise}

1.  Modify `backup.py` so that it can save JSON manifests as well as CSV manifests
    based on a command-line flag.

2.  Write another program called `migrate.py` that converts a set of manifests
    from CSV to JSON.
    (The program's name comes from the term [%g data_migration "data migration" %].)

3.  Modify `backup.py` programs so that each manifest stores the user name of the person who created it
    along with file hashes,
    and then modify `migrate.py` to transform old files into the new format.

### Mock hashes {: .exercise}

1.  Modify the file backup program so that it uses a function called `ourHash` to hash files.

2.  Create a replacement that returns some predictable value, such as the first few characters of the data.

3.  Rewrite the tests to use this function.

How did you modify the main program so that the tests could control which hashing function is used?

### Comparing manifests {: .exercise}

Write a program `compare-manifests.py` that reads two manifest files and reports:

-   Which files have the same names but different hashes
    (i.e., their contents have changed).

-   Which files have the same hashes but different names
    (i.e., they have been renamed).

-   Which files are in the first hash but neither their names nor their hashes are in the second
    (i.e., they have been deleted).

-   Which files are in the second hash but neither their names nor their hashes are in the first
    (i.e., they have been added).

### From one state to another {: .exercise}

1.  Write a program called `from_to.py` that takes the name of a directory
    and the name of a manifest file
    as its command-line arguments,
    then adds, removes, and/or renames files in the directory
    to restore the state described in the manifest.
    The program should only perform file operations when it needs to,
    e.g.,
    it should not delete a file and re-add it if the contents have not changed.

2.  Write some tests for `from_to.py` using pytest and a mock filesystem.

### File history {: .exercise}

1.  Write a program called `file_history.py`
    that takes the name of a file as a command-line argument
    and displays the history of that file
    by tracing it back in time through the available manifests.

2.  Write tests for your program using pytest and a mock filesystem.

### Pre-commit hooks {: .exercise}

Modify `backup.py` to load and run a function called `pre_commit` from a file called `pre_commit.py`
stored in the root directory of the files being backed up.
If `pre_commit` returns `True`, the backup proceeds;
if it returns `False` or throws an exception,
no backup is created.

### Naming manifests {: .exercise}

1.  How does Git keep track of the manifests that record
    which files are in each snapshot?

1.  Add a simple version of this scheme to the backup tool
    developed in this chapter.
