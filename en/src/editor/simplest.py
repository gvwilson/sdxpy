import curses

def main(scr):
    while True:
        key = scr.getkey()
        if key in "Qq":
            break

if __name__ == "__main__":
    curses.wrapper(main)
