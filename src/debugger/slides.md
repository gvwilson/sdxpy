---
template: slides
title: "A Debugger"
---

## The Problem

-   Tracing execution with `print` statements is tedious

-   And impossible (or nearly so) in some situations

-   Single-stepping/breakpoint debugger is far more effective

-   Build one to understand how they work

-   And to show how to test interactive applications

---

## Preparation

-   We will want non-interactive input and output for testing

-   So [%g refactor "refactor" %] the virtual machine of [%x vm %]

-   Pass an output stream (by default `sys.stdout`)

[%inc vm_base.py mark=init %]

-   Replace every `print` with a call to `self.write`

[%inc vm_base.py mark=write %]

---

## Getting Input

-   Similarly, don't use `input` function directly

[%inc vm_step.py mark=init %]

[%inc vm_step.py mark=read %]

---

## Enumerating State

-   Old VM was either running or finished

-   New one has a third state: single-stepping

-   So define an [%g enumeration "enumeration" %]

[%inc architecture.py mark=state %]

-   Safer than using strings (which can be mis-spelled)

---

## Running

-   New `run` method starts in `STEPPING` state

    -   If it started in `RUNNING` we could never tell it to do otherwise

[%inc vm_step.py mark=run %]

---

## Interaction Cases

1.  Empty line: go around again

2.  [%g disassemble "Disassemble" %] current instruction or show memory:
    do that and go around again

3.  Quit:
    change state to `FINISHED`.

4.  Run normally:
    change state to `RUNNING`

5.  Single-step:
    exit loop without changing state

---

## Disassembling

[%inc vm_step.py mark=lookup %]

-   If we type in the number-to-instruction lookup table,
    it will eventually fall out of step

-   So build it from architecture description

[% figure
   slug="debugger-table"
   img="table.svg"
   alt="Building a consistent lookup table"
   caption="Building a consistent lookup table."
%]

---

## Capturing Output

-   Has to be an object with a `write` method

-   But can save what it's given for later inspection

[%inc test_vm.py mark=writer %]

---

## Providing Input

-   Need a "function" that takes a prompt and returns a string

-   Create a class with a `__call__` method that "reads" from a list

[%inc test_vm.py mark=reader %]

---

## Testing Disassembly

[%inc test_vm.py mark=disassemble %]

1.  Create program (just a `hlt` instruction)
2.  Create a `Reader` with the commands `"d"` and `"q"`
3.  Create a `Writer` to capture output
4.  Run the program
5.  Check that the output is correct

---

## Is It Worth It?

-   Yes

-   Test that the debugger can single-step three times and then quit

[%inc test_vm.py mark=print %]

---

<!--# class="aside" -->

## Other Tools

-   [Expect][expect] often used to script command-line applications

    -   Can be used through the [pexpect][pexpect] module

-   [Selenium][selenium] and [Cypress][cypress] for browser-based applications

    -   Simulate mouse clicks, window resizing, etc.

-   Harder to set up and use than a simple `assert`

-   But so are the things they're testing

---

## Extensibility

-   Move every interactive operation to a method

-   Return Boolean to signal whether debugger should stay in interactive mode

[%inc vm_extend.py mark=memory %]

[%inc vm_extend.py mark=step %]

---

## Extensibility

-   Modify `interact` to choose operations from a lookup table

[%inc vm_extend.py mark=interact %]

---

## Extensibility

-   Build the table in the constructor

[%inc vm_extend.py mark=init %]

---

## Stop Here

-   A [%g breakpoint "breakpoint" %] tells the computer to stop at a particular instruction

    -   A [%g conditional_breakpoint "conditional breakpoint" %] stops if a condition is true

---

## Breakpoint Sets

-   Design #1: store breakpoint addresses in a set for `run` to check

[% figure
   slug="debugger-beside"
   img="beside.svg"
   alt="Storing breakpoint addresses beside the program"
   caption="Storing breakpoints beside the program."
%]

---

## What Hardware Does

-   Replace actual instruction with new `brk` instruction

-   Look up the real instruction when we hit a `brk`

[% figure
   slug="debugger-break"
   img="break.svg"
   alt="Inserting breakpoint instructions"
   caption="Inserting breakpoints into a program."
%]

---

## Add Commands

-   Rely on parent class to initialize most of the table

-   Then add more entries

[%inc vm_break.py mark=init %]

---

## Setting and Clearing

[%inc vm_break.py mark=add %]

[%inc vm_break.py mark=clear %]

---

## Running

[%inc vm_break.py mark=run %]

---

<!--# class="summary" -->

## Summary

[% figure
   slug="debugger-concept-map"
   img="concept_map.svg"
   alt="Concept map for debugger"
   caption="Concepts for debugger."
%]
