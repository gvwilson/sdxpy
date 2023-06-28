import sys
from string import ascii_lowercase

ROW = 0
COL = 1

def make_lines(num_lines):
    result = []
    for i in range(num_lines):
        ch = ascii_lowercase[i % len(ascii_lowercase)]
        result.append(ch + "".join(str(j % 10) for j in range(i)))
    return result

def setup():
    num_lines = int(sys.argv[1])
    size = None
    if len(sys.argv) > 2:
        size = (int(sys.argv[2]), int(sys.argv[3]))
    lines = make_lines(num_lines)
    return size, lines
