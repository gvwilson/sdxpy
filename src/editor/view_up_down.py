class View:
    def __init__(self, screen, height):
        self._screen = screen
        self._height = height

    def initialize(self):
        self._screen.clear()

    def height(self):
        return self._height

    def display(self, lines):
        assert len(lines) <= self._height
        for (i, line) in enumerate(lines):
            self._screen.addstr(i, 0, line)
        for i in range(len(lines), self._height):
            self._screen.addstr(i, 0, "")
        self._screen.refresh()

    def getkey(self):
        return self._screen.getkey()
