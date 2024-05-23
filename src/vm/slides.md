---
template: slides
title: "A Virtual Machine"
---

## The Problem

-   Still a lot of magic in the interpreter of [%x interp %]

-   Build something that mimics hardware more closely

-   See [%b Nisan2021 %] for a fuller description

-   Or play [Human Resource Machine][human_resource_machine]

---

## Architecture

-  Our [%g virtual_machine "virtual machine" %] (VM)

[% figure
   slug="vm-architecture"
   img="architecture.svg"
   alt="Virtual machine architecture"
   caption="Architecture of the virtual machine."
%]

---

## Architecture

1.  [%g instruction_pointer "Instruction pointer" %] (IP)
    holds the address of the next instruction

    -   Automatically initialized to 0,
        so every program must start there

1.  Instructions can access [%g register_hardware "registers" %] R0 to R3 directly

    -   No memory-to-memory operations

1.  256 [%g word_memory "words" %] of memory

    -   Addresses fit in a single byte

---

## What It Can Do

-   [%g instruction_set "Instruction set" %] defines what the processor can do

-   Each instruction is 3 bytes

-   [%g op_code "op code" %] fits in one byte

-   May have zero, one, or two single-byte operands

    -   Could use variable-length instructions,
        but that would complicate the VM

-   Each operand is a register identifier, a constant, or an address

---

## Writing Instructions

-   Instructions are numbers,

-   Write them in [%g assembly_code "assembly code" %] for readability

<div class="small">
<table>
<tr><th>Name</th><th>Code</th><th>Format</th><th>Action</th><th>Example</th></tr>
<tr><td><code>hlt</code></td><td> 1</td><td><code>--</code></td><td>Halt program       </td><td><code>hlt</code>    </td></tr>
<tr><td><code>ldc</code></td><td> 2</td><td><code>rv</code></td><td>Load constant      </td><td><code>ldc R0 123</code></td></tr>
<tr><td><code>ldr</code></td><td> 3</td><td><code>rr</code></td><td>Load register      </td><td><code>ldr R0 R1</code></td></tr>
<tr><td><code>add</code></td><td> 6</td><td><code>rr</code></td><td>Add                </td><td><code>add R0 R1</code></td></tr>
<tr><td><code>bne</code></td><td> 9</td><td><code>rv</code></td><td>Branch if not equal</td><td><code>bne R0 123</code></td></tr>
<tr><td><code>prr</code></td><td>10</td><td><code>r-</code></td><td>Print register     </td><td><code>prr R0</code> </td></tr>
</table>
</div>

---

## Details

[%inc architecture.py %]

---

## VM Class

[%inc vm.py mark=init %]

---

## Fetching and Unpacking

[%inc vm.py mark=fetch %]

-  Use [%g bitwise_operation "bitwise operations" %] to get bytes out of integer

[% figure
   slug="vm-unpacking"
   img="unpacking.svg"
   alt="Unpacking instructions"
   caption="Using bitwise operations to unpack instructions."
%]

---

## Running a Program

[%inc vm.py mark=run omit=skip %]

---

## Sample Instructions

-   Store a value

[%inc vm.py mark=store %]

-   Addition

[%inc vm.py mark=add %]

-   [%g conditional_jump "Conditional jump" %]

[%inc vm.py mark=beq %]

---

## Writing Programs

-   Hexadecimal

[%inc print_r1.mx %]

-   Assembly code

[%inc print_r1.as %]

-   Write an [%g assembler "assembler" %] to the latter into the former

---

## Labels

-   Instruction set doesn't have names for addresses

-   But we want [%g label_address "labels" %] for readability

[%inc count_up.as %]

---

## Counting Up

[%inc count_up.out %]

---

## Counting Up

[% figure
   slug="vm-count-up"
   img="count_up.svg"
   alt="Counting from 0 to 2"
   caption="Flowchart of assembly language program to count up from 0 to 2."
%]

---

## Counting Up

[% figure
   slug="vm-count-trace"
   img="count_trace.svg"
   alt="Trace counting program"
   caption="Tracing registers and memory values for a simple counting program."
%]

---

## Assembler Class

[%inc assembler.py mark=class %]

---

## Resolving Labels

[%inc assembler.py mark=labels %]

-   Either save label *or* increment current address

---

## Compiling an Instruction

[%inc assembler.py mark=compile %]

---

## Converting a Value

-   Look up label's address if value starts with `@`

-   Convert value to number if it doesn't

[%inc assembler.py mark=value %]

---

<!--# class="summary" -->

## Summary

[% figure
   slug="vm-concept-map"
   img="concept_map.svg"
   alt="Concept map for virtual machine and assembler"
   caption="Concept map for virtual machine and assembler."
%]
