---
syllabus:
-   Programs usually store integers using two's complement rather than sign and magnitude.
-   Characters are usually encoded as bytes using either ASCII, UTF-8, or UTF-32.
-   Programs can use bitwise operators to manipulate the bits representing data directly.
-   Low-level compiled languages usually store raw values, while high-level interpreted languages use boxed values.
-   Sets of values can be packed into contiguous byte arrays for efficient transmission and storage.
depends:
-   persist
---

Python and other high-level languages shield programmers from low-level details,
but sooner or later someone has to worry about bits and bytes.
This chapter explores how computers represent numbers and text
and shows how to work with binary data.

## Integers {: #binary-int}

Let's start by looking at how integers are stored.
The natural way to do this with ones and zeroes uses base 2,
so 1001 in binary is \\( (1×8)+(0×4)+(0×2)+(1×1) \\) or 9 base 10.
We can handle negative numbers by reserving the top bit for the sign,
so that 01001 is +9 and 11001 is -9.

This representation has two drawbacks.
The minor one is that it gives us two zeroes,
one positive and one negative.
More importantly,
the hardware needed to do arithmetic
on this [%g sign_magnitude "sign and magnitude" %] representation
is more complicated than the hardware needed for another scheme
called [%g twos_complement "two's complement" %].
Instead of mirroring positive values,
two's complement rolls over when going below zero like an odometer.
For example,
with three-bit integers we get the values in [%t binary-3bit %].

<div class="table" id="binary-3bit" caption="3-bit integer values" markdown="1">
| Base 10 | Base 2 |
| ------- | ------ |
| 3       | 011    |
| 2       | 010    |
| 1       | 001    |
| 0       | 000    |
| -1      | 111    |
| -2      | 110    |
| -3      | 101    |
| -4      | 100    |
</div>

We can still tell whether a number is positive or negative
by looking at the first bit:
negative numbers have a 1, positives have a 0.
However,
two's complement is asymmetric:
since 0 counts as a positive number,
numbers go from -4 to 3, or -16 to 15, and so on.
As a result,
even if `x` is a valid number,
`-x` may not be.

We can write binary numbers directly in Python using the `0b` prefix:
for example,
`0b0011` is 3 base 10:

[% inc pat="binary_notation.*" fill="py out" %]

Programmers usually write [%i "hexadecimal" %] instead:
the digits 0–9 have the usual meaning,
and the letters A-F (or a-f) are used to represent the digits 11–15.
We signal that we're using hexadecimal with a `0x` prefix,
so `0xF7` is \\( (15×16)+7 \\) or 247 base 10.
Each hexadecimal digit corresponds to four bits ([%t binary-hex %]),
which makes it easy to translate bits to digits and vice versa:
for example,
`0xF7` is `0b11110111`.
As a bonus,
two hexadecimal digits is exactly one byte.

<div class="table" id="binary-hex" caption="Hexadecimal digits" markdown="1">
| Decimal | Hexadecimal | Bits |
| ------- | ----------- | ---- |
| 0       | 0           | 0000 |
| 1       | 1           | 0001 |
| 2       | 2           | 0010 |
| 3       | 3           | 0011 |
| 4       | 4           | 0100 |
| 5       | 5           | 0101 |
| 6       | 6           | 0110 |
| 7       | 7           | 0111 |
| 8       | 8           | 1000 |
| 9       | 9           | 1001 |
| 10      | A           | 1010 |
| 11      | B           | 1011 |
| 12      | C           | 1100 |
| 13      | D           | 1101 |
| 14      | E           | 1110 |
| 15      | F           | 1111 |
</div>

## Bitwise Operations {: #binary-bitops}

Like most languages based on C,
Python provides [%g bitwise_operation "bitwise operations" %]
for working directly with 1's and 0's in memory:
`&` (and),
`|` (or),
`^` (xor),
`~` (not).
`&` yields a 1 only if both its inputs are 1's,
while `|` yields 1 if either or both are 1.
`^`, called [%g exclusive_or "exclusive or" %] or "xor" (pronounced "ex-or"),
produces 1 if either but *not* both of its arguments are 1;
putting it another way,
`^` produces 0 if its inputs are the same and 1 if they are different.
Finally,
`~` flips its argument: 1 becomes 0, and 0 becomes 1.

When these operators are used on multi-bit values
they work on corresponding bits independently as shown in [%t binary-ops %].

<div class="table" id="binary-ops" caption="Bitwise operations" markdown="1">
| Expression | Bitwise       | Result          |
| ---------- | ------------- | --------------- |
| `12 & 6`   | `1100 & 0110` | `4` (`0100`)    |
| `12 | 6`   | `1100 | 0110` | `14` (`1110`)   |
| `12 ^ 6`   | `1100 ^ 0110` | `10` (`1010`)   |
| `~ 6`      | `~ 0110`      | `9` (`1001`)    |
| `12 << 2`  | `1100 << 2`   | `48` (`110000`) |
| `12 >> 2`  | `1100 >> 2`   | `3` (`0011`)    |
</div>

We can set individual bits to 0 or 1 with these operators.
To set a particular bit to 1,
create a value in which that bit is 1 and the rest are 0.
When this is or'd with a value,
the bit we set is guaranteed to come out 1;
the other bits will be left as they are.
Similarly,
to  set a bit to zero,
create a [%g bit_mask "mask" %] in which that bit is 0 and the others are 1,
then use `&` to combine the two.
To make things easier to read,
programmers often set a single bit,
negate it with `~`,
and then use `&`:

[% inc file="bit_mask.py" %]

Python also has [%g bit_shift "bit shifting" %] operators
that move bits left or right.
Shifting the bits `0110` left by one place produces `1100`,
while shifting it right by one place produces `0011`.
In Python,
this is written `x << 1` or `x >> 1`.
Just as shifting a decimal number left corresponds to multiplying by 10,
shifting a binary number left is the same as multiplying it by 2.
Similarly,
shifting a number right corresponds to dividing by 2 and throwing away the remainder,
so `17 >> 3` is 2.

But what if the top bit of an integer changes from 1 to 0 or vice versa as a result of shifting?
If we're using two's complement,
then the bits `1111` represent the value -1;
if we shift right we get `0111` which is 7.
Similarly,
if we shift `0111` to the left we get `1110` (assuming we fill in the bottom with 0),
which is -2.

Different languages deal with this problem in different ways.
Python always fills with zeroes,
while Java provides two versions of right shift:
`>>` fills in the high end with zeroes
while `>>>` copies in the topmost (sign) bit of the original value.
C (and by extension C++) lets the underlying hardware decide,
which means that if you want to be sure of getting a particular answer
you have to handle the top bit yourself.

## Text {: #binary-text}

The rules for storing text make integers look simple.
By the early 1970s most programs used [%g ascii "ASCII" %],
which represented unaccented Latin characters using the numbers from 32 to 127.
(The numbers 0 to 31 were used for [%g control_code "control codes" %]
such as newline, carriage return, and bell.)
Since computers use 8-bit bytes and the numbers 0–127 only need 7 bits,
programmers were free to use the numbers 128–255 for other characters.
Unfortunately,
different programmers used them to represent different symbols:
non-Latin characters,
graphic characters like boxes,
and so on.
The chaos was eventually tamed by the [%g ansi_encoding "ANSI standard" %]
which (for example) defined the value 231 to mean the character "ç".

A standard that specifies how characters are represented in memory
is called a [%g character_encoding "character encoding" %].
Unfortunately,
the encoding defined by the ANSI standard only solved a small part of a large problem.
It didn't include characters from Turkish, Devanagari, and many other alphabets,
much less the thousands of characters used in some East Asian writing systems.
One solution would have been to use 16 or even 32 bits per character,
but:

1.  existing text files using ANSI would have to be transcribed, and
2.  documents would be two or four times larger.

The solution was a new two-part standard called [%g unicode Unicode %].
The first part defined a [%g code_point "code point" %] for every character:
U+0065 for an upper-case Latin "A",
U+2605 for a black star,
and so on.
(The [Unicode Consortium site][unicode] offers a complete list.)

The second part defined ways to store these values in memory.
The simplest of these is [%g utf_32 "UTF-32" %],
which stores every character as a 32-bit number.
This scheme waste a lot of memory if the text is written in a Western European language,
since it uses four times as much storage as is absolutely necessary,
but it's easy to process.

The most popular encoding is [%g utf_8 "UTF-8" %],
which is [%g variable_length_encoding "variable length" %].
Every code point from 0 to 127 is stored in a single byte whose high bit is 0,
just as it was in the original ASCII standard.
If the top bit in the byte is 1,
on the other hand,
the number of 1's after the high bit but before the first 0
tells UTF-8 how many more bytes that character is using.
For example,
if the first byte of the character is `11101101` then:

-   the first 1 signals that this is a multi-byte character;
-   the next two 1's signal that the character includes bits
    from the following two bytes as well as this one;
-   the 0 separates the byte count from the first few bits used in the character;
    and
-   the final 1101 is the first four bits of the character.

But that's not all:
every byte that's a continuation of a character starts with the bits 10.
(Such bytes are, unsurprisingly, called [%g continuation_byte "continuation bytes" %].)
This rule means that if we look at any byte in a string
we can immediately tell if it's the start of a character
or the continuation of a character.
Thus,
if we want to represent a character whose code point is 1789:

-   We convert to binary 11011111101.
-   We count and realize that we'll need two bytes:
    the first storing the high 5 bits of the character,
    the second storing the low 6 bits.
-   We encode the high 5 bits as 11011011,
    meaning "start of a character with one continuation byte
    and the 5 payload bits 11011".
-   We encode the low 6 bits as 10111101,
    meaning "a continuation byte with 6 payload bits 111101".

## And Now, Persistence {: #binary-binary}

[%x persist %] showed how to store data as human-readable text.
There are generally four reasons to store it in formats that people can't easily read:

Size
:   The string `"10239472"` is 8 bytes long,
    but the 32-bit integer it represents only needs 4 bytes in memory.
    This doesn't matter for small data sets,
    but it does for large ones,
    and it definitely does when data has to move between disk and memory
    or between different computers.

Speed
:   Adding the integers 34 and 56 is a single machine operation.
    Adding the values represented by the strings `"34"` and `"56"` is dozens;
    we'll explore this in the exercises.
    Most programs that read and write text files
    convert the values in those files into binary data
    using something like the `int` or `float` functions,
    but if we're going to process the data many times,
    it makes sense to avoid paying the conversion cost over and over.

Hardware
:   Someone, somewhere, has to convert the signal from the thermocouple to a number,
    and that signal probably arrives as a stream of 1's and 0's.
    
Lack of anything better
:   It's possible to represent images as ASCII art, but sound?
    Or video?
    It would be possible, but it would hardly be sensible.

The first step toward saving and loading binary data
is to write it and read it correctly.
If we open a file for reading using `open("filename", "r")`
then Python assumes we want to read character strings from the file.
It therefore:

-   uses our system's default encoding (which is probably UTF-8)
    to convert bytes to characters, and

-   converts Windows line endings (which are the two characters `"\r\n"`)
    into their Unix equivalents (the single character `"\n"`)
    so that our program only has to deal with the latter.

These translations are handy when we're working with text,
but they mess up binary data:
we probably don't want the pixels in our PNG image translated in these ways.
If we use `open("filename", "rb")` with a lower-case 'b' after the 'r',
on the other hand,
Python gives us back the file's contents as a `bytes` object
instead of as character strings.
In this case we will almost always use `file.read(N)`
to read `N` bytes at a time
rather than using the file in a `for` loop
(which reads up to the next line ending).

What about the values we actually store?
C and Fortran manipulate "naked" values:
programs use what the hardware provides directly.
Python and other dynamic languages,
on the other hand,
put each value in a data structure
that keeps track of its type along with a bit of extra administrative information
([%f binary-boxing %]).
Something stored this way is called a [%g boxed_value "boxed value" %];
this extra data allows the language to do [%i "introspection" %] and much more.

[% figure
   slug="binary-boxing"
   img="boxing.svg"
   alt="Boxed values"
   caption="Using boxed values to store metadata."
%]

The same is true of collections.
For example,
Fortran stores all the values in an array side by side in memory
([%f binary-arrays %]).
Writing this to disk is easy:
if the array starts at location L in memory and has N values,
each of which is B bytes long,
we just copy the bytes from L to L+NB-1 to the file.

[% figure
   slug="binary-arrays"
   img="arrays.svg"
   alt="Storing arrays"
   caption="Low-level and high-level array storage."
%]

A Python list,
on the other hand,
stores references to values rather than the values themselves.
To put the values in a file
we can either write them one at a time
or pack them into a contiguous block and write that.
Similarly,
when reading from a file,
we can either grab the values one by one
or read a larger block and then unpack it in memory.

Packing data is a lot like formatting values for textual output.
The format specifies what types of data are being packed,
how big they are (e.g., is this a 32-bit or 64-bit floating point number?),
and how many values there are,
which in turn exactly determines how much memory is required by the packed representation.

Unpacking reverses this process.
After reading data into memory
we can unpack it according to a format.
The most important thing is that
*we can unpack data any way we want*.
We might pack an integer and then unpack it as four characters,
since both are 32 bits long
([%f binary-packing-unpacking %]).
Or we might save two characters,
an integer,
and two more characters,
then unpack it as a 64-bit floating point number.
The bits are just bits:
it's our responsibility to make sure we keep track of their meaning
when they're down there on disk.

[% figure
   slug="binary-packing-unpacking"
   img="packing_unpacking.svg"
   alt="Packing and unpacking values"
   caption="Packing and unpacking binary values."
%]

Python's [struct][py_struct] module packs and unpacks data for us.
The function `pack(format, val_1, val_2, …)`
takes a format string and a bunch of values as arguments
and packs them into a `bytes` object.
The inverse function,
`unpack(format, string)`,
takes some bytes and a format
and returns a [%i "tuple" %] containing the unpacked values.
Here's an example:

[% inc pat="pack_unpack.*" fill="py out" %]

What is `\x1f` and why is it in our data?
If Python finds a character in a string that doesn't have a printable representation,
it prints a 2-digit [%g escape_sequence "escape sequence" %] in [%i "hexadecimal" %].
Python is therefore telling us that
our string contains the eight bytes
`['\x1f', '\x00', '\x00', '\x00', 'A', '\x00', '\x00', '\x00']`.
`1F` in hex is \\( (1×16^1)+(15×16^0) \\), or 31;
`'A'` is our 65,
because the ASCII code for an upper-case letter A is the decimal value 65.
All the other bytes are zeroes (`"\x00"`)
because each of our integers is 32 bits long
and the significant digits only fill one byte's worth of each.

<div class="table" id="binary-formats" caption="`struct` package formats" markdown="1">
| Format | Meaning                                     |
|------- | ------------------------------------------- |
| `"c"`  | Single character (i.e., string of length 1) |
| `"B"`  | Unsigned 8-bit integer                      |
| `"h"`  | Short (16-bit) integer                      |
| `"i"`  | 32-bit integer                              |
| `"f"`  | 32-bit float                                |
| `"d"`  | Double-precision (64-bit) float             |
</div>

The `struct` module offers a lot of different formats,
some of which are shown in [%t binary-formats %].
The `"B"`, `"h"`, and `"2"` formats deserve some explanation.
`"B"` takes the least significant 8 bits out of an integer and packs those;
`"h"` takes the least significant 16 bits and does likewise.
They're needed because binary data formats often store only as much data as they need to,
so we need a way to get 8- and 16-bit values out of files.
(Many audio formats,
for example,
only store 16 bits per sample.)

Any format can be preceded by a count,
so the format `"3i"` means "three integers":

[% inc pat="pack_count.*" fill="py out" %]

We get the wrong answer in the last call
because we only told Python to pack five characters.
How can we tell it to pack all the data that's there regardless of length?

The short answer is that we can't:
we must specify how much we want packed.
But that doesn't mean we can't handle variable-length strings;
it just means that we have to construct the format on the fly
using an expression like this:

```python
format = f"{len(str)}s"
```

If `str` contains the string `"example"`,
the expression above will assign `"7s"` to `format`,
which just happens to be exactly the right format to use to pack it.
{: .continue}

That's fine when we're writing,
but how do we know how much data to get if we're reading?
For example, suppose we have the two strings "hello" and "Python".
We can pack them like this:

```python
pack('5s6s', 'hello', 'Python')
```

but how do I know how to unpack 5 characters then 6?
The trick is to save the size along with the data.
If we always use exactly the same number of bytes to store the size,
we can read it back safely,
then use it to figure out how big our string is:
{: .continue}

[% inc file="variable_packing.py" keep="pack" %]

[% inc file="variable_packing.py" keep="main" %]
[% inc file="variable_packing.out" %]

The unpacking function is analogous.
We break the [%g buffer_memory "memory buffer" %]
into a [%i "header" %] that's exactly four bytes long
(i.e., the right size for an integer)
and a body made up of whatever's left.
We then unpack the header,
whose format we know,
to determine how many characters are in the string.
Once we've got that we use the trick shown earlier
to construct the right format on the fly
and then unpack the string and return it.

[% inc file="variable_unpacking.py" keep="main" %]
[% inc file="variable_unpacking.out" %]

This is called [%g little_endian "little-endian" %] and is used by all Intel processors.
Some other processors put the most significant byte first,
which is called [%g big_endian "big-endian" %].
There are pro's and con's to both, which we won't go into here.
What you *do* need to know is that if you move data from one architecture to another,
it's your responsibility to flip the bytes around,
because the machine doesn't know what the bytes mean.
This is such a pain that the `struct` module and other libraries like it 
will do things for you if you ask it to.
If you're using `struct`,
the first character of a format string optionally indicates the byte order
([%t binary-endian %]).

<div class="table" id="binary-endian" caption="`struct` package endian indicators" markdown="1">
| Character | Byte order | Size     | Alignment     |
| --------- | ---------- | -------- | ------------- |
| `@`       | native     | native   | native        |
| `=`       | native     | standard | none          |
| `<`       | little     | endian   | standard none |
| `>`       | big        | endian   | standard none |
| `!`       | network    | standard | none          |
</div>

You should also use the `struct` module's `calcsize` function,
which tells you how large (in bytes) the data produced or consumed by a format will be:

[% inc pat="calcsize.*" fill="py out" %]

Binary data is to programming what chemistry is to biology:
you don't want to spend any more time thinking at its level than you have to,
but there's no substitute when you *do* have to.
Please remember that libraries already exist to handle
almost every binary format ever created
and to read data from almost every instrument on the market.
You shouldn't worry about 1's and 0's unless you really have to.

## Summary {: #binary-summary}

*Please see [%x bonus %] for extra material related to these ideas.*

[% figure
   slug="binary-concept-map"
   img="concept_map.svg"
   alt="Concept map for binary data"
   caption="Concepts for binary data."
%]

## Exercises {: #binary-exercises}

### Adding Strings {: .exercise}

Write a function that takes two strings of digits
and adds them as if they were numbers
*without* actually converting them to numbers.
For example,
`add_str("12", "5")` should produce the string `"17"`.

### File Types {: .exercise}

The first eight bytes of a PNG image file always contain the following (base-10) values:

```
137 80 78 71 13 10 26 10
```

Write a program that determines whether a file is a PNG image or not.

### Converting Integers to Bits {: .exercise}

Using Python's bitwise operators,
write a function that returns the binary representation of a non-negative integer.
Write another function that converts a string of 1's and 0's into an integer
(treating it as unsigned).

### Encoding and Decoding {: .exercise}

1.  Write a function that takes a list of integers representing Unicode code points as input
    and returns a list of single-byte integers with their UTF-8 encoding.

2.  Write the complementary function that turns a list of single-byte integers
    into the corresponding code points
    and reports an error if anything is incorrectly formatted.

### Storing Arrays {: .exercise}

Python's [array][py_array] module manages a block of basic values
(characters, integers, or floating-point numbers).
Write a function that takes a list as input,
checks that all values in the list are of the same basic type,
and if so,
packs them into an array and then uses the `struct` module to pack that.

### Performance {: .exercise}

Getting a single value out of an array created with the [array][py_array] module takes time,
since the value must be boxed before it can be used.
Write some tests to see how much slower working with values in arrays is
compared to working with values in lists.
