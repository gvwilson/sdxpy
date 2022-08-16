---
title: "A Virtual Machine and Assembler"
syllabus:
- FIXME
---

You might feel there's still magic in our interpreter,
so let's build something lower-level.
If you want to dive deeper,
have a look at [%i "Nystrom, Bob" %][Bob Nystrom's][nystrom_bob][%/i%]
*[Crafting Interpreters][crafting_interpreters]* [%b Nystrom2021 %].
You may also enjoy the game [%i "Human Resource Machine" %][Human Resource Machine][human_resource_machine][%/i%],
which asks you to solve puzzles of increasing difficulty
using a processor almost as simple as ours.

## Architecture {: #vm-arch}

Every processor has its own [%i "instruction set" %][%g instruction_set "instruction set" %][%/i%],
and a compiler translates high-level languages into those instructions.
Compilers often use an intermediate representation called
[%i "assembly code" %][%g assembly_code "assembly code" %][%/i%]
that gives instructions human-readable names instead of numbers.
Our [%i "virtual machine" %][%g virtual_machine "virtual machine" %][%/i%] simulates
a computer with three parts
which are shown in [%f vm-architecture %]
for a program made up of 110 instructions:

1.  An [%i "instruction pointer" %][%g instruction_pointer "instruction pointer" %][%/i%] (IP)
    that holds the memory address of the next instruction to execute.
    It is automatically initialized to point at address 0,
    which is where every program must start.
    This rule is part of the [%i "Application Binary Interface" %][%g abi "Application Binary Interface" %][%/i%] (ABI)
    for our virtual machine.

1.  Four [%i "register (in computer)" %][%g register "registers" %][%/i%] named R0 to R3 that instructions can access directly.
    There are no memory-to-memory operations in our VM:
    everything  happens in or through registers.

1.  256 [%g word_memory "words" %] of memory, each of which can store a single value.
    Both the program and its data live in this single block of memory;
    we chose the size 256 so that each address will fit in a single byte.

[% figure
   slug="vm-architecture"
   img="architecture.svg"
   alt="Virtual machine architecture"
   caption="Architecture of the virtual machine."
%]

The instructions for our VM are 3 bytes long.
The [%i "op code" "virtual machine!op code" %][%g op_code "op code" %][%/i%] fits into one byte,
and each instruction may optionally include one or two single-byte operands.
Each operand is a register identifier,
a constant,
or an address
(which is just a constant that identifies a location in memory);
since constants have to fit in one byte,
the largest number we can represent directly is 256.
[% t vm-op-codes %] uses the letters `r`, `c`, and `a`
to indicate instruction format,
where `r` indicates a register identifier,
`c` indicates a constant,
and `a` indicates an address.

<div class="table" id="vm-op-codes" caption="Virtual machine op codes." markdown="1">
| Instruction | Code | Format | Action              | Example      | Equivalent                |
| ----------- | ---- | ------ | ------------------- | ------------ | ------------------------- |
|  `hlt`      |    1 | `--`   | Halt program        | `hlt`        | `process.exit(0)`         |
|  `ldc`      |    2 | `rc`   | Load immediate      | `ldc R0 123` | `R0 := 123`               |
|  `ldr`      |    3 | `rr`   | Load register       | `ldr R0 R1`  | `R0 := RAM[R1]`           |
|  `cpy`      |    4 | `rr`   | Copy register       | `cpy R0 R1`  | `R0 := R1`                |
|  `str`      |    5 | `rr`   | Store register      | `str R0 R1`  | `RAM[R1] := R0`           |
|  `add`      |    6 | `rr`   | Add                 | `add R0 R1`  | `R0 := R0 + R1`           |
|  `sub`      |    7 | `rr`   | Subtract            | `sub R0 R1`  | `R0 := R0 - R1`           |
|  `beq`      |    8 | `ra`   | Branch if equal     | `beq R0 123` | `if (R0 === 0) PC := 123` |
|  `bne`      |    9 | `ra`   | Branch if not equal | `bne R0 123` | `if (R0 !== 0) PC := 123` |
|  `prr`      |   10 | `r-`   | Print register      | `prr R0`     | `console.log(R0)`         |
|  `prm`      |   11 | `r-`   | Print memory        | `prm R0`     | `console.log(RAM[R0])`    |
</div>

We put our VM's architectural details in a file
that can be shared by other components:

[% excerpt f="architecture.py" %]

There isn't a name for this design pattern,
but putting all the constants that define a system in one file
instead of scattering them across multiple files
makes them easier to find as well as ensuring consistency.
{: .continue}

## Execution {: #vm-execute}

As in previous chapters,
we will split a class that would normally be written in one piece into several parts for exposition.
We start by defining a class with an instruction pointer, some registers, and some memory
along with a prompt for output:

[% excerpt f="vm_base.py" omit="skip" %]

A program is just an array of numbers representing instructions.
To load one,
we copy those numbers into memory and reset the instruction pointer and registers:

[% excerpt f="vm_base.py" keep="initialize" %]

In order to handle the next instruction,
the VM gets the value in memory that the instruction pointer currently refers to
and moves the instruction pointer on by one address.
It then uses [%i "bitwise operation" %][%g bitwise_operation "bitwise operations" %][%/i%]
to extract the op code and operands from the instruction
([%f vm-unpacking %]):

[% excerpt f="vm_base.py" keep="fetch" %]

[% figure
   slug="vm-unpacking"
   img="unpacking.svg"
   alt="Unpacking instructions"
   caption="Using bitwise operations to unpack instructions."
%]

<div class="callout" markdown="1">

### Semi-realistic

We always unpack two operands regardless of whether the instructions has them or not,
since this is what a hardware implementation would be.
We have also included assertions in our VM
to simulate the way that real hardware includes logic
to detect illegal instructions and out-of-bound memory addresses.

</div>

The next step is to extend our base class with one that has a `run` method.
As its name suggests,
this runs the program by fetching instructions and executing them until told to stop:

[% excerpt f="vm.py" omit="skip" %]

Some instructions are very similar to others,
so we will only look at three here.
The first stores the value of one register in the address held by another register:

[% excerpt f="vm.py" keep="op_str" %]

The first three lines check that the operation is legal;
the fourth one uses the value in one register as an address,
which is why it has nested array indexing.
{: .continue}

Adding the value in one register to the value in another register is simpler:

[% excerpt f="vm.py" keep="op_add" %]

as is jumping to a fixed address if the value in a register is zero:
{: .continue}

[% excerpt f="vm.py" keep="op_beq" %]

## Assembly Code {: #vm-assembly}

We could figure out numerical op codes by hand,
and in fact that's what [the first programmers][eniac_programmers] did.
However,
it is much easier to use an [%i "assembler" %][%g assembler "assembler" %][%/i%],
which is just a small compiler for a language that very closely represents actual machine instructions.

Each command in our assembly languages matches an instruction in the VM.
Here's an assembly language program to print the value stored in R1 and then halt:

[% excerpt f="print_r1.as" %]

Its numeric representation is:
{: .continue}

[% excerpt f="print_r1.mx" %]

One thing the assembly language has that the instruction set doesn't
is [%i "label (on address)" %][%g label_address "labels on addresses" %][%/i%].
The label `loop` doesn't take up any space;
instead,
it tells the assembler to give the address of the next instruction a name
so that we can refer to that address as `@loop` in jump instructions.
For example,
this program prints the numbers from 0 to 2
([%f vm-count_up %]):

[% excerpt pat="count_up.*" fill="as mx" %]

[% figure
   slug="vm-count_up"
   img="count_up.svg"
   alt="Counting from 0 to 2"
   caption="Flowchart of assembly language program to count up from 0 to 2."
%]

Let's trace this program's execution
([%f vm-trace-counter %]):

1.  R0 holds the current loop index.
1.  R1 holds the loop's upper bound (in this case 3).
1.  The loop prints the value of R0 (one instruction).
1.  The program adds 1 to R0.
    This takes two instructions because we can only add register-to-register.
1.  It checks to see if we should loop again,
    which takes three instructions.
1.  If the program *doesn't* jump back, it halts.

[% figure
   slug="vm-trace-counter"
   img="trace_counter.svg"
   alt="Trace counting program"
   caption="Tracing registers and memory values for a simple counting program."
%]

The implementation of the assembler mirrors the simplicity of assembly language.
The main method gets interesting lines,
finds the addresses of labels,
and turns each remaining line into an instruction:

[% excerpt f="assembler.py" keep="assemble" %]

To find labels,
we go through the lines one by one
and either save the label *or* increment the current address
(because labels don't take up space):

[% excerpt f="assembler.py" keep="find-labels" %]

To compile a single instruction we break the line into tokens,
look up the format for the operands,
and pack them into a single value:

[% excerpt f="assembler.py" keep="compile" %]

Combining op codes and operands into a single value
is the reverse of the unpacking done by the virtual machine:

[% excerpt f="assembler.py" keep="combine" %]

Finally, we need few utility functions:

[% excerpt f="assembler.py" keep="utilities" %]

Let's try assembling a program and display its output,
the registers,
and the interesting contents of memory.
As a test,
this program counts up to three:

[% excerpt pat="count_up.*" fill="as out" %]

## How can we store data? {: #vm-data}

It is tedious to write interesting programs when each value needs a unique name.
We can do a lot more once we have collections like [%i "array!implementation of" %]arrays[%/i%],
so let's add those to our assembler.
We don't have to make any changes to the virtual machine,
which doesn't care if we think of a bunch of numbers as individuals or elements of an array,
but we do need a way to create arrays and refer to them.

We will allocate storage for arrays at the end of the program
by using `.data` on a line of its own to mark the start of the data section
and then `label: number` to give a region a name and allocate some storage space
([%f vm-storage-allocation %]).

[% figure
   slug="vm-storage-allocation"
   img="storage_allocation.svg"
   alt="Storage allocation"
   caption="Allocating storage for arrays in the virtual machine."
%]

This enhancement only requires a few changes to the assembler.
First,
we need to split the lines into instructions and data allocations:

[% excerpt f="allocate_data.py" keep="assemble" %]

[% excerpt f="allocate_data.py" keep="split-allocations" %]

Second,
we need to figure out where each allocation lies and create a label accordingly:

[% excerpt f="allocate_data.py" keep="add-allocations" %]

And that's it:
no other changes are needed to either compilation or execution.
To test it,
let's fill an array with the numbers from 0 to 3:

[% excerpt pat="fill_array.*" fill="as out"%]

<div class="callout" markdown="1">

### How does it actually work?

Our VM is just another program.
If you'd like to know what happens when instructions finally meet hardware,
and how electrical circuits are able to do arithmetic,
make decisions,
and talk to the world,
[% b Patterson2017 %] has everything you want to know and more.

</div>

## Exercises {: #vm-exercises}

### Swapping values {: .exercise}

Write an assembly language program that swaps the values in R1 and R2
without affecting the values in other registers.

### Reversing an array {: .exercise}

Write an assembly language program that starts with:

-   the base address of an array in one word
-   the length of the array N in the next word
-   N values immediately thereafter

and reverses the array in place.
{: .continue}

### Increment and decrement {: .exercise}

1.  Add instructions `inc` and `dec` that add one to the value of a register
    and subtract one from the value of a register respectively.

2.  Rewrite the examples to use these instructions.
    How much shorter do they make the programs?
    How much easier to read?

### Using long addresses {: .exercise}

1.  Modify the virtual machine so that the `ldr` and `str` instructions
    contain 16-bit addresses rather than 8-bit addresses
    and increase the virtual machine's memory to 64K words to match.

2.  How does this complicate instruction interpretation?

### Operating on strings {: .exercise}

The C programming language stored character strings as non-zero bytes terminated by a byte containing zero.

1.  Write a program that starts with the base address of a string in R1
    and finishes with the length of the string (not including the terminator) in the same register.

2.  Write a program that starts with the base address of a string in R1
    and the base address of some other block of memory in R2
    and copies the string to that new location (including the terminator).

3.  What happens in each case if the terminator is missing?

### Call and return {: .exercise}

1.  Add another register to the virtual machine called SP (for "stack pointer")
    that is automatically initialized to the *last* address in memory.

2.  Add an instruction `psh` (short for "push") that copies a value from a register
    to the address stored in SP and then subtracts one from SP.

3.  Add an instruction `pop` (short for "pop") that adds one to SP
    and then copies a value from that address into a register.

4.  Using these instructions,
    write a subroutine that evaluates `2x+1` for every value in an array.

### Disassembling instructions {: .exercise}

A [%g disassembler "disassembler %] turns machine instructions into assembly code.
Write a disassembler for the instruction set used by our virtual machine.
(Since the labels for addresses are not stored in machine instructions,
disassemblers typically generate labels like `@L001` and `@L002`.)

### Linking multiple files {: .exercise}

1.  Modify the assembler to handle `.include filename` directives.

2.  What does your modified assembler do about duplicate label names?
    How does it prevent infinite includes
    (i.e., `A.as` includes `B.as` which includes `A.as` again)?

### Providing system calls {: .exercise}

Modify the virtual machine so that developers can add "system calls" to it.

1.  On startup,
    the virtual machine loads an array of functions defined in a file called `syscalls.py`.

2.  The `sys` instruction takes a one-byte constant argument.
    It looks up the corresponding function and calls it with the values of R0-R3 as parameters
    and places the result in R0.

### Unit testing {: .exercise}

1.  Write unit tests for the assembler.

2.  Once they are working,
    write unit tests for the virtual machine.
