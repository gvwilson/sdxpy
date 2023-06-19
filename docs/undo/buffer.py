from util import ROW, COL

class Buffer:
    def __init__(self, lines):
        self._lines = lines[:]
        self._top = 0
        self._height = None

    def lines(self):
        return self._lines[self._top:self._top + self._height]

    def nrow(self):
        return len(self._lines)

    def ncol(self, row):
        return len(self._lines[row])

    def set_height(self, height):
        self._height = height

    def transform(self, pos):
        result = (pos[ROW] - self._top, pos[COL])
        return result

    def scroll(self, row, col):
        old = self._top
        if (row == self._top - 1) and self._top > 0:
            self._top -= 1
        elif (row == self._bottom()) and \
             (self._bottom() < self.nrow()):
            self._top += 1

    def _bottom(self):
        return self._top + self._height
