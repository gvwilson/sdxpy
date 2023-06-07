class Controller:
    def __init__(self, viewport, view):
        self._viewport = viewport
        self._view = view

    def display(self):
        lines = self._viewport.lines()
        cursor = self._viewport.cursor()
        self._view.display(lines, *cursor)

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
        self._viewport.up()
        self.display()

    def down(self):
        self._viewport.down()
        self.display()
