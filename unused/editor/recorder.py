class Recorder:
    def __init__(self):
        self.clear()

    def show(self, y, line):
        self._lines.append((y, line))

    def clear(self):
        self._lines = []

    def get(self):
        return self._lines
