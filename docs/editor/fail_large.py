import curses
import sys

def main(scr, buffer):
    scr.erase()
    for i, line in enumerate(buffer):
        scr.addstr(i, 0, line)

    while True:
        key = scr.getkey()
        if key in "Qq":
            break

# [launch]
if __name__ == "__main__":
    buffer = ['0123456789' * 100] * 1000
    try:
        curses.wrapper(main, buffer)
    except Exception as exc:
        print(exc)
# [/launch]
