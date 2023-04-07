from curses import wrapper

LINES = ["this", "is", "a", "test"]

def main(stdscr):
    stdscr.clear()
    for (i, line) in enumerate(LINES):
        stdscr.addstr(i, 0, line)
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
