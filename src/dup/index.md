---
syllabus:
-   A hash function creates a fixed-size value from an arbitrary sequence of bytes.
-   Use big-oh notation to estimate the running time of algorithms.
-   The output of a hash function is deterministic but not predictable.
-   A good hash function's output is evenly distributed.
-   A cryptographic hash function generates a unique identifier for a file's contents.
depends:
---

Suppose we want to find duplicated files,
such as extra copies of photos or data sets.
We can't rely on the files' names;
instead,
we need to compare their contents,
but this will be slow for large files.

A better approach is to generate a shorter identifier for each file
that depends only on the bytes it contains,
then group files with the same identifier and compare those.
This approach is faster because we only compare files that might be equal,
and as we'll see,
we can generate identifiers so that if two files have the same one,
they're (almost) guaranteed to have the same content.

## Getting Started {: #dup-start}

We'll start by implementing the brute force approach
so that we can compare sophisticated designs to it.
The short program below takes a list of filenames from the command line,
finds duplicates,
and prints the matches:

[% inc file="brute_force_1.py" keep="main" %]

The function `same_bytes` reads two files and compares them byte by byte:

[% inc file="brute_force_1.py" keep="bytes" %]

Notice that the files are opened in [%g binary_mode "binary mode" %]
using `"rb"` instead of the usual `"r"`.
As we'll see in [%x binary %],
this tells Python to read the bytes as they are
rather than trying to convert them to characters.
{: .continue}

To test this program and the others we're about to write,
we create a `tests` directory with six files:

| `a1.txt` | `a2.txt` | `a3.txt` | `b1.txt` | `b2.txt` | `c1.txt` |
| ---- | ---- | ---- | ---- | ---- | ---- |
| `aaa` | `aaa` | `aaa` | `bb` | `bb` | `c` |

We expect the three `a` files and the two `b` files to be reported as duplicates.
There's no particular reason for these tests—we just have to start somewhere.
We run our program like this:

[% inc pat="brute_force_1.*" fill="sh out" %]

The output is correct but not useful:
every file is reported as being identical to itself,
and every match of different files is reported twice.
Let's fix the nested loop in `find_duplicates`
so that we only check potentially differing pairs once
([%f dup-triangle %]):

[% inc file="brute_force_2.py" keep="dup" %]

[% figure
   slug="dup-triangle"
   img="triangle.svg"
   alt="Looping over distinct combinations"
   caption="Scoping the inner loop to produce unique combinations."
%]

How much work does our revised program do?
\\( N \\) objects can be paired in \\( N(N-1)/2 \\) ways,
so for large \\( N \\) the work is proportional to \\( N^2 \\).
A computer scientist would say that
the [%g time_complexity "time complexity" %] of our algorithm is \\( O(N^2) \\),
which is pronounced "[%g big_oh "big-oh" %] of N squared".
If the number of files doubles,
the running time roughly quadruples,
which means means that the time per file increases as the number of files increases.
Slowdown like this is often unavoidable,
but in this case there's a better way.

## Hashing Files {: #dup-group}

Instead of comparing every file against every other,
let's process each file once to produce a short identifier
and only compare files with the same identifier
([%f dup-hash-group %]).
If there are \\( g \\) files in each group,
the work will be roughly \\( O(g(N/g)^2) \\)
(i.e., \\( g \\) groups times \\( (N/g)^2 \\) comparisons within each group).
As the number of groups gets larger,
the number of files in each group will hopefully get smaller,
and the overall running time will decrease
*if* the files are evenly distributed between the groups.

[% figure
   slug="dup-hash-group"
   img="hash_group.svg"
   alt="Grouping by hash code"
   caption="Grouping by hash code reduces comparisons from 15 to 4."
%]

We can construct IDs for files using a [%g hash_function "hash function" %]
to produce a [%g hash_code "hash code" %].
Since bytes are just numbers,
we can create a very simple hash function by adding up the bytes in a file
and taking the remainder modulo some number:

[% inc file="naive_hash.py" keep="hash" %]

Here's a quick test that calculates the hash code for
successively longer substrings of the word `"hashing"`:

[% inc file="naive_hash.py" keep="example" %]
[% inc file="naive_hash.out" %]

The output seems random,
but is it?
As a more stringent test,
let's try hashing every line of text in
the [Project Gutenberg][gutenberg] version of the novel *Dracula*
and plot the distribution ([%f dup-naive-dracula %]).

[% figure
   slug="dup-naive-dracula"
   img="naive_dracula.svg"
   alt="Hash codes of *Dracula*"
   caption="Distribution of hash codes per line in *Dracula*."
%]

Is the histogram's peak at zero a flaw of some kind in our hash function?
After a bit of digging,
we realize that
the text file we're processing uses a blank line to separate paragraphs,
so the peak reflects a bias in our data.
If we plot the distribution of hash codes of *unique* lines,
the result is more even ([%f dup-naive-dracula-unique %]).

[% figure
   slug="dup-naive-dracula-unique"
   img="naive_dracula_unique.svg"
   alt="Hash codes of unique lines of *Dracula*"
   caption="Distribution of hash codes per unique line in *Dracula*."
%]

Now that we can hash files,
we can build a dictionary with hash codes as keys
and sets of files as values.
We do this using a common pattern
where if we haven't seen a particular key before,
we add it with an empty value,
then unilaterally add this file to that value
(in this case, a set):

[% inc file="grouped.py" keep="group" %]

We can now re-use most of the code we wrote earlier
to find duplicates within each group:

[% inc file="grouped.py" keep="main" %]
[% inc file="grouped.out" %]

## Better Hashing {: #dup-hash}

Let's go back to the formula \\( O(g(N/g)^2) \\)
that tells us how much work we have to do
if we have divided \\( N \\) files between \\( g \\) groups.
If \\( g \\) and \\( N \\) are equal—i.e.,
if we have exactly as many groups as files—then
the work to process \\( N \\) files would be \\( O(N) \\).
We have to read each file at least once,
so we can't possibly do better than this,
but how can we ensure that each unique file winds up in its own group?

The answer is to use a
[%g cryptographic_hash_function "cryptographic hash function" %].
The output is completely deterministic:
given the same bytes in the same order,
it will always produce the same output.
However,
its output is distributed like a uniform random variable,
and is unpredictable:
given a hash code,
there's no way to figure out what bytes would produce it
other than generating random strings of bytes and hashing them.

Cryptographic hash functions are hard to write—or rather,
it's very hard to prove that a particular algorithm has the properties we require.
We will therefore use a function from Python's [hashing library][py_hashlib]
that implements the [%g sha256 "SHA-256" %] algorithm.
Given some bytes as input,
this function produces a 256-bit hash,
which is normally written as a 64-character [%g hexadecimal "hexadecimal" %] string.
This uses the letters A-F (or a-f) to represent the digits from 10 to 15,
so that (for example) `3D5` is \\((3×16^2)+(13×16^1)+(5×16^0)\\), or 981 in decimal:

[% inc file="using_sha256.py" keep="example" %]
[% inc file="using_sha256.out" %]

<div class="callout" markdown="1">

### The Birthday Problem

The odds that two people share a birthday are 1/365 (ignoring February 29).
The odds that they *don't* are therefore 364/365.
When we add a third person,
the odds that they don't share a birthday
with either of the preceding two people are \\( 363/365 \\),
so the overall odds that nobody shares a birthday are \\( (364/365)×(363/365) \\).
If we keep going,
there's a 50% chance of two people sharing a birthday in a group of just 23 people,
and a 99.9% chance with 70 people.

The same math can tell us how many files we need to hash
before there's a 50% chance of a [%g hash_collision "collision" %] with a 256-bit hash.
According to [Wikipedia][birthday_problem],
the answer is approximately \\( 4{\times}10^{38} \\) files.
We're willing to take that risk…

</div>

Using this function makes our duplicate file finder much shorter:

[% inc pat="dup.*" fill="py sh out" %]

More importantly,
our new approach scales to very large sets of files:
as explained above,
we only have to look at each file once,
so the running time is as good as it possibly can be.

## Summary {: #dup-summary}

Hashing is a tremendously powerful tool:
Python's dictionaries hash their keys to make lookup fast,
and [%i "version control system" %]version control systems[%/i%] use it to determine
when two files or two revisions of a repository are the same or not
([%x archive %]).

But our duplicate file finder is just a beginning.
[%x glob %] shows how we can find sets of files to compare;
[%x test %] and [%x mock %] build tools to test programs like this,
while [%x lint %] explores ways of checking that our programs follow style guidelines.

[% figure
   slug="dup-concept-map"
   img="concept_map.svg"
   alt="Concept map for finding duplicate files"
   caption="Concept map for duplicate file detection with hashing."
%]

## Exercises {: #dup-exercises}

### Odds of Collision {: .exercise}

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

A [%g streaming_api "streaming API" %] delivers data one piece at a time
rather than all at once.
Read the documentation for the `update` method of hashing objects
in Python's [hashing library][py_hashlib]
and rewrite the duplicate finder from this chapter
to use it.

### Big Oh {: .exercise}

[%x intro %] said that as the number of components in a system grows,
the complexity of the system increases rapidly.
How fast is "rapidly" in big-oh terms?

###  The `hash` Function {: .exercise}

-   Read the documentation for Python's built-in `hash` function

-   Why do `hash(123)` and `hash("123")` work but `hash([123])` [%i "raise" %][%/i%] an exception?

### How Good Is SHA-256? {: .exercise}

-   Write a function that calculate the SHA-256 hash code
    of each unique line of a text file.

-   Convert the hex digests of those hash codes to integers.

-   Plot a histogram of those integer values with 20 bins.

-   How evenly distributed are the hash codes?
    How does the distribution change as you process larger files?
