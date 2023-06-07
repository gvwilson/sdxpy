class Model:
    def __init__(self, text):
        if isinstance(text, str):
            text = text.split("\n")
        self._lines = text
        self._y = 0

    def num_lines(self):
        return len(self._lines)

    def lines(self, top, bottom):
        return self._lines[top:bottom]

    def y(self, change=None):
        if change is not None:
            self._y += change
        return self._y

    def insert(self, character):
        self._lines[self._y] = character + self._lines[self._y]
