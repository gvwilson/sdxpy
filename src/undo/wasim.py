import argparse
import curses
import sys

class Window:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols

class Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self._clamp_col(buffer)

    def down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self._clamp_col(buffer)

    def left(self, buffer):
        if self.col > 0:
            self.col -= 1

    def right(self, buffer):
        if self.col < len(buffer[self.row]) - 1:
            self.col += 1

    def _clamp_col(self, buffer):
        old = self.col
        self.col = max(0, min(self.col, len(buffer[self.row])-1))

    def __str__(self):
        return f"r{self.row}c{self.col}"


def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = [s.rstrip("\n") for s in f.readlines()]

    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()

    while True:
        stdscr.erase()
        for row, line in enumerate(buffer[:window.n_rows]):
            stdscr.addstr(row, 0, line[:window.n_cols])
        stdscr.move(cursor.row, cursor.col)

        k = stdscr.getkey()
        if k == "KEY_UP":
            cursor.up(buffer)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
        elif k == "KEY_LEFT":
            cursor.left(buffer)
        elif k == "KEY_RIGHT":
            cursor.right(buffer)
        elif k == "q":
            sys.exit(0)
        stdscr.move(cursor.row, cursor.col)

if __name__ == "__main__":
    curses.wrapper(main)
