class Viewport:
    def __init__(self, model, height):
        self._model = model
        self._height = height
        self._top = 0
        self._bottom = min(model.num_lines(), self._height)

    def lines(self):
        return self._model.lines(self._top, self._bottom)

    def current(self):
        return self._top, self._bottom

    def up(self):
        if self._model.y() == 0:
            return
        if self._model.y(-1) < self._top:
            self._top -= 1
            self._bottom -= 1

    def down(self):
        if self._model.y() == (self._model.num_lines() - 1):
            return
        if self._model.y(1) >= self._bottom:
            self._top += 1
            self._bottom += 1

    def cursor(self):
        assert self._model.y() >= self._top
        return (self._model.y() - self._top, 0)
