import curses

from buffer import Buffer
from cursor import Cursor
from window import Window
from util import ROW, setup

class App:
    TRANSLATE = {
        "\x18": "CONTROL_X"
    }

    def __init__(self, size, lines):
        self._size = size
        self._lines = lines
        self._running = True
        self._screen = None
        self._window = None
        self._buffer = None
        self._cursor = None

    def __call__(self, screen):
        self._setup(screen)
        self._run()

    def __str__(self):
        return f"App(S={self._screen}, W={self._window}, B={self._buffer}, C={self._cursor})"

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
        self._cursor = Cursor(self._buffer, self._window)

    def _run(self):
        self._buffer.set_height(self._window.size()[ROW])
        while self._running:
            self._window.draw(self._buffer.lines())
            screen_pos = self._buffer.transform(self._cursor.pos())
            self._screen.move(*screen_pos)
            self._interact()
            self._buffer.scroll(*self._cursor.pos())

    def _interact(self):
        key = self._screen.getkey()
        key = self.TRANSLATE.get(key, key)
        name = f"_do_{key}"
        if hasattr(self, name):
            getattr(self, name)()
        self._add_log(key)

    def _add_log(self, key):
        pass

    def get_log(self):
        return []

    def _do_CONTROL_X(self):
        self._running = False

    def _do_KEY_UP(self):
        self._cursor.up()

    def _do_KEY_DOWN(self):
        self._cursor.down()

    def _do_KEY_LEFT(self):
        self._cursor.left()

    def _do_KEY_RIGHT(self):
        self._cursor.right()

if __name__ == "__main__":
    size, lines = setup()
    app = App(size, lines)
    curses.wrapper(app)
