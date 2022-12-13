import curses
import sys

# [main]
def main(scr, contents):
    scr.erase()
    for i, line in enumerate(contents):
        scr.addstr(i, 0, line)

    while True:
        key = scr.getkey()
        if key in "Qq":
            break
# [/main]

# [launch]
if __name__ == "__main__":
    contents = []
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as reader:
            contents = reader.readlines()
    curses.wrapper(main, contents)
# [/launch]
