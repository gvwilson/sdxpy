---
title: "A Debugger"
syllabus:
- FIXME
---

We have finally come to another of the questions that sparked this book:
how does a [%i "debugger" %]debugger[%/i%] work?
Debuggers are as much a part of good programmers' lives as version control
but are taught far less often
(in part, we believe, because it's harder to create homework questions for them).
This chapter builds a simple single-stepping debugger
for the virtual machine in [%x vm %]
and shows how we can test interactive applications.

Before we start work,
let's consolidate and reorganize the code in our virtual machine.
Its overall structure is shown below;
the methods all work as they did at the end of [%x vm %].

[% inc file="vm_base.py" omit="hide" %]

## One Step at a Time {: #debugger-step}

The virtual machine we're starting from loads a program and runs it to completion,
so it's either running or finished.
We want to add a third state for single-step execution,
so let's start by adding an [%g enumeration "enumeration" %] to `architecture.py`:

[% inc file="architecture.py" keep="state" %]

We could use strings to keep track of states,
but as soon as there are more than two there are likely to be many,
and having them spelled out makes it easier for the next person
to find out what they can be.
{: .continue}

The old `run` method was simple:
keep going until the program is finished.

[% inc file="vm_base.py" keep="run" %]

The new `run` method is necessarily more complicated.
The VM is initially in the `STEPPING` state,
because if we start it in the `RUNNING` state
we'll never have an opportunity to interact with it.
As long as it's not finished,
we ask the user for a command,
and then get the next instruction and execute it
if we're still in single-step mode:

[% inc file="vm_step.py" keep="run" %]

The interaction method needs to handle several cases:

1.  The user enters an empty line (i.e., presses return),
    in which case it loops around and waits for something else.

2.  The user asks to [%g disassemble "disassemble" %] the current instruction
    or show the contents of memory,
    in which case it does that and loops around.

3.  The user wants to run the next command,
    in which case the method breaks out of the loop
    without changing the VM's state.
    The `run` method will then see that the VM is still in single-stepping mode
    and execute a single instruction.

4.  The user wants to quit,
    and has either entered that command or pressed control-D
    (the Unix end-of-file character).
    Either way,
    `interact` changes the state to `FINISHED` and returns
    so that `run` will know it's done.

Finally,
the method that disassembles an instruction to show us what we're about to do
checks a [%g reverse_lookup "reverse lookup table" %]
to create a printable representation of an instruction and its operands:

[% inc file="vm_step.py" keep="disassemble" %]

We build the reverse lookup table from the `OPS` table in `architecture.py`
so that it's always in sync with the table we're using to construct operations.
If we wrote the reverse lookup table ourselves,
sooner or later we'd forget to update it when updating the forward lookup table:
{: .continue}

[% inc file="vm_step.py" keep="lookup" %]

## Interacting {: #debugger-interact}

[% inc file="vm_interact.py" %]

## Breakpoints {: #debugger-break}

[% inc file="vm_break.py" %]

## Testing

FIXME

[% fixme concept-map %]

## Exercises {: #debugger-exercises}

FIXME
