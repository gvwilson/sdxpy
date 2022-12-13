import curses
import sys

def main(scr, logfile):
    while True:
        key = scr.getkey()
        print(repr(key), file=logfile)
        if key in "Qq":
            break

if __name__ == "__main__":
    assert len(sys.argv) == 2
    with open(sys.argv[1], "w") as writer:
        curses.wrapper(main, writer)
