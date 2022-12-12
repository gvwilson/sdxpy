import curses
import sys

def main(scr, contents):
    scr.erase()
    for i, line in enumerate(contents):
        scr.addstr(i, 0, line)

    while True:
        key = scr.getkey()
        if key in "Qq":
            break

# [launch]
if __name__ == "__main__":
    contents = ['0123456789' * 100] * 1000
    try:
        curses.wrapper(main, contents)
    except Exception as exc:
        print(exc)
# [/launch]
