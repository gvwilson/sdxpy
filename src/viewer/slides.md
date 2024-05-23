---
template: slides
title: "A File Viewer"
---

## The Problem

-   We have been editing a lot of files

-   How can we display a text file in a window?

-   How can we move around in that file?

-   How we can change it will be the topic of [%x undo %]

---

## Curses

[%inc first_curses.py %]

-   The [curses][py_curses] library handles interaction with a text terminal

-   `curses.wrapper` takes a function of a single argument

-   Does setup, then calls that function with a standard screen

-   This program just gobbles keystrokes: stop it with Ctrl-C

---

## Debugging

-   Printing messages or single-stepping with a debugger is tricky

-   Create a simple logging function

[%inc util.py mark=log %]

---

## Debugging

[%inc logging_curses.py mark=show %]

-   Print representation of characters to file (so that `\n` shows up)

-   Exit cleanly

---

## Showing Lines

[%inc show_lines.py mark=main %]

-   Screen coordinates put (0, 0) in the upper left

-   And use (y, x) rather than (x, y)

---

## Showing Lines

[%inc show_lines.py mark=run %]

-   Make lines for testing rather than showing file

-   Open the log file

-   Use `lambda` to make a one-parameter function for `curses.wrapper`

---

## Making Lines

[%inc util.py mark=lines %]
[%inc make_lines.out %]

---

## Windowing

-   Run program with 100 lines (or anything else larger than screen)

-   `_curses.error: addwstr() returned ERR` because trying to draw outside screen

-   So create a `Window` class that knows how big the screen is

[%inc use_window.py mark=window %]

---

## Windowing

[%inc use_window.py mark=main %]

-   Can't create `Window` before calling `curses.wrapper` because it needs the screen

-   [%g delayed_construction "Delayed construction" %]

---
<!--# class="aside" -->

## Optimization

-   `Window` re-draws everything after every keystroke

-   Fast enough that people (usually) won't notice

-   But an obvious target for optimization

---

## Sizing the Window

-   Allow users to specify how big the window appears to be

-   Helps with testing

[%inc size_window.py mark=window %]

---

## Two Dimensions

-   Use `ROW` and `COL` instead of 0 and 1 (or `R` and `C`)

-   Should really create an [%g enumeration "enumeration" %]

[%inc util.py mark=coord %]
[%inc cursor_const.py mark=window omit=omit %]

---

## Moving the Cursor

[%inc move_cursor.py mark=cursor %]

-   `Cursor.pos` returns location as tuple so caller can't modify it

---

## Moving the Cursor

[%inc move_cursor.py mark=main %]

-   [%g spread "Spread" %] position into `stdscr.move`

-   Screen's `getkey` method returns names of cursor keys

---

## Boom

-   We can move right or below text

-   And blow up when moving off left of screen or off top with
    `_curses.error: wmove() returned ERR`

-   Do some [%g refactor "refactoring" %] before fixing this problem

---

## Application Class

-   Create an object with a `__call__` method

-   Fool `curses.wrapper` into thinking we have given it a function

[%inc main_app.py mark=main %]

---

## Application Class

[%inc main_app.py mark=run %]
[%inc main_app.py mark=launch %]

---

## Dispatching Keystrokes

-   Find and call key handlers via [%g dynamic_dispatch "dynamic dispatch" %]

[%inc dispatch_keys.py mark=interact %]

---

## Dispatching Keystrokes

[%inc dispatch_keys.py mark=main %]

-   Use a member variable `self._running` so that every other method
    *doesn't* have to return a "keep running" flag

-   Add `TRANSLATE` to turn things like Ctrl-X into strings `CONTROL_X`

    -   Got the value by looking in our log file

---
<!--# class="aside" -->

## Inheritance

-   `DispatchApp` is a child of `MainApp` so that we can recycle initialization

-   `DispatchApp.__init__` [%g upcall "upcalls" %] to `MainApp.__init__`

-   Probably wouldn't create multiple classes in a real program,
    but simplifies exposition when teaching

-   Had to move some earlier code around when writing later classes
    to make everything work cleanly

-   *This is normal*

---

## Managing the Buffer

[%inc buffer_class.py mark=buffer %]

-   Doesn't do much yet, but will later keep track of viewable region

-   Makes a copy of `lines` so that other code can't change its internals

---

## Changing the Application

[%inc buffer_class.py mark=app %]

---
<!--# class="aside" -->

## Factory Methods

-   Want to re-use as much of `BufferApp` as possible

-   If `setup` calls constructors to create window, buffer, and cursor,
    we have to rewrite it each time

-   Putting constructor calls in [%g factory_method "factory methods" %]
    allows us to override them one by one

-   Could pass classes into `BufferApp` constructor…

-   …but later on, these objects will need to reference each other

-   Again, moving things around like this is normal

---

## Clipping

[%inc clip_cursor.py mark=cursor %]

---

## Clipping

[%inc clip_cursor.py mark=other %]

-   Add methods to the buffer

-   Construct different cursor and buffer objects
    without changing anything else in the application

---

## A Bug

-   Move to end of line and go up to shorter line
    leaves cursor outside the text

[%inc clip_fixed.py mark=cursor %]

-   Good design if there's one obvious place to make a change

---

## Viewport

-   Can still move below the window because cursor is in buffer space not window space

-   What if the buffer is bigger than the window?

-   Need a [%g viewport "viewport" %] to track
    the currently-visible portion of the buffer

    -   Do vertical here and leave horizontal for exercises

---

## Buffer

[%inc viewport.py mark=buffer %]

---

## Buffer

[%inc viewport.py mark=transform %]
[%inc viewport.py mark=scroll %]

---

## Application

[%inc viewport.py mark=app %]

-   Transform buffer coordinates into screen coordinates

-   This class is where we need separate factory methods

---

## Cursor

[%inc viewport.py mark=cursor %]

---

<!--# class="summary" -->

## Summary

[% figure
   slug="viewer-concept-map"
   img="concept_map.svg"
   alt="Concept map of file viewer"
   caption="Concept map"
%]
