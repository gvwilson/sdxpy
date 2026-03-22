import curses

from util import ROW, COL

class Window:
    def __init__(self, screen, size):
        self._screen = screen
        if size is None:
            self._size = (curses.LINES, curses.COLS)
        else:
            self._size = size

    def size(self):
        return self._size

    def draw(self, lines):
        self._screen.erase()
        for (y, line) in enumerate(lines):
            if 0 <= y < self._size[ROW]:
                self._screen.addstr(y, 0, line[:self._size[COL]])

    def __str__(self):
        return f"Window(S=screen, Z={self._size})"
