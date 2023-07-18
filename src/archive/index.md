---
syllabus:
-   Version control tools use hashing to uniquely identify each saved file.
-   Each snapshot of a set of files is recorded in a manifest.
-   Using a mock filesystem to test version control is safer and faster than using the real thing.
-   Operations involving multiple files may suffer from race conditions.
-   Use a base class to specify what a component must be able to do
    and derive child classes to implement those operations.
depends:
-   dup
-   glob
-   reflect
---

We've written almost a thousand lines of Python so far.
We could recreate it if we had to,
but we'd rather not have to.
We'd also like to be able to see what we've changed
and to collaborate with other people.

A [%g version_control_system "version control system" %]
like [%i "Git" url="git" %]
solves all of these problems at once.
It keeps track of changes to files
so that we can see what we've changed,
recover old versions,
and merge our changes with those made by other people.

The core of a modern version control tool
is a way to archive files that:

1.  records which versions of which files existed at the same time,
    so that we can go back to a consistent previous state,
    and

1.  stores any particular version of a file only once,
    so that we don't waste disk space.

This chapter builds a tool that does both tasks.
It won't create and merge branches;
if you would like to see how that works,
please see [%i "Cook, Mary Rose" "Mary Rose Cook's" url="cook_mary_rose" %] [Gitlet][gitlet]
or [%i "Polge, Thibault" "Thibault Polge's" %] [Write yourself a Git][write_yourself_a_git].

## Saving Files {: #archive-files}

Many files only change occasionally after they're created, or not at all.
It would be wasteful for a version control system to make copies
each time the user saved a snapshot of a project,
so instead we will copy each unique file to something like `abcd1234.bck`,
where `abcd1234` is the hash of the file's contents ([%x dup %]).
We will then record the filenames and hash keys in each snapshot:
The hash keys tell us which unique files existed at the time of the snapshot,
while the filenames tell us what each file was called when the snapshot was made.
To restore a particular snapshot,
we will copy the `.bck` files back to their original locations
([%f archive-storage %]).

[% figure
   slug="archive-storage"
   img="storage.svg"
   alt="Backup file storage"
   caption="Organization of backup file storage."
%]

The first step is to find all the files in or below a given directory
that we need to save.
As described in [%x glob %],
Python's [glob][py_glob] module can do this for us.
Let's use this to create a table of files and hashes:

[% inc file="hash_all.py" keep="func" %]

Notice that we're truncating the [%i "hash code" %] of each file
to just 16 [%i "hexadecimal" %] digits.
This greatly increases the odds of [%i "collision (in hashing)" "collision" %],
so real version control systems don't do this,
but it makes our program's output easier to show on screen.
For example,
if our test directory looks like this:

[% inc file="sample_dir.out" %]

then our program's output is:
{: .continue}

[% inc pat="hash_all.*" fill="sh out" %]

## Testing {: #archive-test}

Before we go any further
we need to figure out how we're going to test our code.
The obvious approach is to create directories and sub-directories
containing some files we can use as [%i "fixture" "fixtures" %].
However,
we are going to change or delete those files
as we back things up and restore them.
To make sure early tests don't contaminate later ones
we would have to re-create those files and directories after each test.

As discussed in [%x reflect %],
a better approach is to use a [%i "mock object" %]
instead of the real filesystem.
The [pyfakefs][pyfakefs] module replaces key functions like `open`
with functions that behave the same way
but act on "files" stored in memory
([%f archive-mock-fs %]).
Using it prevents our tests from accidentally disturbing the filesystem;
it also makes tests much faster
since in-memory operations are thousands of times faster than ones that touch the disk.

[% figure
   slug="archive-mock-fs"
   img="mock_fs.svg"
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

## Tracking Backups {: #archive-track}

The second part of our backup tool
keeps track of which files have and haven't been backed up already.
It stores backups in a directory that contains files like `abcd1234.bck`
(the hash followed by `.bck`)
and creates a [%g manifest "manifest" %]
that describe the content of each snapshot.
A real system would support remote storage as well
so that losing one hard drive wouldn't mean losing all our work,
so we need to design our system with multiple back ends in mind.

For now,
we will store manifests in [%i "CSV" %] files named `ssssssssss.csv`,
where `ssssssssss` is the [%g utc "UTC" %] [%g timestamp "timestamp" %]
of the backup's creation.

<div class="callout" markdown="1">

### Time of Check/Time of Use

Our naming convention for manifests will fail
if we try to create two or more backups in the same second.
This might seem unlikely,
but many faults and security holes
are the result of programmers assuming things weren't going to happen.

We could try to avoid this problem by using a two-part naming scheme `ssssssss-a.csv`,
`ssssssss-b.csv`, and so on,
but this leads to a [%g race_condition "race condition" %]
called [%g toctou "time of check/time of use" %].
If two users run the backup tool at the same time,
they will both see that there isn't a file (yet) with the current timestamp,
so they will both try to create the first one.
Ensuring that multi-file updates are [%g atomic_operation "atomic operations" %]
(i.e., that they always behave a single indivisible step)
is a hard problem;
[%g file_locking "file locking" %] is a common approach,
but complete solutions are out of the scope of this book.

</div>

This function creates a backup—or rather,
it will once we fill in all the functions it depends on:

[% inc file="backup.py" keep="backup" %]

Writing a high-level function first
and then filling in the things it needs
is called [%g successive_refinement "successive refinement" %]
or [%g top_down_design "top-down design" %].
In practice,
nobody designs code and then implements the design without changes
unless they have solved closely-related problems before [%b Petre2016 %].
Instead,
good programmers jump back and forth between higher and lower levels of design,
adjusting their overall strategy as work on low-level details
reveals problems or opportunities they hadn't foreseen.
{: .continue}

When writing the manifest,
we check that the backup directory exists,
create it if it does not,
and then save the manifest as CSV:
{: .continue}

[% inc file="backup.py" keep="write" %]

We then copy those files that *haven't* already been saved:
{: .continue}

[% inc file="backup.py" keep="copy" %]

We have introduced several more race conditions here:
for example,
if two people are creating backups at the same time,
they could both discover that the backup directory doesn't exist
and then both try to create it.
Whoever does so first will succeed,
but whoever comes second will fail.
We will look at ways to fix this in the exercises as well.

<div class="callout" markdown="1">

### What Time Is It?

Our `backup` function relies on a [%g helper_function "helper function" %]
called `current_time`
that does nothing but call `time.time` from
[%i "Python standard library" "Python's standard library" %]:

[% inc file="backup.py" keep="time" %]

We could call `time.time` directly,
but wrapping it up like this makes it easier to replace with a mock for testing.
{: .continue}

</div>

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

## Refactoring {: #archive-refactor}

Now that we have a better idea of what we're doing,
we can [%i "refactor" %] to create a [%g base_class "base class" %]
that prescribes the general steps in creating a backup:

[% inc file="backup_oop.py" keep="base" %]

We can then derive a [%i "child class" %]
to archive things locally
and fill in its methods by re-using code from the functions
we have just written.
Once we've done this,
we can create the specific archiver we want with a single line:

[% inc file="backup_oop.py" keep="create" %]

Why go to this trouble?
First,
it makes life easier when we want to write archivers
that behave the same way but work differently.
For example,
we could create an archiver that [%g file_compression "compresses" %]
files as it archives them
by deriving a new class from `ArchiveLocal`
and changing only its `_copy_files` method.

Second,
other code can use an archiver *without knowing exactly what it's doing*.
For example,
the function `analyze_and_save` reads some data,
analyzes it,
saves the results,
and then create an archive of those results.
It doesn't know,
and doesn't need to know,
whether the archive is compressing files,
whether those files are being saved locally or remotely,
or anything else:

[% inc file="backup_oop.py" keep="use" %]

This example highlights one of the great strengths of [%i "object-oriented programming" %].
It's easy to write programs in which new code uses old code;
provided classes and objects are carefully designed,
they allow old code to use new code without being changed.

## Summary {: #archive-summary}

[% figure
   slug="archive-concept-map"
   img="concept_map.svg"
   alt="Concept map of file backup"
   caption="Concept map for hashing-based file backup."
%]

## Exercises {: #archive-exercises}

### Sequencing Backups {: .exercise}

Modify the backup program so that manifests are numbered sequentially
as `00000001.csv`, `00000002.csv`, and so on
rather than being timestamped.
Why doesn't this solve the time of check/time of use race condition mentioned earlier?

### JSON Manifests {: .exercise}

1.  Modify `backup.py` so that it can save [%i "JSON" %] manifests as well as CSV manifests
    based on a command-line flag.

2.  Write another program called `migrate.py` that converts a set of manifests
    from CSV to JSON.
    (The program's name comes from the term [%g data_migration "data migration" %].)

3.  Modify `backup.py` programs so that each manifest stores the user name of the person who created it
    along with file hashes,
    and then modify `migrate.py` to transform old files into the new format.

### Mock Hashes {: .exercise}

1.  Modify the file backup program
    so that it uses a function called `ourHash` to hash files.

2.  Create a replacement that returns some predictable value,
    such as the first few characters of the data.

3.  Rewrite the tests to use this function.

How did you modify the main program
so that the tests could control which hashing function is used?

### Comparing Manifests {: .exercise}

Write a program `compare-manifests.py` that reads two manifest files and reports:

-   Which files have the same names but different hashes
    (i.e., their contents have changed).

-   Which files have the same hashes but different names
    (i.e., they have been renamed).

-   Which files are in the first hash
    but neither their names nor their hashes are in the second
    (i.e., they have been deleted).

-   Which files are in the second hash
    but neither their names nor their hashes are in the first
    (i.e., they have been added).

### From One State to Another {: .exercise}

1.  Write a program called `from_to.py` that takes the name of a directory
    and the name of a manifest file
    as its command-line arguments,
    then adds, removes, and/or renames files in the directory
    to restore the state described in the manifest.
    The program should only perform file operations when it needs to,
    e.g.,
    it should not delete a file and re-add it if the contents have not changed.

2.  Write some tests for `from_to.py` using pytest and a mock filesystem.

### File History {: .exercise}

1.  Write a program called `file_history.py`
    that takes the name of a file as a command-line argument
    and displays the history of that file
    by tracing it back in time through the available manifests.

2.  Write tests for your program using pytest and a mock filesystem.

### Pre-commit Hooks {: .exercise}

Modify `backup.py` to load and run a function called `pre_commit` from a file called `pre_commit.py`
stored in the root directory of the files being backed up.
If `pre_commit` returns `True`, the backup proceeds;
if it returns `False` or throws an exception,
no backup is created.
