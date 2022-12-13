import curses
import sys

class Window:
    def __init__(self, nrow, ncol):
        assert 0 <= nrow and 0 <= ncol
        self.nrow = nrow
        self.ncol = ncol

class Editor:
    # [init]
    def __init__(self):
        self.scr = None
        self.win = None
        self.running = True
        self.actions = {
            "Q": self.quit,
            "q": self.quit
        }
    # [/init]

    def __call__(self, scr, contents):
        self.setup(scr, contents)
        self.interact()

    def setup(self, scr, contents):
        self.scr = scr
        self.win = Window(curses.LINES - 1, curses.COLS - 1)

        self.scr.erase()
        for i, line in enumerate(contents[:self.win.nrow]):
            self.scr.addstr(i, 0, line[:self.win.ncol])

    # [interact]
    def interact(self):
        while self.running:
            key = self.scr.getkey()
            if key in self.actions:
                self.actions[key]()
    # [/interact]

    # [quit]
    def quit(self):
        self.running = False
    # [/quit]

if __name__ == "__main__":
    editor = Editor()
    contents = ['0123456789' * 100] * 1000
    try:
        curses.wrapper(editor, contents)
    except Exception as exc:
        print(exc)
