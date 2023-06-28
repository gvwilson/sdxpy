import curses
import sys

from util import open_log, log, make_lines

# [main]
def main(stdscr, lines):
    while True:
        stdscr.erase()
        for (y, line) in enumerate(lines):
            stdscr.addstr(y, 0, line)
        key = stdscr.getkey()
        if key.lower() == "q":
            return
# [/main]

# [run]
if __name__ == "__main__":
    num_lines, logfile = int(sys.argv[1]), sys.argv[2]
    lines = make_lines(num_lines)
    open_log(logfile)
    curses.wrapper(lambda stdscr: main(stdscr, lines))
# [/run]
