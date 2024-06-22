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
    -   Still worse
-   Look at statistics
    -   `frequencies.py
    -   Lots of words only occur once (long tail)
