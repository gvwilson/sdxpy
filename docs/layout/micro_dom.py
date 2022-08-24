# [erase]
from wrapped import WrappedBlock, WrappedCol, WrappedRow
# [/erase]

# [mixin]
class DomMixin:
    def find_rules(self, css):
        self.rules = css.find_rules(self)
        if hasattr(self, "children"):
            for child in self.children:
                child.find_rules(css)

    def _common_init(self, tag):
        self.tag = tag
        self.rules = None

    def _common_eq(self, other):
        result = isinstance(other, self.__class__) and \
            self.tag == other.tag and \
            self.rules == other.rules
        return result

    def _common_child_eq(self, other):
        result = (len(self.children) == len(other.children)) and \
            all(self.children[i] == other.children[i] for i in range(len(self.children)))
        return result
# [/mixin]
    

class DomBlock(WrappedBlock, DomMixin):
    def __init__(self, lines):
        lines = lines.split("\n")
        super().__init__(
            max(len(ln) for ln in lines),
            len(lines)
        )
        self.lines = lines
        self._common_init("text")

    def __eq__(self, other):
        return self._common_eq(other) and \
            (self.lines == other.lines)

    def __str__(self):
        return f"block[{repr('@'.join(self.lines))}]"


# [col]
class DomCol(WrappedCol, DomMixin):
    def __init__(self, attributes, *children):
        super().__init__(*children)
        self.attributes = attributes
        self._common_init("col")

    def __eq__(self, other):
        return self._common_eq(other) and \
            (self.attributes == other.attributes) and \
            self._common_child_eq(other)
    # [omit]
    def __str__(self):
        return f"col[{'|'.join(str(c) for c in self.children)}]"
    # [/omit]
# [/col]


class DomRow(WrappedRow, DomMixin):
    def __init__(self, attributes, *children):
        super().__init__(0, *children)
        self.attributes = attributes
        self._common_init("row")

    def __eq__(self, other):
        return self._common_eq(other) and \
            (self.attributes == other.attributes) and \
            self._common_child_eq(other)

    def __str__(self):
        return f"row[{'|'.join(str(c) for c in self.children)}]"
