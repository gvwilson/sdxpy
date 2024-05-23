---
template: slides
title: "Undo and Redo"
---

## The Problem

-   Want to change files as well as viewing them

-   So modify the file viewer of [%x viewer %] to allow editing

-   And since people make mistakes when editing, implement undo

---

## Starting Point

-   `Window` can draw lines and report its size

-   `Buffer` stores lines of text,
    keeps track of a viewport,
    and transforms buffer coordinates to screen coordinates

-   `Cursor` knows its position in the buffer
    and can move up, down, left, and right

-   `App` makes a window, a buffer, and a cursor,
    then maps keys to actions

[% figure
   slug="undo-classes"
   img="classes.svg"
   alt="Classes in file viewer"
   caption="Relationships between classes in file viewer"
%]

---

## A Headless Screen

-   Create a [%g headless "headless" %] screen for testing

-   Store current state of display in rectangular grid

-   Take a list of keystrokes (for simulation)

    -   Would have made more sense for `App` to have a method
        that gets keystrokes

---

## A Headless Screen

[%inc headless.py mark=screen %]

---

## Bad But Necessary

-   Also need to define `HeadlessWindow` to take a size
    and pass it to the screen

[%inc headless.py mark=window %]

---

## Logging

-   Record keys, cursor position, and screen contents for testing

[%inc headless.py mark=app %]

---

## Testing

[%inc test_headless.py mark=example %]

-   Last key is always `CONTROL_X` (exit)

---

## Insertion and Deletion

[%inc insert_delete.py mark=buffer %]

-   Delete character *under* the cursor, not to the left

-   A little defensive programming as well

---

## Application

[%inc insert_delete.py mark=app %]

[%inc insert_delete.py mark=action %]

---

## Application

[%inc insert_delete.py mark=dispatch %]

-   Add `_get_key` to return family (generic) and key (specific)

---

## Testing

-   Write a function to make the fixture and run the test

[%inc test_insert_delete.py mark=fixture %]

-   Tests are straightforward

[%inc test_insert_delete.py mark=example %]

---

<!--# class="aside" -->

## Edge Case

-   Can't delete when in an empty screen

[%inc test_insert_delete.py mark=empty %]

-   Our focus is implementing undo, so leave this for an exercise

---

## Recording History

-   In order to undo things we have to:

    1.  keep track of *actions* and reverse them, or

    2.  keep track of *state* and restore it

-   Recording actions requires less space but can be trickier to implement

-   Have actions append entries to a log

---

## The Simple Approach

[%inc history.py mark=app %]

-   What about undoing cursor movement?

-   And do we write an interpreter for these log records?

---

## Verbs as Nouns

-   Use the [%g command_pattern "Command" %] design pattern

-   Each action (verb) is an object (noun)
    with methods to go forward and backward

-   Every action is derived from an abstract base class

[%inc action.py mark=Action %]

---

## Insertion

[%inc action.py mark=Insert %]

---

## Deletion

[%inc action.py mark=Delete %]

---

## Movement

[%inc action.py mark=Move %]

-   Give `Cursor` methods to move in a particular direction (by name)
    and move to a particular location

---

## Application

[%inc action.py mark=interact %]

-   Create the action object

-   Call its `.do` method

-   Modify all action methods to take a key to simplify the code a little

---

## Application

[%inc action.py mark=actions %]

-   And it *almost* works!

-   Our first implementation of `Undo` creates an infinite loop
    because it puts itself on the undo stack
    and then does the action on the top of the stack

---

## Finally

-   Modify `Action` to have a `.save` method that returns `True`

-   Override in `Undo`

[%inc undoable.py mark=Undo %]

-   Only add object to undo stack if `.save` is `True`
    -   Could define `Action.post_action`
        to add the action to the undo stack

---

<!--# class="summary" -->

## Summary

[% figure
   slug="undo-concept-map"
   img="concept_map.svg"
   alt="Concept map of undo"
   caption="Concept map"
%]
