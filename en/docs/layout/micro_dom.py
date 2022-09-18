# [erase]
from wrapped import WrappedBlock, WrappedCol, WrappedRow

# [/erase]

# [mixin]
class DomMixin:
    def _common_eq(self, other):
        result = (
            isinstance(other, self.__class__)
            and self.tag == other.tag
            and self.width == other.width
            and self.height == other.height
        )
        return result

    def _child_eq(self, other):
        result = (len(self.children) == len(other.children)) and all(
            self.children[i] == other.children[i] for i in range(len(self.children))
        )
        return result


# [/mixin]


class DomBlock(WrappedBlock, DomMixin):
    def __init__(self, lines):
        lines = lines.split("\n")
        super().__init__(max(len(ln) for ln in lines), len(lines))
        self.tag = "text"
        self.lines = lines

    def __eq__(self, other):
        return self._common_eq(other) and (self.lines == other.lines)

    def __str__(self):
        return f"block[{repr('@'.join(self.lines))}]"


# [col]
class DomCol(WrappedCol, DomMixin):
    def __init__(self, width, height, *children):
        super().__init__(*children)
        self.width = width
        self.height = height
        self.tag = "col"

    def __eq__(self, other):
        return self._common_eq(other) and self._child_eq(other)

    # [omit]
    def __str__(self):
        return f"col[{'|'.join(str(c) for c in self.children)}]"

    # [/omit]


# [/col]


class DomRow(WrappedRow, DomMixin):
    def __init__(self, width, height, *children):
        super().__init__(width, *children)
        self.height = height
        self.tag = "row"

    def __eq__(self, other):
        return self._common_eq(other) and self._child_eq(other)

    def __str__(self):
        return f"row[{'|'.join(str(c) for c in self.children)}]"
