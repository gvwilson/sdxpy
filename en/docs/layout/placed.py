from easy_mode import Block, Col, Row

# [block]
class PlacedBlock(Block):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.x0 = None
        self.y0 = None

    def place(self, x0, y0):
        self.x0 = x0
        self.y0 = y0

    def report(self):
        return [
            "block", self.x0, self.y0,
            self.x0 + self.width,
            self.y0 + self.height
        ]
# [/block]

# [col]
class PlacedCol(Col):
    def __init__(self, *children):
        super().__init__(*children)
        assert isinstance(self.children, list)
        self.x0 = None
        self.y1 = None

    def place(self, x0, y0):
        self.x0 = x0
        self.y0 = y0
        y_current = self.y0
        for child in self.children:
            child.place(x0, y_current)
            y_current += child.get_height()

    def report(self):
        return [
            "col", self.x0, self.y0,
            self.x0 + self.get_width(),
            self.y0 + self.get_height()
        ] + [c.report() for c in self.children]
# [/col]

# [row]
class PlacedRow(Row):
    def __init__(self, *children):
        super().__init__(*children)
        assert isinstance(self.children, list)
        self.x0 = None
        self.y0 = None

    def place(self, x0, y0):
        self.x0 = x0
        self.y0 = y0
        y1 = self.y0 + self.get_height()
        x_current = x0
        for child in self.children:
            child_y = y1 - child.get_height()
            child.place(x_current, child_y)
            x_current += child.get_width()

    def report(self):
        return [
            "row", self.x0, self.y0,
            self.x0 + self.get_width(),
            self.y0 + self.get_height()
        ] + [c.report() for c in self.children]
# [/row]
