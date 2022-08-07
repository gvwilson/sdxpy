---
title: "Versioned File Backups"
syllabus:
- FIXME
---

Now that we can test software we have something worth saving.
A [%i "version control system" %][%g version_control_system "version control system" %][% /i %]
like [%i "Git" "version control system!Git" %][Git][git][% /i %]
keeps track of changes to files
so that we can recover old versions if we want to.
Its core is a way to archive files that:

1.  records which versions of which files existed at the same time
    (so that we can go back to a consistent previous state), and
2.  stores any particular version of a file only once,
    so that we don't waste disk space.

This chapter will build a tool for doing both tasks.
It won't do everything Git does;
in particular, it won't let us create and merge branches.
If you would like to know how that works,
please see [%i "Cook, Mary Rose" %][Mary Rose Cook's][cook_mary_rose][% /i %]
excellent [Gitlet][gitlet] project.

## How can we uniquely identify files? {: #backup-unique}

To avoid storing redundant copies of files,
we need a way to tell when two files contain the same data.
We can't rely on names because files can be renamed or moved over time;
we could compare the files byte by byte,
but a quicker way is to use a [%i "hash function" %][%g hash_function "hash function" %][% /i %]
that turns arbitrary data into a fixed-length string of bits
([% fixme file-backup-hash-function %]).

[% fixme
   slug="backup-hash-function"
   img="hash-function.svg"
   alt="Hash functions"
   caption="How hash functions speed up lookup."
%]

A hash function always produces the same [%i "hash code" %][%g hash_code "hash code" %][% /i %] for a given input.
A [%i "cryptographic hash function" "hash function!cryptographic" %][%g cryptographic_hash_function "cryptographic hash function" %][% /i %]
has two extra properties:

1.  The output depends on the entire input:
    changing even a single byte results in a different hash code.

1.  The outputs look like random numbers:
    they are unpredictable and evenly distributed
    (i.e., the odds of getting any specific hash code are the same)

It's easy to write a bad hash function,
but very hard to write one that qualifies as cryptographic.
We will therefore use a library to calculate 160-bit [%i "hash code!SHA-1" "SHA-1 hash code" %][%g sha_1 "SHA-1" %][% /i %] hashes for our files.
These are not random enough to keep data secret from a patient, well-funded attacker,
but that's not what we're using them for:
we just want hashes that are random to make [%i "hash function!collision" "collision (in hashing)" %][%g collision "collision" %][% /i %] extremely unlikely.

<div class="callout" markdown="1">

### The Birthday Problem

The odds that two people share a birthday are 1/365 (ignoring February 29).
The odds that they *don't* are therefore 364/365.
When we add a third person,
the odds that they don't share a birthday with either of the preceding two people are 363/365,
so the overall odds that nobody shares a birthday are (365/365)×(364/365)×(363/365).
If we keep calculating, there's a 50% chance of two people sharing a birthday in a group of just 23 people,
and a 99.9% chance with 70 people.

We can use the same math to calculate how many files we need to hash before there's a 50% chance of a collision.
Instead of 365 we use \\(2^{160}\\) (the number of values that are 160 bits long),
and after checking [Wikipedia][wikipedia-birthday-problem]
and doing a few calculations with [%i "Wolfram Alpha" %][Wolfram Alpha][wolfram-alpha][% /i %],
we calculate that we would need to have approximately \\(10^{24}\\) files
in order to have a 50% chance of a collision.
We're willing to take that risk…

</div>

Node's `crypto` module provides tools to create a SHA-1 hash.
To use them,
we create an object that keeps track of the current state of the hashing calculations,
tell it how we want to encode (or represent) the hash value,
and then feed it some bytes.
When we are done,
we call its `.end` method
and then use its `.read` method to get the final result:

[% fixme pat="hash-text.*" fill="js sh out" %]

Hashing a file instead of a fixed string is straightforward:
we just read the file's contents and pass those characters to the hashing object:

[% fixme pat="hash-file.*" fill="js sh out" %]

However,
it is more efficient to process the file as a [%g stream "stream" %]:

[% fixme pat="hash-stream.*" fill="js sh out" %]

This kind of interface is called
a [%i "streaming API" "execution!streaming" %][%g streaming_api "streaming" %][% /i %] [%g api "API" %]
because it is designed to process a stream of data one chunk at a time
rather than requiring all of the data to be in memory at once.
Many applications use streams
so that programs don't have to read entire (possibly large) files into memory.
{: .continue}

To start,
this program asks the `fs` library to create a reading stream for a file
and to [%g pipe "pipe" %] the data from that stream to the hashing object
([% fixme file-backup-streaming %]).
It then tells the hashing object what to do when there is no more data
by providing a [%i "event handler!streaming API" "streaming API!event handler" %][%g handler "handler" %][% /i %] for the "finish" event.
This is called asynchronously:
as the output shows,
the main program ends before the task handling the end of data is scheduled and run.
Most programs also provide a handler for "data" events to do something with each block of data as it comes in;
the `hash` object in our program does that for us.

[%
   fixme
   slug="backup-streaming"
   img="figures/streaming.svg"
   alt="Streaming file operations"
   caption="Processing files as streams of chunks."
%]

## How can we back up files? {: #backup-backup}

Many files only change occasionally after they're created, or not at all.
It would be wasteful for a version control system to make copies
each time the user wanted to save a snapshot of a project,
so instead our tool will copy each unique file to something like `abcd1234.bck`,
where `abcd1234` is a hash of the file's contents.
It will then store a data structure that records the filenames and hash keys for each snapshot.
The hash keys tell it which unique files are part of the snapshot,
while the filenames tell us what each file's contents were called when the snapshot was made
(since files can be moved or renamed).
To restore a particular snapshot,
all we have to do is copy the saved `.bck` files back to where they were
([% fixme file-backup-storage %]).

[% fixme
   slug="backup-storage"
   img="figures/storage.svg"
   alt="Backup file storage"
   caption="Organization of backup file storage."
%]

We can build the tools we need to do this uses promises.
The main function creates a promise that uses the asynchronous version of `glob` to find files
and then:

1.  checks that entries in the list are actually files;

1.  reads each file into memory; and

1.  calculates hashes for those files.

[% fixme file="hash-existing-promise.js" keep="main" %]

This function uses `Promise.all`
to wait for the operations on all of the files in the list to complete
before going on to the next step.
A different design would combine stat, read, and hash into a single step
so that each file would be handled independently
and use one `Promise.all` at the end to bring them all together.
{: .continue}

The first two [%i "helper function" %]helper functions[% /i %] that `hashExisting` relies on
wrap asynchronous operation in promises:

[% fixme file="hash-existing-promise.js" keep="helpers" %]

The final helper function calculates the hash synchronously,
but we can use `Promise.all` to wait on those operations finishing anyway:

[% fixme file="hash-existing-promise.js" keep="hashPath" %]

Let's try running it:

[% fixme pat="run-hash-existing-promise.*" fill="js sh slice.out" %]

The code we have written is clearer than it would be with callbacks
(try rewriting it if you don't believe this)
but the layer of promises around everything still obscures its meaning.
The same operations are easier to read when written using `async` and `await`:

[% fixme file="hash-existing-async.js" keep="main" %]

This version creates and resolves exactly the same promises as the previous one,
but those promises are created for us automatically by Node.
To check that it works,
let's run it for the same input files:
{: .continue}

[% fixme pat="run-hash-existing-async.*" fill="js sh slice.out" %]

## How can we track which files have already been backed up? {: #backup-track}

The second part of our backup tool keeps track of which files have and haven't been backed up already.
It stores backups in a directory that contains backup files like `abcd1234.bck`
and files describing the contents of particular snapshots.
The latter are named `ssssssssss.csv`,
where `ssssssssss` is the [%g utc "UTC" %] [%g timestamp "timestamp" %] of the backup's creation
and the `.csv` extension indicates that the file is formatted as [%g csv "comma-separated values" %].
(We could store these files as [%g json "JSON" %], but CSV is easier for people to read.)

> ### Time of check/time of use
>
> Our naming convention for index files will fail if we try to create more than one backup per second.
> This might seem very unlikely,
> but many faults and security holes are the result of programmers assuming things weren't going to happen.
>
> We could try to avoid this problem by using a two-part naming scheme `ssssssss-a.csv`,
> `ssssssss-b.csv`, and so on,
> but this leads to a [%i "race condition" %][%g race_condition "race condition" %][% /i %]
> called [%i "race condition!time of check/time of use" "time of check/time of use" %][%g toctou "time of check/time of use" %][% /i %].
> If two users run the backup tool at the same time,
> they will both see that there isn't a file (yet) with the current timestamp,
> so they will both try to create the first one.

[% fixme file="check-existing-files.js" %]

To test our program,
let's manually create testing directories with manufactured (shortened) hashes:

[% fixme pat="tree-test.*" fill="sh out" %]

We use Mocha to manage our tests.
Every test is an `async` function;
Mocha automatically waits for them all to complete before reporting results.
To run them,
we add the line:

```js
"test": "mocha */test/test-*.js"
```

in the `scripts` section of our project's `package.json` file
so that when we run `npm run test`,
Mocha looks for files in `test` sub-directories of the directories holding our lessons.
{: .continue}

Here are our first few tests:

[% fixme file="test/test-find.js" %]

and here is Mocha's report:
{: .continue}

[% fixme file="test-check-filesystem.out" %]

## How can we test code that modifies files? {: #backup-test}

The final thing our tool needs to do
is copy the files that need copying and create a new index file.
The code itself will be relatively simple,
but testing will be complicated by the fact
that our tests will need to create directories and files before they run
and then delete them afterward
(so that they don't contaminate subsequent tests).

A better approach is to use a [%i "mock object!for testing" "unit test!using mock object" %][%g mock_object "mock object" %][% /i %]
instead of the real filesystem.
A mock object has the same interface as the function, object, class, or library that it replaces,
but is designed to be used solely for testing.
Node's [`mock-fs`][node-mock-fs] library provides the same functions as the `fs` library,
but stores everything in memory
([% fixme file-backup-mock-fs %]).
This prevents our tests from accidentally disturbing the filesystem,
and also makes tests much faster
(since in-memory operations are thousands of times faster than operations that touch the disk).

[% fixme
   slug="backup-mock-fs"
   img="figures/mock-fs.svg"
   alt="Mock filesystem"
   caption="Using a mock filesystem to simplify testing."
%]

We can create a mock filesystem by giving the library a JSON description of
the files and what they should contain:

[% fixme file="test/test-find-mock.js" omit="tests" %]

[%i "Mocha!beforeEach" %]Mocha[% /i %] automatically calls `beforeEach` before running each tests,
and [%i "Mocha!afterEach" %]`afterEach`[% /i %] after each tests completes
(which is yet another [%i "protocol!for unit testing" %]protocol[% /i %]).
All of the tests stay exactly the same,
and since `mock-fs` replaces the functions in the standard `fs` library with its own,
nothing in our application needs to change either.
{: .continue}

We are finally ready to write the program that actually backs up files:

[% fixme file="backup.js" %]

The tests for this are more complicated than tests we have written previously
because we want to check with actual file hashes.
Let's set up some fixtures to run tests on:

[% fixme file="test/test-backup.js" keep="fixtures" %]

and then run some tests:
{: .continue}

[% fixme file="test/test-backup.js" keep="tests" %]
[% fixme file="test-backup.out" %]

<div class="callout" markdown="1">

### Design for test

One of the best ways---maybe *the* best way---to evaluate software design
is by thinking about [%i "testability!as design criterion" "software design!testability" %]testability[% /i %]
[%b Feathers2004 %].
We were able to use a mock filesystem instead of a real one
because the filesystem has a well-defined API
that is provided to us in a single library,
so replacing it is a matter of changing one thing in one place.
If you have to change several parts of your code in order to test it,
the code is telling you to consolidate those parts into one component.

</div>

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

1.  Modify `backup.js` so that it can save JSON manifests as well as CSV manifests
    based on a command-line flag.

2.  Write another program called `migrate.js` that converts a set of manifests
    from CSV to JSON.
    (The program's name comes from the term [%g data_migration "data migration" %].)

3.  Modify `backup.js` programs so that each manifest stores the user name of the person who created it
    along with file hashes,
    and then modify `migrate.js` to transform old files into the new format.

### Mock hashes {: .exercise}

1.  Modify the file backup program so that it uses a function called `ourHash` to hash files.

2.  Create a replacement that returns some predictable value, such as the first few characters of the data.

3.  Rewrite the tests to use this function.

How did you modify the main program so that the tests could control which hashing function is used?

### Comparing manifests {: .exercise}

Write a program `compare-manifests.js` that reads two manifest files and reports:

-   Which files have the same names but different hashes
    (i.e., their contents have changed).

-   Which files have the same hashes but different names
    (i.e., they have been renamed).

-   Which files are in the first hash but neither their names nor their hashes are in the second
    (i.e., they have been deleted).

-   Which files are in the second hash but neither their names nor their hashes are in the first
    (i.e., they have been added).

### From one state to another {: .exercise}

1.  Write a program called `from-to.js` that takes the name of a directory
    and the name of a manifest file
    as its command-line arguments,
    then adds, removes, and/or renames files in the directory
    to restore the state described in the manifest.
    The program should only perform file operations when it needs to,
    e.g.,
    it should not delete a file and re-add it if the contents have not changed.

2.  Write some tests for `from-to.js` using Mocha and `mock-fs`.

### File history {: .exercise}

1.  Write a program called `file-history.js`
    that takes the name of a file as a command-line argument
    and displays the history of that file
    by tracing it back in time through the available manifests.

2.  Write tests for your program using Mocha and `mock-fs`.

### Pre-commit hooks {: .exercise}

Modify `backup.js` to load and run a function called `preCommit` from a file called `pre-commit.js`
stored in the root directory of the files being backed up.
If `preCommit` returns `true`, the backup proceeds;
if it returns `false` or throws an exception,
no backup is created.
