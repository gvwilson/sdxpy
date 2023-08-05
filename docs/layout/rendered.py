from placed import PlacedBlock, PlacedCol, PlacedRow

# [render]
class Renderable:
    def render(self, screen, fill):
        for ix in range(self.get_width()):
            for iy in range(self.get_height()):
                screen[self.y0 + iy][self.x0 + ix] = fill
# [/render]

# [derive]
class RenderedBlock(PlacedBlock, Renderable):
    pass

class RenderedCol(PlacedCol, Renderable):
    pass

class RenderedRow(PlacedRow, Renderable):
    pass
# [/derive]
