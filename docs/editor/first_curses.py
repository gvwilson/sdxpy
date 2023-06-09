import curses

def main(stdscr):
    while True:
        key = stdscr.getkey()

if __name__ == "__main__":
    curses.wrapper(main)
