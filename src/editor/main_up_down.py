import sys
from curses import wrapper

from model_original import Model
from view_up_down import View
from controller_up_down import Controller

def main(screen, height, lines):
    model = Model(lines)
    view = View(screen, height)
    controller = Controller(model, view)
    view.initialize()
    controller.event_loop()

if __name__ == "__main__":
    lines = ["this", "is", "a", "test"]
    height = int(sys.argv[1]) if (len(sys.argv) > 1) else len(lines)
    wrapper(lambda screen: main(screen, height, lines))
