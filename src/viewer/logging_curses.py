import curses
import sys

import util

def main(stdscr):
    while True:
        key = stdscr.getkey()
        util.log(repr(key))
        if key.lower() == "q":
            return

if __name__ == "__main__":
    util.open_log(sys.argv[1])
    curses.wrapper(main)
