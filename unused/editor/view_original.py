class View:
    def __init__(self, height, render):
        self._height = height
        self._render = render

    def height(self):
        return self._height

    def display(self, lines):
        assert len(lines) <= self._height
        for (i, line) in enumerate(lines):
            self._render.show(i, line)
        for i in range(len(lines), self._height):
            self._render.show(i, "")
