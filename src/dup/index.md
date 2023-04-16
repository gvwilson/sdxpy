---
title: "Finding Duplicate Files"
syllabus:
-   A hash function creates a fixed-size value from an arbitrary sequence of bytes.
-   The output of a hash function is deterministic but not predictable.
-   A cryptographic hash function's output is evenly distributed.
---

## Exercises {: #dup-exercises}

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

FIXME

### Big Oh {: .exercise}

FIXME
