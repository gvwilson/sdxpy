import curses
import sys

from util import ROW, COL, setup
from clip_cursor import ClipBuffer
from clip_cursor_fixed import ClipCursorFixed, ClipAppFixed

class ViewportCursor(ClipCursorFixed):
    def __init__(self, buffer, window):
        super().__init__(buffer)
        self._window = window

    def _fix(self):
        self._pos[COL] = min(
            self._pos[COL],
            self._buffer.ncol(self._pos[ROW]) - 1,
            self._window.size()[COL] - 1
        )

    def left(self):
        super().left()
        self._fix()

    def right(self):
        super().right()
        self._fix()

class ViewportBuffer(ClipBuffer):
    def __init__(self, lines):
        super().__init__(lines)
        self._top = 0
        self._height = None

    def set_height(self, height):
        self._height = height

    def transform(self, pos):
        result = pos[ROW] - self._top, pos[COL]
        return result

    def scroll(self, row, col):
        old = self._top
        if (row == self._top - 1) and self._top > 0:
            self._top -= 1
        elif (row == self._bottom()) and (self._bottom() < self.nrow()):
            self._top += 1

    def lines(self):
        return self._lines[self._top:self._top + self._height]

    def _bottom(self):
        return self._top + self._height

class ViewportApp(ClipAppFixed):
    def _make_buffer(self):
        self._buffer = ViewportBuffer(self._lines)

    def _make_cursor(self):
        self._cursor = ViewportCursor(self._buffer, self._window)

    def _run(self):
        self._buffer.set_height(self._window.size()[ROW])
        while self._running:
            self._window.draw(self._buffer.lines())
            screen_pos = self._buffer.transform(self._cursor.pos())
            self._screen.move(*screen_pos)
            self._interact()
            self._buffer.scroll(*self._cursor.pos())

if __name__ == "__main__":
    size, lines = setup()
    app = ViewportApp(size, lines)
    curses.wrapper(app)
