---
syllabus:
-   FIXME
depends:
-   viewer
---

-   Bring over viewer app
    -   `app.py`, `buffer.py`, `cursor.py`, `window.py`, `util.py`
    -   `Window`, `Cursor`, `Buffer`, `App`
    -   Add call to `._add_log` to `App._interact` (another unanticipated hook)

-   Create headless versions
    -   `HeadlessScreen` replaces the `curses` screen
        -   Takes keystrokes as input (what we're simulating)
        -   Automatically generate Ctrl-X when out of keystrokes
        -   Store current state of display in rectangular grid
        -   Would make more sense for `App` to have a method that gets keys
    -   `HeadlessWindow` requires a size
        -   Violates Liskov Substitution Principle
    -   `HeadlessApp` fills in logging methods
    -   First tests make sure we can move around
    -   `headless.py`
    -   `test_headless.py`

-   Create insert/delete version
    -   `InsertDeleteBuffer` in `insert_delete.py`
        -   Add methods to insert and delete in buffer
	-   Delete character *under* cursor, not to the left
    -   `InsertDeleteApp` provides `_get_key` in the app to return (family, key)
        -   `_interact` dispatches to one of two cases (special-purpose or generic + key)
        -   Could define per-key method to make customization easier
    -   `test_insert_delete.py`
    -   But one test fails: empty screen (cursor isn't on top of a character)
        -   Our focus is undo, so we'll ignore this for now
	-   Tackle it in the exercises

-   Record history of insertions and deletions
    -   `HistoryApp` in `history.py` creates a list `_history`
    -   Modify `_do_INSERT` and `_do_DELETE` to append records
    -   Could add more logic to history recording, but this approach is broken anyway
    -   Insert, move, move, undo: where does it leave the cursor?
    -   Next step is to create objects that record actions
