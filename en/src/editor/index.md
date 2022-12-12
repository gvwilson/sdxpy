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

[% inc file="show_large.py" keep="window" %]

-   Initialize it inside `main` and then trim what we're showing

[% inc file="show_large.py" keep="main" %]

## Exercises {: #editor-exercises}
