from placed import PlacedBlock, PlacedCol, PlacedRow

# [blockcol]
class WrappedBlock(PlacedBlock):
    def wrap(self):
        return self

class WrappedCol(PlacedCol):
    def wrap(self):
        return PlacedCol(*[c.wrap() for c in self.children])
# [/blockcol]

# [row]
class WrappedRow(PlacedRow):
    def __init__(self, width, *children):
        super().__init__(*children)
        assert width >= 0, "Need non-negative width"
        self.width = width

    def get_width(self):
        return self.width

    # [wrap]
    def wrap(self):
        children = [c.wrap() for c in self.children]
        rows = self._bucket(children)
        new_rows = [PlacedRow(*r) for r in rows]
        new_col = PlacedCol(*new_rows)
        return PlacedRow(new_col)
    # [/wrap]

    # [bucket]
    def _bucket(self, children):
        result = []
        current_row = []
        current_x = 0

        for child in children:
            child_width = child.get_width()
            if (current_x + child_width) <= self.width:
                current_row.append(child)
                current_x += child_width
            else:
                result.append(current_row)
                current_row = [child]
                current_x = child_width
        result.append(current_row)

        return result
    # [/bucket]
# [/row]
