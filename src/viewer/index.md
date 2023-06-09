-   `first_curses.py`: run a program with a screen
    -   Does nothing with keys
    -   Stop with Ctrl-C
    -   No way to see what it's doing (can't print)

-   `logging_curses.py`: create a log file
    -   Use `lambda` to create a function with the signature needed by `curses.wrapper`
    -   Print representation of characters to file (so that `\n` shows up)
    -   Exit cleanly

-   `show_lines.py`: show lines in location
    -   Screen coordinates put (0, 0) in the upper left
    -   Run `show_lines.py` with 1000 lines (anything larger than screen)
        -   `_curses.error: addwstr() returned ERR` because trying to draw off bottom of screen

-   `use_window.py`: fix problem with `show_lines.py`
    -   Create a `Window` class that knows how big the window is
        -   Can't create this and then pass it in to `main` because `curses.wrapper` creates `stdscr`
    -   Redraw all the lines each time: it's a *view* class

-   `size_window.py`: allow user to specify size of window
    -   Helps with testing

-   `d2.py`: use a tuple and constants `ROW` and `COL`
    -   Should create a class, but that's more effort than it's worth right now

-   `move_cursor.py`: create and move a cursor
    -   `Cursor.pos` returns (y, x) position as tuple (so that caller can't modify internals)
    -   Spread that into `stdscr.move`
    -   But can move right or below text
    -   And blow up when moving off left of screen or off top
    -   `_curses.error: wmove() returned ERR`

-   `main_app.py`: create an application object with a `__call__` method (required by `curses.wrapper`)
    -   Delayed instantiation of `Window`

-   `dispatch_keys.py`: find and call key handlers dynamically
    -   Use a member variable `self._running` and have `_handle_q` handle that
        so that other methods don't have to return anything
    -   But now can only quit with lower-case 'q' (and will want to insert that character)
    -   So add `TRANSLATE` to turn things like Ctrl-X into strings `CONTROL_X`

-   `buffer_class.py`: create a class to manage the buffer

-   `clip_cursor.py`: make sure cursor cannot move outside of lines
    -   But go to a long line and then move up to a shorter one
    -   `clip_fixed.py`

-   Can still move below the window because cursor is in buffer space not window space
-   What if the buffer is bigger than the window?
    -   Need a *viewport* to keep track of the portion of the buffer that is currently visible
    -   We'll do vertical and leave horizontal for exercises
-   `viewport.py`
    -   Add `transform` to transform cursor coordinates into screen coordinates
    -   Keep track of the top visible line
    -   Add a `bottom` method for convenience
    -   Move the `_top` marker up or down as needed
    -   Cursor needs to clip left and right as well as up and down

|                     | main   | window   | cursor            | buffer           | app            |
| ------------------- | ------ | -------- | ----------------- | ---------------- | -------------- |
| `first_curses.py`   | `main` |          |                   |                  |                |
| `logging_curses.py` | `main` |          |                   |                  |                |
| `show_lines.py`     | `main` |          |                   |                  |                |
| `use_window.py`     | `main` | `Window` |                   |                  |                |
| `size_window.py`    | `main` | `Window` |                   |                  |                |
| `d2.py`             | `main` | `Window` |                   |                  |                |
| `move_cursor.py`    | `main` |          | `Cursor`          |                  |                |
| `main_app.py`       |        |          |                   |                  | `MainApp`      |
| `dispatch_app.py`   |        |          |                   |                  | `DispatchApp`  |
| `buffer_class.py`   |        |          |                   | `Buffer`         | `BufferApp`    |
| `clip_cursor.py`    |        |          | `ClipCursor`      | `ClipBuffer`     | `ClipApp`      |
| `clip_fixed.py`     |        |          | `ClipCursorFixed` |                  | `ClipAppFixed` |
| `viewport.py`       |        |          | `ViewportCursor`  | `ViewportBuffer` | `ViewportApp`  |
