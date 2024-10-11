---
template: slides
title: "Binary Data"
---

## Why Binary?

-   Operations are much faster
    -   Write addition using textual digits as an exercise
-   Bits take less space
    -   `"10239472"` is 8 bytes, but `10239472` is just 4
-   How would we represent images, audio, or video as characters?

[%inc bird.txt %]

---

## Integers

-   If all we have is 1's and 0's, use base-2
-   9<sub>10</sub> is (1×8)+(0×4)+(0×2)+(1×1) = 1001<sub>2</sub>
-   Can write numbers in binary using `0b` prefix

[%inc binary_notation.py %]
[%inc binary_notation.out %]

---

## Hexadecimal

-   More common to use [%g hexadecimal "hexadecimal" %] (base 16)
-   Digits are 0123456789ABCDEF
-   Each digit represents 4 bits (half a byte)

[%inc hex_notation.py %]
[%inc hex_notation.out %]

---

## Negative Numbers

-   Could use [%g sign_magnitude "sign and magnitude" %]
    -   `0100` is 4
    -   `1100` is -4
-   But:
    -   Gives us two zeroes (one positive, one negative)
    -   Makes the hardware to do arithmetic more complicated

---

## Two's Complement

-   [%g twos_complement "Two's complement" %] wraps around like an odometer

[% table slug="binary-3bit" tbl="3bit.tbl" caption="3-bit integer values using two's complement." %]

---

## Two's Complement

-   Can still determine sign by looking at the first bit

-   But two's complement is asymmetric

-   No positive number to match the largest negative number

---

## Bitwise Operations

-   Operate on corresponding bits in representation

-   `&` (and) is 1 if both bits are 1, 0 otherwise

    -   `0b1100 & 0b1010 == 0b1000`

    -   `12 & 10 == 8`

-   `|` (or) is 1 if *either* bit is 1, 0 otherwise

    -   `0b1100 | 0b1010 == 0b1110`

    -   `12 | 10 == 14`

---

## Bitwise Operations

[% table slug="binary-ops" tbl="bitwise.tbl" caption="Bitwise operations." %]

---

<!--# class="aside" -->

## This Is Not Arithmetic

-   Take a closer look at `~6`

    -   We are using two's complement, so 6 is `0b000…00110`

    -   Its bitwise negation is `0b111…11001`, which is -7

-   Shifting up and down is *almost* like multiplying or dividing by 2

-   But what if the top bit changes?

    -   If we only have 4 bits, `0b1111 >> 1` is `0b0111`, so -1/2 is 7

---

## Storing Numbers

-   C and Fortran store numbers as numbers
-   Python used **boxed values**
    -   Reference count
    -   Type code
    -   Value

[% figure
   slug="binary-boxing"
   img="boxing.svg"
   alt="Boxed values"
   caption="Using boxed values to store metadata."
%]

---

## Storing Arrays

-   The differences are even larger for arrays and lists

[% figure
   slug="binary-arrays"
   img="arrays.svg"
   alt="Boxed arrays"
   caption="Low-level and high-level array storage."
%]

---

## Packing and Unpacking

-   Operations on unboxed (raw) values are much faster
    -   Most numerical libraries written in C or Fortran
    -   Then wrapped in Python or R
-   Need to:
    -   Get data from raw bytes into Python structures
    -   Copy data from Python structures into packed bytes
-   Also do this for efficient storage of large data

---

## The `struct` Module

[%inc pack_unpack.py %]
[%inc pack_unpack.out %]

---

<!--# class="aside" -->

## Hexadecimal Again

-   Not all bytes correspond to common characters

-   So Python uses two-digit hex representation `\xPQ`

-   `\x00` is a [%g null_byte "null byte" %] (value 0)

-   Easy to miss the actual `A` between one `\x00` and the next

---

## Packing With Counts

[%inc pack_count.py %]
[%inc pack_count.out %]

-   Only packs as much as we tell it to

---

## Dynamic Formats

-   Construct format dynamically

[%inc dynamic_format.py %]
[%inc dynamic_format.out %]

---

## Variable-Length Packing

-   Pack strings as a fixed-size count and that many bytes

-   Use `bytes` to convert character string to bytes

[%inc variable_packing.py mark=pack %]

---

## Variable-Length Packing

[%inc variable_packing.py mark=main %]
[%inc variable_packing.out %]

-   First four bytes are the 32-bit integer representation of 6
-   Next six bytes are our characters

---

## Unpacking

[%inc variable_unpacking.py mark=main %]
[%inc variable_unpacking.out %]

---

## Bytes and Text

-   ASCII originally defined 128 7-bit characters
    -   0–31 were [%g control_code "control codes" %]
-   Since bytes have 8 bits, programmers used the values 128–255 however they wanted
-   ANSI standard defined (for example) 231<sub>10</sub> to be "ç"
-   But what about Turkish, Devanagari, kanji, hieroglyphics, …?
    -   Two bytes wouldn't be enough
    -   Four bytes per character would quadruple storage requirements
    -   And would mostly not be needed (by American businesses)

---

## Unicode

-   Define a [%g code_point "code point" %] for every character
    -   U+0065 for an upper-case Latin "A"
    -   U+2605 for a black star &#9733;
-   Define several [%g character_encoding "character encodings" %]
-   UTF-32 uses 32 bits for every character
-   Most popular is [%g utf_8 "UTF-8" %]
    -   Code points 0–127 are stored in a single byte with a leading 0
    -   If the top bit is 1, the number of 1's tells UTF-8 how many bytes there are in the character

---

## Unicode

-   If the first byte is `0b11101101`:
    -   The leading 1 means "multibyte"
    -   The next two bits mean "this is a three-byte character"
    -   The first 0 separates the header from the start of the character
    -   The final `1101` is the first four bits of the character
-   Every [%g continuation_byte "continuation byte" %] starts with `10`
    -   So we can tell if a byte is in the middle of a character

---

## Characters as Bytes

[%inc pack_unicode.py mark=main %]
[%inc pack_unicode.out %]

---

<!--# class="aside" -->

## Binary Mode

-   `open(filename, "r")` converts bytes to characters
    -   And converts Windows line endings `\r\n` to Unix `\n`
-   Use `open(filename, "rb")` to read in [%g binary_mode "binary mode" %]

---

<!--# class="summary" -->

## Summary

[% figure
   slug="binary-concept-map"
   img="concept_map.svg"
   alt="Concept map for binary data"
   caption="Concept map."
%]
