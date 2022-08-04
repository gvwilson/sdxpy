---
title: "Binary Storage"
syllabus:
- FIXME
---

## Integers {: #binary-storage-int}

Let's start by looking at how numbers are stored.
If we only have 0's and 1' the natural way to store a positive integer is to use base 2,
so 1001 in binary is (1×8)+(0×4)+(0×2)+(1×1) or 9 base 10.
It's natural to extend this scheme to negative numbers by reserving one bit for the sign,
so that 01001 is +9 and 11001 is -9.

But there are two problems with this.
The minor one is that it gives us two representations for zero,
and no-one wants to have to write:

```python
if (length != +0) and (length != -0)
```

The major one is that
the hardware needed to do addition and other arithmetic
on this [%g sign_magnitude "sign and magnitude" %] representation
are more complicated than the hardware needed for another representation
called {% g twos_complement "two's complement" %].
Instead of mirroring positive values,
two's complement rolls over when going below zero like an odometer.
For example,
with three-bit integers we get:

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

This scheme solves the "double zero" problem
and the hardware to handle it is faster and cheaper.
We can still tell whether a number is positive or negative
by looking at the first bit:
negative numbers have a 1, positives have a 0.
The only odd thing is its asymmetry:
because 0 counts as a positive number,
numbers go from -4 to 3, or -16 to 15, and so on,
so even if `x` is a valid number,
`-x` may not be.

## Floating Point Numbers {: #binary-storage-fp}

Finding a good representation for floating point numbers is hard.
The root of the problem is that
we cannot represent an infinite number of real values
with a finite set of bit patterns.
And no matter what values we represent,
there will be an infinite number of values between each of them that we can't.

<div class="callout" markdown="1">

### Go to the source

The explanation that follows is simplified to keep it manageable.
If you're doing any calculation on a computer at all,
please read [%b Goldberg1991 %].

</div>

Floating point numbers are represented by a sign,
a magnitude,
and an exponent.
In a 32-bit [%g word_memory "word" %]
the IEEE 754 standard calls for 1 bit of sign,
23 bits for the magnitude (or mantissa),
and 8 bits for the exponent.
We will illustrate how it works using a much smaller representation:
no sign,
3 bits for the magnitude,
and 2 for the exponent.

[% fixme "represent 48" $]

Here are the values we can represent this way:

[% fixme "number line" %]

There are a lot of values this format can't represent.
It can store 8 and 10, for example, but not 9.
This is exactly like the problem hand calculators have
with fractions like 1/3:
in decimal, we have to round that to 0.3333 or 0.3334.

But if this scheme has no representation for 9
then 8+1 must be stored as either 8 or 10.
If that's so,
then what is 8+1+1?
If we add from the left,
(8+1)+1 is 8+1 is 8,
but if we add from the right,
8+(1+1) is 8+2 is 10.
Changing the order of operations makes the difference between right and wrong.

The authors of numerical libraries spend a lot of time worrying about things like this.
In this case
sorting the values and then add from smallest to largest
gives the best chance of getting the best possible answer.
In other situations,
like inverting a matrix, the rules are much more complicated.

Another observation about our uneven number line is that
the we can represent are unevenly spaced.
However,
the relative spacing between each set of values stays the same:
the first group is separated by 1,
then the separation becomes 2,
then 4,
then 8,
so that the ratio of spacing to values stays roughly constant.
This happens because we're multiplying the same fixed set of mantissas
by ever-larger exponents,
and it points us at a couple of useful definitions:

-   The [%g absolute_error "absolute error" %] in an approximation
    is the absolute value of the difference
    between the approximation and the actual value.

-   The [%g relative_error "relative error" %]
    is the ratio of the absolute error
    to the absolute value we're approximating.

For example,
being off by 1 in approximating 8+1 and 56+1 is the same absolute error,
but the relative error is larger in the first case than in the second.
{: .continue}

When we're thinking about floating point numbers,
relative error is almost always more useful than absolute:
it makes little sense to say that we're off by a hundredth
when the value in question is a billionth.
We should take this into account when testing.
The program shown below loops over the integers from 1 to 9
and uses them to create the values 0.9, 0.09, and so on:

FIXME

It then sums those numbers to produce 0.9, 0.99, and so on.

Let's calculate the same values by subtracting .1 from 1,
then subtracting .01,
and so on.
This program does that and computes the difference
between the two representations:

The very first value contributing to our sum is already slightly off
because we cannot exactly represent 0.9 in base 2
any more than we can exactly represent 1/3 in base 10.
Doubling the size of the mantissa would reduce the error,
but we can't ever eliminate it.
The good news is that 9×0.1 and 1-0.1 are exactly the same.
It might not be precisely right, but at least it's consistent.

The same cannot be said for some of the later values:
there are small differences between what we get from our two formulas.
And sometimes the accumulated errors cancel out
and make the result more accurate once again.

One implication of this is that
we should never use `==` or `!=` on floating point numbers
because two numbers calculated in different ways
will probably not have exactly the same bits.
It's OK to use `<`, `>=`, and other orderings.
FIXME: why.

If we want to compare floating point numbers,
use pytest's `approx`,
which checks whether two numbers are within some tolerance of each other.
<https://docs.pytest.org/en/4.6.x/reference.html#pytest-approx>

FIXME: Fraction
<https://www.textualize.io/blog/posts/7-things-about-terminals>

## Text {: #binary-storage-text}

FIXME

## And Now, Persistence {: #binary-storage-binary}

So, why binary?
Why store data in a format that can't be handled by editors like Notepad and nano?
There are generally four reasons:

Size
:   The string `"10239472"` is 8 bytes long,
    but the 32-bit integer it represents only needs 4 bytes in memory.
    This doesn't matter for small data sets,
    but it does for large ones,
    and it definitely does when data has to move between disk and memory
    or between different computers.

Speed
:   Adding the integers 34 and 56 is a single machine operation.
    Adding the values represented by the strings `"34"` and `"56"` is dozens.
    FIXME: exercise
    Most programs that read and write text files
    convert the values in those files into binary data
    using something like the `int` or `float` functions,
    but if we're going to process the data many times,
    it makes sense to avoid paying the conversion cost over and over.

Hardware
:   Someone, somewhere, has to convert the signal from the thermocouple to a number,
    and that signal probably arrives arrives as a stream of 1's and 0's.
    
Lack of anything better
:   It's possible to represent images as ASCII art, but sound?
    Or video?
    It would be possible, but it would hardly be sensible.

Most programs use line-oriented file I/O:
they read characters until they see an end-of-line marker
and then hand back those characters as a string.
We can also use byte-oriented routines,
the most basic of which is simply called `read`.
If `stream` is an open file,
then `stream.read(N)` hands back up to the next N bytes from the file
("up to", because there might not be that much data left).
The result is returned as a string,
but---and this is crucial---there is no guarantee that the values represent characters.
We can concatenate other data onto it,
but if the underlying file is a PNG image,
text-oriented methods like `string.upper`
won't do anything meaningful.

Where there's a `read` there's a `write`.
`stream.write(str)` writes the bytes in the string `str` to a file that has been opened for writing.
In both the reading and writing cases,
though,
it's very important to open the file in [%g binary_mode "binary mode" %] using either:

```python
reader = open('input.dat', 'rb')
```

or:
{: .continue}

```python
writer = open('input.dat', 'wb')
```

The `"b"` at the end of the mode string tells Python
*not* to translate Windows line endings (which are the two characters `"\r\n"`)
into Unix line endings (the single character `"\n"`).
This translation is handy when we're working with text,
since it means our programs only have to deal with one style of line
ending no mater what platform the code is running on,
but it messes up non-textual data.

There's another problem here as well.
C and Fortran store integers as "naked" 32-bit values:
the program uses what the machine provides,
no more and no less.
Python and other dynamic languages usually don't use raw values.
Instead,
they put the value in a larger data structure
that keeps track of its type along with a bit of extra administrative information.
That extra data allows those languages to do garbage collection.
It also allows us to assign values to variables without explicitly declaring their type,
since the value we're assigning carries its type along with it.

A similar issue comes up when we compare Fortran's arrays to Python's lists.
Fortran stores the data in an array side by side in one big block of memory.
Writing this to disk is easy:
if the array starts at location L in memory and has N values,
each of which is B bytes long,
we just copy the bytes from L to L+NB-1 to the file.

A Python list,
on the other hand,
stores pointers to values rather than the values themselves.
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
and how many values there are.
The format exactly determines how much memory is required by the packed representation.
The result of packing values is a block of bytes,
which Python represents as a string,
but as mentioned above,
this isn't a string of characters.

Unpacking reverses this process.
After reading data into memory
we can unpack it according to a format.
The most important thing is that
*we can unpack data any way we want*.
We might pack an integer and then unpack it as four characters,
since both are 32 bits long.
Or we might save two characters,
an integer,
and two more characters,
then unpack it as a 64-bit floating point number.
The bits are just bits:
it's our responsibility to make sure we keep track of their meaning
when they're down there on disk.

In Python we can use the `struct` module to pack and unpack data.
The function `pack(format, val_1, val_2, …)`
takes a format string and a bunch of values as arguments,
packs them into a string,
and gives that back to us.
The inverse function, `unpack(format, string)` takes such a string and a format
and returns a tuple containing the unpacked values. Here's an example:

```python
>>> import struct 
>>> fmt = 'ii' \# two 32-bit integers
>>> x = 31 
>>> y = 65 
>>> binary = struct.pack(fmt, x, y)
>>> print("binary representation:", repr(binary))
binary representation: '\x1f\x00\x00\x00A\x00\x00\x00' 

>>> normal = struct.unpack(fmt, binary) 
>>> print("back to normal:", normal)
back to normal: (31, 65)
```

Er, what?
What is `\x1f` and why is it in our data?
Well,
if Python finds a character in a string that doesn't have a printable representation,
it prints a 2-digit escape sequence in [%g hexadecimal "hexadecimal" %] (base 16).
This uses the letters A-F (or a-f) to represent the digits from 10 to 15,
so that (for example) `3D5` is (3×16^2^)+(13×16^1^)+(5×16^0^), or 981 in decimal.
Python is therefore telling us that
our string contains the eight bytes
`['\x1f', '\x00', '\x00', '\x00', 'A', '\x00', '\x00', '\x00']`.
`1F` in hex is (1×16^1^)+(15×16^0^), or 31;
`'A'` is our 65,
because the ASCII code for an upper-case letter A is the decimal value 65.
All the other bytes are zeroes (`"\x00"`)
because each of our integers is 32 bits long
and the significant digits only fill one byte's worth of each.

The `struct` module offers a lot of different formats:

| Format | Meaning                                     |
|------- | ------------------------------------------- |
| `"c"`  | Single character (i.e., string of length 1) |
| `"B"`  | Unsigned 8-bit integer                      |
| `"h"`  | Short (16-bit) integer                      |
| `"i"`  | 32-bit integer                              |
| `"f"`  | 32-bit float                                |
| `"d"`  | Double-precision (64-bit) float             |

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

```python
>>> pack('3i', 1, 2, 3)
'\x01\x00\x02\x00\x03\x00'

>>> pack('5s', 'hello') hello 
>>> pack('5s', 'a longer string')
a lon
```

We get the wrong answer because we only told Python to pack five characters.
How can we tell it to pack all the data that's there regardless of length?

The short answer is that we can't:
we must specify how much we want packed.
But that doesn't mean we can't handle variable-length strings;
it just means that we have to construct the format on the fly:

```python
format = '%ds' % len(str)
```

`len(str)` is just the length of the string `str`,
and the plain old text format `"%ds"` means
"a decimal integer followed by the letter 's'",
so if `str` contains the string `"example"`,
the expression above will assign the string `"7s"` to `format`,
which just happens to be exactly the right format to use to pack it.

That's fine when we're writing,
buthow do we know how much data to get if we're reading?
For example, suppose I have the two strings "hello" and "Python".
I can pack them like this:

```python
buffer = pack('5s6s', 'hello', 'Python')
```

but how do I know how to unpack 5 characters then 6?
The trick is to save the size along with the data.
If we always use exactly the same number of bytes to store the size,
we can read it back safely,
then use it to figure out how big our string is:
{: .continue}

```python
>>> def pack_string(str):
...     header = pack('i', len(str))
...     body_format = '%ds' % len(str)
...     body = pack(body_format, str)
...     return header + body
...
>>> pack_string('hello')
'\x05\x00\x00\x00hello'
```

The unpacking function is almost the same:

```python
>>> def unpack_string(buffer):
...    header, body = buffer[:4], buffer[4:]
...    unpacked_header = unpack('i', header)
...    length = unpacked_header[0]
...    body_format = '%ds' % length
...    result = unpack(body_format, body)
...    return result
```

First, we break the buffer into two parts:
a header that's exactly four bytes long
(i.e., the right size for an integer)
and a body made up of whatever's left.
We then unpack the header,
whose format we know,
to determine how many characters are in the string.
Once we've got that we use the trick shown earlier
to construct the right format on the fly
and then unpack the string and return it.

<div class="callout" markdown="1">

### Big and Little

Something else to notice here is that
the least significant byte of an integer comes first.
This is called [%g little_endian "little-endian" %] and is used by all Intel processors.
Some other processors put the most significant byte first,
which is called [%g big_endian "big-endian" %].
There are pro's and con's to both, which we won't go into here.
What you *do* need to know is that if you move data from one architecture to another,
it's your responsibility to flip the bytes around,
because the machine doesn't know what the bytes mean.
This is such a pain that the `struct` library and other libraries like
will do things for you if you ask it to.
If you're using `struct`,
the first character of a format string optionally indicates the byte order:

| Character | Byte order | Size     | Alignment     |
| --------- | ---------- | -------- | ------------- |
| `@`       | native     | native   | native        |
| `=`       | native     | standard | none          |
| `<`       | little     | endian   | standard none |
| `>`       | big        | endian   | standard none |
| `!`       | network    | standard | none          |

</div>

You should also use the `struct` library's `calcsize` function,
which tells you how large (in bytes) the data produced or consumed by a format will be.
For example:

```python
>>> calcsize('4s')
4

>>> calcsize('3i4s5d')
56
```

Binary data is to programming what chemistry is to biology:
you don't want to spend any more time thinking at its level than you have to,
but there's no substitute when you *do* have to.
Please remember that libraries already exist to handle almost every binary format ever created
and to read data from almost every instrument on the market.
You shouldn't worry about 1's and 0's unless you really have to.

## Exercises {: #binary-storage-exercises}

FIXME
