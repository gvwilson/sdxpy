import curses

from util import start
from main_app import MainApp

# [main]
class DispatchApp(MainApp):
    def __init__(self, size, lines):
        super().__init__(size, lines)
        self._running = True

    def _run(self):
        while self._running:
            self._window.draw(self._lines)
            self._screen.move(*self._cursor.pos())
            self._interact()
# [/main]

    # [interact]
    TRANSLATE = {
        "\x18": "CONTROL_X"
    }

    def _interact(self):
        key = self._screen.getkey()
        key = self.TRANSLATE.get(key, key)
        name = f"_do_{key}"
        if hasattr(self, name):
            getattr(self, name)()

    def _do_CONTROL_X(self):
        self._running = False

    def _do_KEY_UP(self):
        self._cursor.up()
    # [/interact]

    def _do_KEY_DOWN(self):
        self._cursor.down()

    def _do_KEY_LEFT(self):
        self._cursor.left()

    def _do_KEY_RIGHT(self):
        self._cursor.right()

if __name__ == "__main__":
    size, lines = start()
    app = DispatchApp(size, lines)
    curses.wrapper(app)
