import curses
import sys

# [window]
class Window:
    def __init__(self, nrow, ncol):
        assert 0 <= nrow and 0 <= ncol
        self.nrow = nrow
        self.ncol = ncol
        self.row = 0

    def bottom(self):
        return self.row + self.nrow - 1

    def up(self, cur):
        if (cur.row == self.row - 1) and (self.row > 0):
            self.row -= 1

    def down(self, contents, cur):
        if (cur.row == self.bottom() + 1) and (self.bottom() < len(contents) - 1):
            self.row += 1
# [/window]

    # [translate]
    def translate(self, cur):
        return cur.row - self.row, cur.col
    # [/translate]

class Cursor:
    def __init__(self, row, col):
        assert 0 <= row and 0 <= col
        self.row = row
        self.col = col

class Editor:
    def __init__(self):
        self.scr = None
        self.win = None
        self.cur = None
        self.running = True
        self.actions = {
            "Q": self.quit,
            "q": self.quit,
            "KEY_UP": self.up,
            "KEY_DOWN": self.down,
            "KEY_LEFT": self.left,
            "KEY_RIGHT": self.right
        }

    def __call__(self, scr, contents):
        self.setup(scr, contents)
        self.interact()

    def setup(self, scr, contents):
        self.scr = scr
        self.contents = contents
        self.win = Window(curses.LINES - 1, curses.COLS - 1)
        self.cur = Cursor(0, 0)

    def interact(self):
        while self.running:
            self.display()
            key = self.scr.getkey()
            if key in self.actions:
                self.actions[key]()

    # [display]
    def display(self):
        self.scr.erase()
        visible = self.contents[self.win.row : (self.win.row + self.win.nrow)]
        for i, line in enumerate(visible):
            self.scr.addstr(i, 0, line[:self.win.ncol])
        self.scr.move(*self.win.translate(self.cur))
    # [/display]

    def quit(self):
        self.running = False

    def left(self):
        if self.cur.col > 0:
            self.cur.col -= 1
        self.win.up(self.cur)

    def right(self):
        line_len = len(self.contents[self.cur.row])
        if self.cur.col < min(self.win.ncol - 1, line_len - 1):
            self.cur.col += 1
        self.win.down(self.contents, self.cur)

    # [updown]
    def up(self):
        if self.cur.row > 0:
            self.cur.row -= 1
        self.limit_col()
        self.win.up(self.cur)

    def down(self):
        if self.cur.row < len(self.contents) - 1:
            self.cur.row += 1
        self.limit_col()
        self.win.down(self.contents, self.cur)
    # [/updown]

    def limit_col(self):
        self.cur.col = min(self.cur.col, len(self.contents[self.cur.row]) - 1)

def make_contents():
    line = '0123456789'
    result = []
    for i in range(100):
        result.append(f"{i:3}:{line[:i+1]}")
    return result

if __name__ == "__main__":
    editor = Editor()
    contents = make_contents()
    try:
        curses.wrapper(editor, contents)
    except Exception as exc:
        print(exc)
