import sys
from curses import wrapper

from model_editor import Model
from viewport_editor import Viewport
from view_cursor import View
from controller_editor import Controller
from utils import make_lines

def main(screen, height, width, lines):
    model = Model(lines)
    viewport = Viewport(model, height)
    view = View(screen, height, width)
    controller = Controller(viewport, view)
    view.initialize()
    controller.event_loop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} height width")
        sys.exit(1)
    height = int(sys.argv[1])
    width = int(sys.argv[2])
    lines = make_lines(height, width)
    wrapper(lambda screen: main(screen, height, width, lines))
