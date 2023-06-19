from util import ROW, COL

class Cursor:
    def __init__(self, buffer, window):
        self._buffer = buffer
        self._window = window
        self._pos = [0, 0]

    def pos(self):
        return tuple(self._pos)

    def up(self):
        self._pos[ROW] = max(self._pos[ROW] - 1, 0)
        self._fix()

    def down(self):
        self._pos[ROW] = min(self._pos[ROW] + 1, self._buffer.nrow() - 1)
        self._fix()

    def left(self):
        self._pos[COL] = max(self._pos[COL] - 1, 0)
        self._fix()

    def right(self):
        self._pos[COL] = min(
            self._pos[COL] + 1,
            self._buffer.ncol(self._pos[ROW]) - 1
        )
        self._fix()

    def _fix(self):
        self._pos[COL] = min(
            self._pos[COL],
            self._buffer.ncol(self._pos[ROW]) - 1,
            self._window.size()[COL] - 1
        )
