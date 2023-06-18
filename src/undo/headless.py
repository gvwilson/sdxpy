from app import App
from util import ROW, COL
from window import Window

class HeadlessScreen:
    def __init__(self, size, keystrokes):
        self._size = size
        self._keys = keystrokes
        self._i_key = 0
        self.erase()

    def getkey(self):
        if self._i_key == len(self._keys):
            key = "CONTROL_X"
        else:
            key = self._keys[self._i_key]
            self._i_key += 1
        return key

    def move(self, row, col):
        assert 0 <= row < self._size[ROW]
        assert 0 <= col < self._size[COL]

    def erase(self):
        self._display = ['_' * self._size[COL] for _ in range(self._size[ROW])]

    def addstr(self, row, col, text):
        assert 0 <= row < self._size[ROW]
        assert col == 0
        assert len(text) <= self._size[COL]
        self._display[row] = text + self._display[row][len(text):]

    def display(self):
        return self._display

    def __str__(self):
        return f"Screen(Z={self._size})"

class HeadlessWindow(Window):
    def __init__(self, screen, size):
        assert size is not None and len(size) == 2
        super().__init__(screen, size)

class HeadlessApp(App):
    def __init__(self, size, lines):
        super().__init__(size, lines)
        self._log = []

    def get_log(self):
        return self._log

    def _add_log(self, key):
        self._log.append((key, self._cursor.pos(), self._screen.display()))

    def _make_window(self):
        self._window = HeadlessWindow(self._screen, self._size)
