import curses
import sys

from util import setup
from d2 import Window
from dispatch_keys import DispatchApp
from move_cursor import Cursor

class Buffer:
    def __init__(self, lines):
        self._lines = lines[:]

    def lines(self):
        return self._lines

class BufferApp(DispatchApp):
    def __init__(self, size, lines):
        super().__init__(size, lines)

    def _setup(self, screen):
        self._screen = screen
        self._make_window()
        self._make_buffer()
        self._make_cursor()

    def _make_window(self):
        self._window = Window(self._screen, self._size)

    def _make_buffer(self):
        self._buffer = Buffer(self._lines)

    def _make_cursor(self):
        self._cursor = Cursor()

    def _run(self):
        while self._running:
            self._window.draw(self._buffer.lines())
            self._screen.move(*self._cursor.pos())
            self._interact()

if __name__ == "__main__":
    size, lines = setup()
    app = BufferApp(size, lines)
    curses.wrapper(app)
