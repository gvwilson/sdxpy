import curses
import sys

from util import COL, ROW, start
from move_cursor import Cursor
from buffer_class import Buffer, BufferApp

# [cursor]
class ClipCursor(Cursor):
    def __init__(self, buffer):
        super().__init__()
        self._buffer = buffer

    def up(self):
        self._pos[ROW] = max(self._pos[ROW]-1, 0)

    def down(self):
        self._pos[ROW] = min(self._pos[ROW]+1, self._buffer.nrow()-1)

    def left(self):
        self._pos[COL] = max(self._pos[COL]-1, 0)

    def right(self):
        self._pos[COL] = min(
            self._pos[COL]+1,
            self._buffer.ncol(self._pos[ROW])-1
        )
# [/cursor]

# [other]
class ClipBuffer(Buffer):
    def nrow(self):
        return len(self._lines)

    def ncol(self, row):
        return len(self._lines[row])

class ClipApp(BufferApp):
    def _make_buffer(self):
        self._buffer = ClipBuffer(self._lines)

    def _make_cursor(self):
        self._cursor = ClipCursor(self._buffer)
# [/other]

if __name__ == "__main__":
    size, lines = start()
    app = ClipApp(size, lines)
    curses.wrapper(app)
