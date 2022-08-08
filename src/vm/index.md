---
title: "A Virtual Machine and Assembler"
syllabus:
- FIXME
---

You might feel there's still magic in our interpreter,
so let's build something lower-level.
Our virtual machine simulates a computer with three parts:

1.  An instruction pointer (IP)
    that holds the memory address of the next instruction to execute.
    It is automatically initialized to point at address 0,
    which is where every program must start.

1.  Four registers named R0 to R3 that instructions can access directly.
    There are no memory-to-memory operations in our VM:
    everything  happens in or through registers.

1.  256 words of memory, each of which can store a single value.
    Both the program and its data live in this single block of memory;
    we chose the size 256 so that each address will fit in a single byte.

The instructions for our VM are 3 bytes long.
The op code fits into one byte,
and each instruction may optionally include one or two single-byte operands.
Each operand is a register identifier,
a constant,
or an address
(which is just a constant that identifies a location in memory);
since constants have to fit in one byte,
the largest number we can represent directly is 256.
The table below uses the letters `r`, `c`, and `a`
to indicate instruction format:
`r` indicates a register identifier,
`c` indicates a constant,
and `a` indicates an address.

| Instruction | Code | Format | Action              | Example      | Equivalent              |
| ----------- | ---- | ------ | ------------------- | ------------ | ----------------------- |
|  `hlt`      |    1 | `--`   | Halt program        | `hlt`        | `sys.exit(0)`           |
|  `ldc`      |    2 | `rc`   | Load constant       | `ldc R0 123` | `R0 = 123`              |
|  `ldr`      |    3 | `rr`   | Load register       | `ldr R0 R1`  | `R0 = RAM[R1]`          |
|  `cpy`      |    4 | `rr`   | Copy register       | `cpy R0 R1`  | `R0 = R1`               |
|  `str`      |    5 | `rr`   | Store register      | `str R0 R1`  | `RAM[R1] = R0`          |
|  `add`      |    6 | `rr`   | Add                 | `add R0 R1`  | `R0 = R0 + R1`          |
|  `sub`      |    7 | `rr`   | Subtract            | `sub R0 R1`  | `R0 = R0 - R1`          |
|  `beq`      |    8 | `ra`   | Branch if equal     | `beq R0 123` | `if (R0 == 0) PC = 123` |
|  `bne`      |    9 | `ra`   | Branch if not equal | `bne R0 123` | `if (R0 != 0) PC = 123` |
|  `prr`      |   10 | `r-`   | Print register      | `prr R0`     | `print(R0)`             |
|  `prm`      |   11 | `r-`   | Print memory        | `prm R0`     | `print(RAM[R0])`        |

We put our VM's architectural details in `architecture.py`.
The VM itself is in `vm.py`:

-   The construct initializes the IP, the registers, and RAM.

-   `initialize` copies a program into RAM.
    A program is just a list of numbers;
    we'll see where they come from in a moment.

-   `fetch` gets the instruction that the IP refers to and moves the IP on to the next address.
    It then uses bitwise operations
    to extract the *op code* and operands from the instruction.

-   `run` is just a big switch statement
    that does whatever the newly-fetched instruction tells it to do,
    such copy a value from memory into a register
    or add the contents of two registers.
    The most interesting instructions are probably the branch instructions,
    which assign a new value to the IP
    so that execution continues at a different location in the program.

We could figure out numerical op codes by hand,
and in fact that's what the first programmers did.
However,
it's much easier to use an *assembler*,
which is just a small compiler for a language that very closely represents actual machine instructions.
Each command in our assembly languages matches an instruction in the VM.
Here's an assembly language program to print the value stored in R1 and then halt:

```{: title="print-r1.as"}
# Print initial contents of R1.
prr R1
hlt
```

In hexadecimal, its numeric representation is:

```{: title="print-r1.mx"}
00010a
000001
```

One thing the assembly language has that the instruction set doesn't
is labels on addresses.
The label `loop` doesn't take up any space;
instead,
it tells the assembler to give the address of the next instruction a name
so that we can refer to that address as `@loop` in jump instructions.
For example,
this program prints the numbers from 0 to 2

```{: title="count-up.as"}
# Count up to 3.
# - R0: loop index.
# - R1: loop limit.
ldc R0 0
ldc R1 3
loop:
prr R0
ldc R2 1
add R0 R2
cpy R2 R1
sub R2 R0
bne R2 @loop
hlt
```

Let's trace this program's execution:

1.  R0 holds the current loop index.
1.  R1 holds the loop's upper bound (in this case 3).
1.  The loop prints the value of R0 (one instruction).
1.  The program adds 1 to R0.
    This takes two instructions because we can only add register-to-register.
1.  It checks to see if we should loop again,
    which takes three instructions.
1.  If the program *doesn't* jump back, it halts.

The implementation of the assembler mirrors the simplicity of assembly language.
The main method gets interesting lines,
finds the addresses of labels,
and turns each remaining line into an instruction:
To find labels,
we go through the lines one by one
and either save the label *or* increment the current address
(because labels don't take up space).

To compile a single instruction we break the line into tokens,
look up the format for the operands,
and pack them into a single value;
combining op codes and operands into a single value
is the reverse of the unpacking done by the virtual machine.

It's tedious to write interesting programs when each value needs a unique name,
so we can add arrays to our assembler.
We allocate storage for arrays at the end of the program
by using `.data` on a line of its own to mark the start of the data section
and then `label: number` to give a region a name and allocate some storage space.

## Exercises {: #compiler-exercises}

### Swapping Values {: .exercise}

Write an assembly language program that swaps the values in R1 and R2
without affecting the values in other registers.

### Reversing an Array {: .exercise}

Write an assembly language program that starts with
the base address of an array in one word,
the length of the array N in the next word,
and N values immediately thereafter,
and reverses the array in place.

### String Length {: .exercise}

C stores character strings as non-zero bytes terminated by a byte containing zero.
Write a program that starts with the base address of a string in R1
and finishes with the length of the string (not including the terminator) in the same register.
