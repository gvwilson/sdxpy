import sys
from curses import wrapper

from model_original import Model
from view_slice import View
from controller_up_down import Controller
from utils import make_lines

def main(screen, height, width, lines):
    model = Model(lines)
    view = View(screen, height, width)
    controller = Controller(model, view)
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
