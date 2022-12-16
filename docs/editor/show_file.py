import curses
import sys

# [main]
def main(scr, buffer):
    scr.erase()
    for i, line in enumerate(buffer):
        scr.addstr(i, 0, line)

    while True:
        key = scr.getkey()
        if key in "Qq":
            break
# [/main]

# [launch]
if __name__ == "__main__":
    buffer = []
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as reader:
            buffer = reader.readlines()
    curses.wrapper(main, buffer)
# [/launch]
