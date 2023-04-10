import argparse
import curses
import sys

class Window:
    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self):
        return self.row + self.n_rows - 1

    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < len(buffer) - 1:
            self.row += 1

    def translate(self, cursor):
        result = cursor.row - self.row, cursor.col - self.col
        return result

    def horizontal_scroll(self, cursor, left_margin=5, right_margin=2):
        n_pages = cursor.col // (self.n_cols - right_margin)
        self.col = max(n_pages * self.n_cols - right_margin - left_margin, 0)

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
        elif self.row > 0:
            self.row -= 1
            self.col = max(0, len(buffer[self.row]) - 1)

    def right(self, buffer):
        if self.col < len(buffer[self.row]) - 1:
            self.col += 1
        elif self.row < len(buffer) - 1:
            self.row += 1
            self.col = 0

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
        for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1:]
            if len(line) > window.n_cols:
                line = line[:window.n_cols - 1] + "»"
            stdscr.addstr(row, 0, line)
        stdscr.move(*window.translate(cursor))

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            cursor.up(buffer)
            window.up(cursor)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
            window.down(buffer, cursor)
        elif k == "KEY_LEFT":
            cursor.left(buffer)
            window.up(cursor)
        elif k == "KEY_RIGHT":
            cursor.right(buffer)
            window.down(buffer, cursor)
        window.horizontal_scroll(cursor)

if __name__ == "__main__":
    curses.wrapper(main)
