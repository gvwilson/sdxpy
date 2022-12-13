import curses
import sys

# [window]
class Window:
    def __init__(self, nrow, ncol):
        assert 0 <= nrow and 0 <= ncol
        self.nrow = nrow
        self.ncol = ncol
# [/window]

# [main]
def main(scr, contents):
    win = Window(curses.LINES - 1, curses.COLS - 1)
    scr.erase()
    for i, line in enumerate(contents[:win.nrow]):
        scr.addstr(i, 0, line[:win.ncol])

    while True:
        key = scr.getkey()
        if key in "Qq":
            break
# [/main]

if __name__ == "__main__":
    contents = ['0123456789' * 100] * 1000
    try:
        curses.wrapper(main, contents)
    except Exception as exc:
        print(exc)
