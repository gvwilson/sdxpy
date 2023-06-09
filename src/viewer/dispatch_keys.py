import curses
import sys

from util import COL, ROW, setup
from main_app import MainApp

class DispatchApp(MainApp):
    TRANSLATE = {
        "\x18": "CONTROL_X"
    }

    def __init__(self, size, lines):
        super().__init__(size, lines)
        self._running = True

    def _run(self):
        while self._running:
            self._window.draw(self._lines)
            self._screen.move(*self._cursor.pos())
            self._interact()

    def _interact(self):
        key = self._screen.getkey()
        key = self.TRANSLATE.get(key, key)
        name = f"_do_{key}"
        if hasattr(self, name):
            getattr(self, name)()

    def _do_KEY_UP(self):
        self._cursor.up()

    def _do_KEY_DOWN(self):
        self._cursor.down()

    def _do_KEY_LEFT(self):
        self._cursor.left()

    def _do_KEY_RIGHT(self):
        self._cursor.right()

    def _do_CONTROL_X(self):
        self._running = False

if __name__ == "__main__":
    size, lines = setup()
    app = DispatchApp(size, lines)
    curses.wrapper(app)
