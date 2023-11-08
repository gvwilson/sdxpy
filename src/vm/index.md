---
abstract: >
    The standard version of Python is implemented in C,
    but C is compiled to instructions for a particular processor.
    To show how that lower layer works,
    this chapter builds a simulator of a small computer
    and an assembler for a very simple language that can be used to program it.
syllabus:
-   Every computer has a processor with a particular instruction set, some registers, and memory.
-   Instructions are just numbers, but may be represented as assembly code.
-   Instructions may refer to registers, memory, both, or neither.
-   A processor usually executes instructions in order, but may jump to another location based on whether a conditional is true or false.
depends:
-   interp
-   binary
---

The interpreter in [%x interp %] relied on Python to do
most of the actual work.
The standard version of Python is implemented in C,
and relies on C's operators to add numbers, index arrays, and so on,
but C is compiled to instructions for a particular processor.
Each operation in the little language of [%x interp %]
is therefore expanded by several layers of software
to become something that hardware can actually run.
To show how that lower layer works,
this chapter builds a simulator of a small computer.
If you want to dive deeper into programming at this level,
have a look at the game [%i "Human Resource Machine" url="human_resource_machine" %].

## Architecture {: #vm-arch}

Our [%g virtual_machine "virtual machine" %]
simulates a computer with three parts ([%f vm-architecture %]):

1.  The [%g instruction_pointer "instruction pointer" %] (IP)
    holds the memory address of the next instruction to execute.
    It is automatically initialized to point at address 0,
    so that is where every program must start.
    This requirement is part of our VM's
    [%g abi "Application Binary Interface" %] (ABI).

1.  Four [%g register_hardware "registers" %] named R0 to R3
    that instructions can access directly.
    There are no memory-to-memory operations in our VM:
    everything happens in or through registers.

1.  256 [%g word_memory "words" %] of memory, each of which can store a single value.
    Both the program and its data live in this single [%i "block (of memory)" "block" %] of memory;
    we chose the size 256 so that the address of each word will fit in a single byte.

[% figure
   slug="vm-architecture"
   img="architecture.svg"
   alt="Virtual machine architecture"
   caption="Architecture of the virtual machine."
%]

Our processor's [%g instruction_set "instruction set" %]
defines what it can do.
Instructions are just numbers,
but we will write them in a simple text format called
[%g assembly_code "assembly code" %]
that gives those number human-readable names.

<div class="pagebreak"></div>

The instructions for our VM are 3 bytes long.
The [%g op_code "op code" %] fits in one byte,
and each instruction may include zero, one, or two single-byte operands.
(Instructions are sometimes called [%g bytecode "bytecode" %],
since they're packed into bytes,
but so is everything else in a computer.)

Each operand is a register identifier,
a constant,
or an address,
which is just a constant that identifies a location in memory.
Since constants have to fit in one byte,
this means that the largest number we can represent directly is 256.
[% t vm-op-codes %] uses the letters `r` and `v`
to indicate instruction format,
where `r` indicates a register identifier.
and `v` indicates a constant value.

<div class="table" id="vm-op-codes" caption="Virtual machine op codes." markdown="1">
| Name  | Code | Format | Action              | Example     | Equivalent           |
| :---- | ---: | :----- | :------------------ | :---------- | :------------------- |
| `hlt` |    1 | `--`   | Halt program        | `hlt`       | `sys.exit(0)`        |
| `ldc` |    2 | `rv`   | Load constant       | `ldc R0 99` | `R0 = 99`            |
| `ldr` |    3 | `rr`   | Load register       | `ldr R0 R1` | `R0 = memory[R1]`    |
| `cpy` |    4 | `rr`   | Copy register       | `cpy R0 R1` | `R0 = R1`            |
| `str` |    5 | `rr`   | Store register      | `str R0 R1` | `memory[R1] = R0`    |
| `add` |    6 | `rr`   | Add                 | `add R0 R1` | `R0 = R0 + R1`       |
| `sub` |    7 | `rr`   | Subtract            | `sub R0 R1` | `R0 = R0 - R1`       |
| `beq` |    8 | `rv`   | Branch if equal     | `beq R0 99` | `if (R0==0) PC = 99` |
| `bne` |    9 | `rv`   | Branch if not equal | `bne R0 99` | `if (R0!=0) PC = 99` |
| `prr` |   10 | `r-`   | Print register      | `prr R0`    | `print(R0)`          |
| `prm` |   11 | `r-`   | Print memory        | `prm R0`    | `print(memory[R0])`  |
</div>

To start building our virtual machine,
we put the VM's details in a file
that can be loaded by other modules:

[% inc file="architecture.py" %]

There isn't a name for this [%i "design pattern" %],
but putting all the constants that define a system in one file
instead of scattering them across multiple files
makes them easier to find as well as ensuring consistency.
{: .continue}

## Execution {: #vm-execute}

We start by defining a class with an instruction pointer, some registers, and some memory
along with a prompt for output:

[% inc file="vm.py" keep="init" %]

A program is just an array of numbers representing instructions.
To load a program into our VM,
we copy those numbers into memory and reset the instruction pointer and registers:

[% inc file="vm.py" keep="init" %]

Notice that the VM's constructor calls `initialize` with an empty array
(i.e., a program with no instructions)
to do initial setup.
If an object has a method to reset or reinitialize itself,
having its constructor use that method
is a way to avoid duplicating code.
{: .continue}

<div class="pagebreak"></div>

To execute the next instruction,
the VM gets the value in memory that the instruction pointer currently refers to
and moves the instruction pointer on by one address.
It then uses [%i "bitwise operation" "bitwise operations" %]
([%x binary %])
to extract the op code and operands from the instruction
([%f vm-unpacking %]).

[% inc file="vm.py" keep="fetch" %]

[% figure
   slug="vm-unpacking"
   img="unpacking.svg"
   alt="Unpacking instructions"
   caption="Using bitwise operations to unpack instructions."
%]

We always unpack two operands regardless of whether the instructions has them or not,
since this is what most hardware implementations would do.
{: .continue}

<div class="callout" markdown="1">

### Processor Design

Some processor do have variable-length instructions,
but they make the hardware more complicated and therefore slower.
To decide whether these costs are worth paying,
engineers rely on simulation and profiling ([%x perf %]).
Backward compatibility is also an issue:
if earlier processors supported variable-length instructions,
later ones must somehow do so as well in order to run old programs.

</div>

The next step is to add a `run` method to our VM
that fetches instructions and executes them until told to stop:

[% inc file="vm.py" keep="run" omit="skip" %]

Let's look more closely at three of these instructions.
The first, `str`, stores the value of one register in the address held by another register:

[% inc file="vm.py" keep="store" %]

Adding the value in one register to the value in another register is simpler:

[% inc file="vm.py" keep="add" %]

as is jumping to a fixed address if the value in a register is zero.
This [%g conditional_jump "conditional jump" %] instruction is how we implement `if`:
{: .continue}

[% inc file="vm.py" keep="beq" %]

## Assembly Code {: #vm-assembly}

We could write out numerical op codes by hand just as [early programmers][eniac_programmers] did.
However,
it is much easier to use an [%g assembler "assembler" %],
which is just a small [%i "compiler" %] for a language
that very closely represents actual machine instructions.

Each command in our assembly languages matches an instruction in the VM.
Here's an assembly language program to print the value stored in R1 and then halt:

[% inc file="print_r1.as" %]

Its numeric representation (in [%i "hexadecimal" %]) is:
{: .continue}

[% inc file="print_r1.mx" %]

One thing the assembly language has that the instruction set doesn't
is [%g label_address "labels" %] on addresses in memory.
The label `loop` doesn't take up any space;
instead,
it tells the assembler to give the address of the next instruction a name
so that we can refer to `@loop` in jump instructions.
For example,
this program prints the numbers from 0 to 2
([%f vm-count-up %]):

<table class="twocol">
  <tbody>
    <tr>
      <td markdown="1">[% inc file="count_up.as" %]</td>
      <td markdown="1">[% inc file="count_up.mx" %]</td>
    </tr>
  </tbody>
</table>

<div class="pagebreak"></div>

[% figure
   slug="vm-count-up"
   img="count_up.svg"
   alt="Counting from 0 to 2"
   caption="Flowchart of assembly language program to count up from 0 to 2."
   cls="here"
%]

Let's trace this program's execution
([%f vm-count-trace %]):

1.  R0 holds the current loop index.
1.  R1 holds the loop's upper bound (in this case 3).
1.  The loop prints the value of R0 (one instruction).
1.  The program adds 1 to R0.
    This takes two instructions because we can only add register-to-register.
1.  It checks to see if we should loop again,
    which takes three instructions.
1.  If the program *doesn't* jump back, it halts.

[% figure
   slug="vm-count-trace"
   img="count_trace.svg"
   alt="Trace counting program"
   caption="Tracing registers and memory values for a simple counting program."
%]

The implementation of the assembler mirrors the simplicity of assembly language.
The main method gets interesting lines,
finds the addresses of labels,
and turns each remaining line into an instruction:

[% inc file="assembler.py" keep="class" %]

To find labels,
we go through the lines one by one
and either save the label *or* increment the current address
(because labels don't take up space):

[% inc file="assembler.py" keep="labels" %]

To compile a single instruction we break the line into pieces,
look up the format for the operands,
and pack the values:

[% inc file="assembler.py" keep="compile" %]

To convert a value,
we either look up the label's address (if the value starts with `@`)
or convert the value to a number:

[% inc file="assembler.py" keep="value" %]

Combining op codes and operands into a single value
is the reverse of the unpacking done by the virtual machine:
{: .continue}

[% inc file="assembler.py" keep="combine" %]

As a test,
this program counts up to three:

[% inc pat="count_up.*" fill="as out" %]

## Arrays {: #vm-arrays}

It's tedious to write programs when each value needs a unique name.
We can do a lot more once we have [%i "array (implementation of)" "arrays" %],
so let's add those to our assembler.
We don't have to make any changes to the virtual machine,
which doesn't care if we think of a bunch of numbers as individuals or elements of an array,
but we do need a way to create arrays and refer to them.

We will allocate storage for arrays at the end of the program
by using `.data` on a line of its own to mark the start of the data section
and then `label: number` to give a region a name and allocate some storage space
([%f vm-array %]).

[% figure
   slug="vm-array"
   img="array.svg"
   alt="Array storage allocation"
   caption="Allocating storage for arrays in the virtual machine."
%]

This enhancement only requires a few changes to the assembler.
First,
we need to split the lines into instructions and data allocations:

[% inc file="arrays.py" keep="assemble" %]

Second,
we need to figure out where each allocation lies and create a label accordingly:

[% inc file="arrays.py" keep="allocate" %]

And that's it:
no other changes are needed to either compilation or execution.
To test it,
let's fill an array with the numbers from 0 to 3:

[% inc pat="fill_array.*" fill="as out"%]

<div class="pagebreak"></div>

## Summary {: #vm-summary}

[% figure
   slug="vm-concept-map"
   img="concept_map.svg"
   alt="Concept map for virtual machine and assembler"
   caption="Concept map for virtual machine and assembler."
   cls="here"
%]

## Exercises {: #vm-exercises}

### Swapping Values {: .exercise}

Write an assembly language program that swaps the values in R1 and R2
without affecting the values in other registers.

### Reversing an Array {: .exercise}

Write an assembly language program that starts with:

-   the base address of an array in one word
-   the length of the array N in the next word
-   N values immediately thereafter

and reverses the array in place.
{: .continue}

### Increment and Decrement {: .exercise}

1.  Add instructions `inc` and `dec` that add one to the value of a register
    and subtract one from the value of a register respectively.

2.  Rewrite the examples to use these instructions.
    How much shorter do they make the programs?
    How much easier to read?

### Using Long Addresses {: .exercise}

1.  Modify the virtual machine so that the `ldr` and `str` instructions
    contain 16-bit addresses rather than 8-bit addresses
    and increase the virtual machine's memory to 64K words to match.

2.  How does this complicate instruction interpretation?

### Operating on Strings {: .exercise}

The C programming language stored character strings as non-zero bytes terminated by a byte containing zero.

1.  Write a program that starts with the base address of a string in R1
    and finishes with the length of the string (not including the terminator) in the same register.

2.  Write a program that starts with the base address of a string in R1
    and the base address of some other block of memory in R2
    and copies the string to that new location (including the terminator).

3.  What happens in each case if the terminator is missing?

### Call and Return {: .exercise}

1.  Add another register to the virtual machine called SP (for "stack pointer")
    that is automatically initialized to the *last* address in memory.

2.  Add an instruction `psh` (short for "push") that copies a value from a register
    to the address stored in SP and then subtracts one from SP.

3.  Add an instruction `pop` (short for "pop") that adds one to SP
    and then copies a value from that address into a register.

4.  Using these instructions,
    write a subroutine that evaluates `2x+1` for every value in an array.

### Disassembling Instructions {: .exercise}

A [%g disassembler "disassembler" %] turns machine instructions into assembly code.
Write a disassembler for the instruction set used by our virtual machine.
(Since the labels for addresses are not stored in machine instructions,
disassemblers typically generate labels like `@L001` and `@L002`.)

### Linking Multiple Files {: .exercise}

1.  Modify the assembler to handle `.include filename` directives.

2.  What does your modified assembler do about duplicate label names?
    How does it prevent infinite includes
    (i.e., `A.as` includes `B.as` which includes `A.as` again)?

### Providing System Calls {: .exercise}

Modify the virtual machine so that developers can add "system calls" to it.

1.  On startup,
    the virtual machine loads an array of functions defined in a file called `syscalls.py`.

2.  The `sys` instruction takes a one-byte constant argument.
    It looks up the corresponding function and calls it with the values of R0-R3 as arguments
    and places the result in R0.

### Unit Testing {: .exercise}

1.  Write unit tests for the assembler.

2.  Once they are working,
    write unit tests for the virtual machine.
