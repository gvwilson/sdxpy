---
syllabus:
-   A hash function creates a fixed-size value from an arbitrary sequence of bytes.
-   The output of a hash function is deterministic but not predictable.
-   A cryptographic hash function's output is evenly distributed.
---

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

FIXME

### Big Oh {: .exercise}

FIXME

###  The `hash` Function {: .exercise}

-   Read the documentation for Python's built-in `hash` function

-   Why do `hash(123)` and `hash("123")` work but `hash([123])` raise an exception?

### How Good Is SHA256? {: .exercise}

-   Write a function that calculate the SHA256 hash code
    of each unique line of a text file.

-   Convert the hex digests of those hash codes to integers.

-   Plot a histogram of those integer values with 20 bins.

-   How evenly distributed are the hash codes?
    How does the distribution change as you process larger files?
