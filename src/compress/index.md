---
title: "File Compression"
abstract: >
    FIXME
syllabus:
-   FIXME
---

[%fixme "create file compressor" %] [%issue 144 %]

-   First idea: number the tokens in the file and replace each with its number
    -   Use blank-nonblank tokenization (which inadvertently captures punctuation)
    -   `compress.py`
    -   Test with text of introduction to this book: makes things worse
-   So store as binary
    -   `binary.py`
    -   Better, but still larger than the original
    -   In fact, our binary compression is worse when tested every chapter
-   Look at statistics
    -   `frequency.py` and `frequency.svg`
    -   Lots of words only occur once (long tail)
    -   Single space occurs over 1600 times
-   Use variable-length encoding [%x binary %]
    -   Use [%g nybble "nybbles" %] (half-bytes)
    -   Most common seven values are 0000 through 0111
    -   Next 49 are (1..., 0...)
    -   343 are (1..., 1..., 0...)
    -   Calculate compression before implementing
    -   `varlen_calc.py` tells us we can get the introduction from 13240 bytes to 10281 (approximately 1.3X)
    -   But `gzip` can do 2.3X: how?
-   [Lempel-Ziv-Storer-Szymanski][lzss]
    -   Use [this tutorial][lzss_tutorial] by [Tim Cogan][cogan_tim]
    -   That's algorithm country rather than software design…
