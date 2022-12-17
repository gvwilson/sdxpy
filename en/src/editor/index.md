---
title: "An Editor"
syllabus:
- FIXME
---

Early text editors were line-at-a-time applications like the debugger of [%x debugger %].
Most people prefer to use full-screen interactive editors,
so this chapters builds a simple one to show how they work.
Our design follows [%i "Lorgat, Wasim" %][Wasim Lorgat][lorgat_wasim][%/i%]'s
[tutorial][lorgat_editor] closely,
and borrows a few ideas from [%i "Equivias, Cristian" %][Cristian Esquivias[%/i%]'s
[`ted` editor][ted_editor] as well.

Our starting point is Python's [curses][py_curses] module.
It gives programs access to a library called `curses`,
which provides a uniform interface to terminal applications on several platforms.
These applications can do much more than most people realize,
and terminal interface libraries like [Textualize][textualize]
can do most of what a modern browser can do,
but we will stick to the basics for now.

## Logging Keystrokes {: #editor-keystrokes}

Let's started by writing a terminal application
that does nothing except wait for a command to quit:

[% inc file="simplest.py" %]

Our application is in a function called `main`.
Instead of calling it directly,
we pass it to `curses.wrapper`,
which initializes the terminal library for us
and then calls our function with an object
that represents the terminal.
`main` then goes into a loop that gets a keystroke
and quits if the key is either 'Q' or 'q'.

When we run this program our terminal window goes blank
and stays that way until we quit.

[% inc file="log_keystrokes.py" %]

-   Test interactively or use standard input

[% inc pat="log_keystrokes.*" fill="sh out" %]

## Displaying a File {: #editor-file}

-   As mentioned in [%x layout %],
    screen's [%i "coordinate system" %]coordinate system[%/i%] is upside down:
    y=0 is at the top
-   Other than that, ask the screen to display lines and then wait for a quit command

[% inc file="show_file.py" keep="main" %]

-   Get the file from anywhere

[% inc file="show_file.py" keep="launch" %]

-   Works, but only for the right kind of file
-   Try to display a thousand lines, each a thousand characters long

[% inc file="fail_large.py" keep="launch" %]
[% inc file="fail_large.out" %]

-   Problem is we're trying to write outside the window
-   Solution is to trim what we're displaying
-   Define a `Window` class to keep track of the display area
    -   Why `-1`?

[% inc file="show_large.py" keep="window" %]

-   Initialize it inside `main` and then trim what we're showing

[% inc file="show_large.py" keep="main" %]

## An Editor Object {: #editor-object}

-   Functions with lots of parameters are hard to manage
-   But `curses.wrapper` requires a function
-   Solution: create a class with a `__call__` method
    -   Must use [%i "Delayed Construction pattern" %][%g delayed_construction_pattern "Delayed Construction" %][%/i%] design pattern
-   Editor

[% inc file="editor_class.py" keep="editor" %]

-   Setup

[% inc file="editor_class.py" keep="setup" %]

-   Interaction

[% inc file="editor_class.py" keep="interact" %]

-   Launch

[% inc file="editor_class.py" keep="launch" %]

-   Then add a lookup table of actions (to be fleshed out later)

[% inc file="editor_interact.py" keep="init" %]

-   Each action must be a method of no arguments (other than `self`)

[% inc file="editor_interact.py" keep="quit" %]

## Moving Around {: #editor-move}

-   Define a `Cursor` to keep track of location

[% inc file="editor_move.py" keep="cursor" %]

-   Move around in response to keys
    -   But stay inside the window *and* the text content

[% inc file="editor_move.py" keep="move" %]

-   Seems to work, except moving from end of long line up or down to shorter line
    -   Testing is hard…
-   Solution is to move and then limit the column

[% inc file="editor_move_fixed.py" keep="move" %]

-   But we can only see the top left portion of the file
-   Want to show the available content, which means mapping one coordinate system to another
-   Enhance the `Window` class to keep track of the top row it's displaying
    -   Keeping track of column will be left as an exercise

[% inc file="editor_scroll.py" keep="window" %]

-   When we display, we show the rows that are currently visible

[% inc file="editor_scroll.py" keep="display" %]

-   The `translate` method turns the cursor's position into a content position

[% inc file="editor_scroll.py" keep="translate" %]

-   Finally, we adjust the screen when moving

[% inc file="editor_scroll.py" keep="updown" %]

-   Keeping track of the coordinate systems and their relation to each other is hard
-   Diagrams, diagrams, diagrams…

## Editing {: #editor-editing}

-   Long overdue: create a `Buffer` class to store the text being edited
    -   Check that it's being constructed with a list of strings (rather than a single string)
    -   Use `__len__` and `__getitem__` so that it looks like a list (no existing code needs to change)

[% inc file="editor_buffer.py" keep="buffer" %]

-   Only significant change to `Editor` is to ask the buffer what its bottom line is:

[% inc file="editor_buffer.py" keep="down" %]

-   Add that method to `Buffer`

[% inc file="editor_buffer.py" keep="bottom" %]

-   Everything else just works, which is a sign of good design
-   Now define the set of characters users are allowed to insert
    -   For now, stick to visible characters plus space
    -   Handle newlines, tabs, etc. in the exercises
    -   Don't define this ourselves: Python's [string][py_string] module is already there
    -   Could add all the characters to `Editor.actions` so that they can be remapped, but leave that for exercises

[% inc file="editor_insert.py" keep="string" %]

-   Interaction changes
    -   If the character is a special action, do that
    -   Otherwise, if it's insertable, insert it and move right
    -   Otherwise, ignore it

[% inc file="editor_insert.py" keep="interact" %]

-   Go back to the `Buffer` class and insert the character

[% inc file="editor_insert.py" keep="insert" %]

-   We can now edit the buffer

## Exercises {: #editor-exercises}
