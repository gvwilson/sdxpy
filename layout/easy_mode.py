# mccole:block
class Block:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
# mccole:/block

# mccole:row
class Row:
    def __init__(self, *children):
        self.children = list(children)

    def get_width(self):
        return sum([c.get_width() for c in self.children])

    def get_height(self):
        return max(
            [c.get_height() for c in self.children],
            default=0
        )
# mccole:/row

# mccole:col
class Col:
    def __init__(self, *children):
        self.children = list(children)

    def get_width(self):
        return max(
            [c.get_width() for c in self.children],
            default=0
        )

    def get_height(self):
        return sum([c.get_height() for c in self.children])
# mccole:/col
