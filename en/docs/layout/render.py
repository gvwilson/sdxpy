def render(root):
    root.place(0, 0)
    width = root.get_width()
    height = root.get_height()
    screen = make_screen(width, height)
    draw(screen, root)
    return "\n".join("".join(ch) for ch in screen)

# [make_screen]
def make_screen(width, height):
    screen = []
    for i in range(height):
        screen.append([" "] * width)
    return screen
# [/make_screen]

# [draw]
def draw(screen, node, fill=None):
    fill = next_fill(fill)
    node.render(screen, fill)
    if hasattr(node, "children"):
        for child in node.children:
            fill = draw(screen, child, fill)
    return fill

def next_fill(fill):
    return "a" if fill is None else chr(ord(fill) + 1)
# [/draw]
