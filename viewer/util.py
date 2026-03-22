import sys

# mccole:log
LOG = None

def open_log(filename):
    global LOG
    LOG = open(filename, "w")

def log(*args):
    print(*args, file=LOG)
# mccole:/log

# mccole:coord
ROW = 0
COL = 1
# mccole:/coord

# mccole:lines
from string import ascii_lowercase

def make_lines(num_lines):
    result = []
    for i in range(num_lines):
        ch = ascii_lowercase[i % len(ascii_lowercase)]
        result.append(ch + "".join(str(j % 10) for j in range(i)))
    return result
# mccole:/lines

# mccole:start
def start():
    num_lines, logfile = int(sys.argv[1]), sys.argv[2]
    size = None
    if len(sys.argv) > 3:
        size = (int(sys.argv[3]), int(sys.argv[4]))
    lines = make_lines(num_lines)
    open_log(logfile)
    return size, lines
# mccole:/start
