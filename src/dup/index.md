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
People often rename files,
so we must compare their contents,
but this will be slow if we have a lot of files.

We can estimate how slow "slow" will be with a simple calculation.
\\( N \\) objects can be paired in \\( N(N-1) \\) ways.
If we remove duplicate pairings
(i.e., if we count A-B and B-A as one pair)
then there are \\( N(N-1)/2 = (N^2 - N)/2 \\) distinct pairs.
As \\( N \\) gets large,
this value is approximately proportional to \\( N^2 \\).
A computer scientist would say that
the [%g time_complexity "time complexity" %] of our algorithm is \\( O(N^2) \\),
which is pronounced "[%g big_oh "big-oh" %] of N squared".
In simpler terms,
when the number of files doubles the running time roughly quadruples,
which means the time per file increases as the number of files increases.

Slowdown like this is often unavoidable,
but in our case there's a better way.
If we generate a shorter identifier for each file
that depends only on the bytes it contains,
we can group together the files that have the same identifier
and only compare the files within a group.
This approach is faster because we only do the expensive byte-by-byte comparison
on files that *might* be equal.
And as we'll see,
if we are very clever about how we generate identifiers
then we can avoid byte-by-byte comparisons entirely.

## Getting Started {: #dup-start}

We'll start by implementing the inefficient \\( N^2 \\) approach
so that we can compare our later designs to it.
The short program below takes a list of filenames from the command line,
finds duplicates,
and prints the matches:

[% inc file="brute_force_1.py" keep="main" %]

This program uses a function called `same_bytes`
that reads two files and compares them byte by byte:

[% inc file="brute_force_1.py" keep="bytes" %]

Notice that the files are opened in [%g binary_mode "binary mode" %]
using `"rb"` instead of the usual `"r"`.
As we'll see in [%x binary %],
this tells Python to read the bytes exactly as they are
rather than trying to convert them to characters.
{: .continue}

To test this program and the others we're about to write,
we create a `tests` directory with six files:

| Filename | `a1.txt` | `a2.txt` | `a3.txt` | `b1.txt` | `b2.txt` | `c1.txt` |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| Content  | `aaa`    | `aaa`    | `aaa`    | `bb`     | `bb`     | `c`      |

We expect the three `a` files and the two `b` files to be reported as duplicates.
There's no particular reason for these tests—we just have to start somewhere.
Our first test looks like this:

[% inc pat="brute_force_1.*" fill="sh out" %]

Our program's output is correct but not useful:
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

## Hashing Files {: #dup-group}

Instead of comparing every file against every other,
let's process each file once to produce a short identifier
that depends only on the file's contents
and then only compare files that have the same identifier,
i.e.,
that *might* be equal.
If files are evenly divided into \\( g \\) groups
then each group will contain roughly \\( N/g \\) files,
so the total work will be roughly \\( O(g(N/g)^2) \\)
(i.e., \\( g \\) groups times \\( (N/g)^2 \\) comparisons within each group).
Simplifying,
this is \\( N^2/g \\),
so as the number of groups grows,
and the overall running time should decrease
([%f dup-hash-group %]).

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

Most of the [%g bucket "buckets" %] are approximately the same height,
but why is there a peak at zero?
Our big-oh estimate of how efficient our algorithm would be
depended on files being distributed evenly between groups;
if that's not the case,
our code won't be as fast as we hoped.

After a bit of digging,
it turns out that
the text file we're processing uses a blank line to separate paragraphs.
These hash to zero,
so the peak reflects an unequal distribution in our data.
If we plot the distribution of hash codes of *unique* lines,
the result is more even ([%f dup-naive-dracula-unique %]).

[% figure
   slug="dup-naive-dracula-unique"
   img="naive_dracula_unique.svg"
   alt="Hash codes of unique lines of *Dracula*"
   caption="Distribution of hash codes per unique line in *Dracula*."
%]

Hashing is a tremendously powerful tool:
for example,
Python's dictionaries hash their keys to make lookup fast.
Now that we can hash files,
we can build a dictionary with hash codes as keys
and sets of filenames as values.
The code that does this is shown below;
each time it calculate a hash code,
it checks to see if that value has been seen before.
If not,
it creates a new entry in the `groups` dictionary
with the hash code as its key
and an empty set as a value.
It can then be sure that there's a set to add the filename to:

[% inc file="grouped.py" keep="group" %]

We can now re-use most of the code we wrote earlier
to find duplicates within each group:

[% inc file="grouped.py" keep="main" %]
[% inc file="grouped.out" %]

## Better Hashing {: #dup-hash}

Let's go back to the formula \\( O(N^2/g) \\)
that tells us how much work we have to do
if we have divided \\( N \\) files between \\( g \\) groups.
If we have exactly as many groups as files—i.e.,
if \\( g \\) is equal to \\( N \\)—then
the work to process \\( N \\) files would be \\( O(N^2/N) = O(N) \\),
which means that the work will be proportional to the number of files.
We have to read each file at least once anyway,
so we can't possibly do better than this,
but how can we ensure that each unique file winds up in its own group?

The answer is to use a
[%g cryptographic_hash_function "cryptographic hash function" %].
The output of such a function is completely deterministic:
given the same bytes in the same order,
it will always produce the same output.
However,
the output is distributed like a uniform random variable:
each possible output is equally likely,
which ensures that files will be evenly distributed between groups.

Cryptographic hash functions are hard to write,
and it's very hard to prove that a particular algorithm has the properties we require.
We will therefore use a function from Python's [hashing module][py_hashlib]
that implements the [%g sha256 "SHA-256" %] hashing algorithm.
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
The odds that they *don't* are therefore \\( 364/365 \\).
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

Using this library function makes our duplicate file finder much shorter:

[% inc pat="dup.*" fill="py sh out" %]

More importantly,
our new approach scales to very large sets of files:
as explained above,
we only have to look at each file once,
so the running time is as good as it possibly can be.

## Summary {: #dup-summary}

[% figure
   slug="dup-concept-map"
   img="concept_map.svg"
   alt="Concept map for finding duplicate files"
   caption="Concept map for duplicate file detection with hashing."
   cls="here"
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
{: .continue}

### Streaming I/O {: .exercise}

A [%g streaming_api "streaming API" %] delivers data one piece at a time
rather than all at once.
Read the documentation for the `update` method of hashing objects
in Python's [hashing module][py_hashlib]
and rewrite the duplicate finder from this chapter
to use it.

### Big Oh {: .exercise}

[%x intro %] said that as the number of components in a system grows,
the complexity of the system increases rapidly.
How fast is "rapidly" in big-oh terms?

###  The `hash` Function {: .exercise}

1.  Read the documentation for Python's built-in `hash` function

1.  Why do `hash(123)` and `hash("123")` work but `hash([123])` [%i "raise" %] an exception?

### How Good Is SHA-256? {: .exercise}

1.  Write a function that calculate the SHA-256 hash code
    of each unique line of a text file.

1.  Convert the hex digests of those hash codes to integers.

1.  Plot a histogram of those integer values with 20 bins.

1.  How evenly distributed are the hash codes?
    How does the distribution change as you process larger files?
