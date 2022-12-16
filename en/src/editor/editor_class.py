import curses
import sys

class Window:
    def __init__(self, nrow, ncol):
        assert 0 <= nrow and 0 <= ncol
        self.nrow = nrow
        self.ncol = ncol

# [editor]
class Editor:
    def __init__(self):
        self.scr = None
        self.win = None

    def __call__(self, scr, buffer):
        self.setup(scr, buffer)
        self.interact()
# [/editor]

# [setup]
    def setup(self, scr, buffer):
        self.scr = scr
        self.win = Window(curses.LINES - 1, curses.COLS - 1)

        self.scr.erase()
        for i, line in enumerate(buffer[:self.win.nrow]):
            self.scr.addstr(i, 0, line[:self.win.ncol])
# [/setup]

# [interact]
    def interact(self):
        while True:
            key = self.scr.getkey()
            if key in "Qq":
                break
# [/interact]

# [launch]
if __name__ == "__main__":
    editor = Editor()
    buffer = ['0123456789' * 100] * 1000
    try:
        curses.wrapper(editor, buffer)
    except Exception as exc:
        print(exc)
# [/launch]
