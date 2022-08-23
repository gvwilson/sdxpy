# [erase]
from wrapped import WrappedBlock, WrappedCol, WrappedRow
# [/erase]

class DomBlock(WrappedBlock):
    def __init__(self, lines):
        super().__init__(
            max(len(ln) for ln in lines.split("\n")),
            len(lines)
        )
        self.lines = lines
        self.tag = "text"
        self.rules = None

    def find_rules(self, css):
        self.rules = css.find_rules(self)


class DomCol(WrappedCol):
    def __init__(self, attributes, *children):
        super().__init__(*children)
        self.attributes = attributes
        self.tag = "col"
        self.rules = None

    def find_rules(self, css):
        self.rules = css.find_rules(self)
        for child in self.children:
            child.find_rules(css)


class DomRow(WrappedRow):
    def __init__(self, attributes, *children):
        super().__init__(0, *children)
        self.attributes = attributes
        self.tag = "row"
        self.rules = None

    def find_rules(self, css):
        self.rules = css.find_rules(self)
        for child in self.children:
            child.find_rules(css)
