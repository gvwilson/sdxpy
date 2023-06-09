import curses
import sys

from util import COL, ROW, setup
from d2 import Window
from move_cursor import Cursor

class MainApp:
    def __init__(self, size, lines):
        self._size = size
        self._lines = lines

    def __call__(self, screen):
        self._setup(screen)
        self._run()

    def _setup(self, screen):
        self._screen = screen
        self._window = Window(self._screen, self._size)
        self._cursor = Cursor()

    def _run(self):
        while True:
            self._window.draw(self._lines)
            self._screen.move(*self._cursor.pos())
            key = self._screen.getkey()
            if key == "KEY_UP": self._cursor.up()
            elif key == "KEY_DOWN": self._cursor.down()
            elif key == "KEY_LEFT": self._cursor.left()
            elif key == "KEY_RIGHT": self._cursor.right()
            elif key.lower() == "q":
                return

if __name__ == "__main__":
    size, lines = setup()
    app = MainApp(size, lines)
    curses.wrapper(app)
