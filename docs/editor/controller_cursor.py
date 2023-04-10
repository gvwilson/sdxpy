class Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def display(self):
        first, last = self._select()
        lines = self._model.lines(first, last)
        y = self._model.y()
        self._view.display(lines, y, 0)

    def event_loop(self):
        self.display()
        while True:
            key = self._view.getkey()
            if key in {"U", "u"}:
                self.up()
            elif key in {"D", "d"}:
                self.down()
            else:
                break

    def up(self):
        if self._model.y() > 0:
            self._model.y(-1)
        self.display()

    def down(self):
        if self._model.y() < (self._model.num_lines() - 1):
            self._model.y(1)
        self.display()

    def _select(self):
        height = self._view.height()
        num_lines = self._model.num_lines()
        y = self._model.y()
        assert 0 <= y < num_lines
        # all lines fit in window => show all of them
        if num_lines <= height:
            first, last = 0, num_lines
        # show the last few lines
        elif (num_lines - y) <= height:
            first, last = num_lines - height, num_lines
        # show slice
        else:
            first, last = y, y + height
        assert 0 <= first <= last <= num_lines
        assert (last - first) <= height
        return first, last
