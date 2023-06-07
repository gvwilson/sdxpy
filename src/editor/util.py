import string
import sys

ROW = 0
COL = 1

LOG = None

def open_log(filename):
    global LOG
    LOG = open(filename, "w")

def log(*args):
    print(*args, file=LOG)

def make_lines(num_lines):
    result = []
    for i in range(num_lines):
        ch = string.ascii_lowercase[i % len(string.ascii_lowercase)]
        result.append(ch + "".join(str(j % 10) for j in range(i)))
    return result

def setup():
    num_lines, logfile = int(sys.argv[1]), sys.argv[2]
    size = None
    if len(sys.argv) > 3:
        size = (int(sys.argv[3]), int(sys.argv[4]))
    lines = make_lines(num_lines)
    open_log(logfile)
    return size, lines
