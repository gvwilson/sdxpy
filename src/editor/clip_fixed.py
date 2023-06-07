import curses
import sys

from util import COL, ROW, setup
from clip_cursor import ClipCursor, ClipApp

class ClipCursorFixed(ClipCursor):
    def up(self):
        super().up()
        self._fix()

    def down(self):
        super().down()
        self._fix()

    def _fix(self):
        self._pos[COL] = min(self._pos[COL], (self._buffer.ncol(self._pos[ROW]) - 1))

class ClipAppFixed(ClipApp):
    def _make_cursor(self):
        self._cursor = ClipCursorFixed(self._buffer)

if __name__ == "__main__":
    size, lines = setup()
    app = ClipAppFixed(size, lines)
    curses.wrapper(app)
