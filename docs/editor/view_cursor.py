class View:
    def __init__(self, screen, height, width):
        self._screen = screen
        self._height = height
        self._width = width

    def initialize(self):
        self._screen.clear()

    def height(self):
        return self._height

    def width(self):
        return self._width

    def display(self, lines, screen_y, screen_x):
        self._screen.clear()
        assert len(lines) <= self._height
        for (i, line) in enumerate(lines):
            self._screen.addstr(i, 0, line[:self._width])
        for i in range(len(lines), self._height):
            self._screen.addstr(i, 0, "")
        self._screen.refresh()
        self._screen.move(screen_y, screen_x)

    def getkey(self):
        return self._screen.getkey()
