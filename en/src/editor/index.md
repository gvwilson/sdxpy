---
title: "An Editor"
syllabus:
- FIXME
---

-   Early text editors were line-at-a-time like our debugger
-   Most of us prefer to use full-screen interactive editors
-   Build a simple one to show how they work and how to test them
-   Based on [%i "Lorgat, Wasim" %][Wasim Lorgat][lorgat_wasim][%/i%]'s
    [tutorial][lorgat_editor]
    and [%i "Equivias, Cristian" %][Cristian Esquivias[%/i%]'s
    [`ted` editor][ted_editor].

## Logging Keystrokes {: #editor-keystrokes}

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

## Exercises {: #editor-exercises}
