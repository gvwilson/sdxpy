import csv
import sys
import time

from df_col import DfCol
from df_row import DfRow

# [create]
RANGE = 10

def make_col(nrow, ncol):
    def _col(n, start):
        return [((start + i) % RANGE) for i in range(n)]
    fill = {f"label_{c}": _col(nrow, c) for c in range(ncol)}
    return DfCol(**fill)

def make_row(nrow, ncol):
    labels = [f"label_{c}" for c in range(ncol)]
    def _row(r):
        return {
            c: ((r + i) % RANGE) for (i, c) in enumerate(labels)
        }
    fill = [_row(r) for r in range(nrow)]
    return DfRow(fill)
# [/create]

# [filter]
FILTER = 2

def time_filter(df):
    def f(label_0, **args):
        return label_0 % FILTER == 1

    start = time.time()
    df.filter(f)
    return time.time() - start
# [/filter]

# [select]
SELECT = 3

def time_select(df):
    indices = [i for i in range(df.ncol()) if ((i % SELECT) == 0)]
    labels = [f"label_{i}" for i in indices]
    start = time.time()
    df.select(*labels)
    return time.time() - start
# [/select]

# [sweep]
def sweep(sizes):
    result = []
    for (nrow, ncol) in sizes:
        df_col = make_col(nrow, ncol)
        df_row = make_row(nrow, ncol)
        times = [
            time_filter(df_col),
            time_select(df_col),
            time_filter(df_row),
            time_select(df_row),
        ]
        result.append([nrow, ncol, *times])
    return result
# [/sweep]


def setup(spec):
    sizes = [s.split("x") for s in spec]
    return [(int(s[0]), int(s[1])) for s in sizes]


def report(result):
    writer = csv.writer(sys.stdout)
    writer.writerow(
        ["nrow", "ncol", "filter_col", "select_col", "filter_row", "select_row"]
    )
    for row in result:
        writer.writerow(row)


if __name__ == "__main__":
    if (len(sys.argv) > 1) and (sys.argv[1] == "--silent"):
        silent = True
        spec = sys.argv[2:]
    else:
        silent = False
        spec = sys.argv[1:]
    sizes = setup(spec)
    result = sweep(sizes)
    if not silent:
        report(result)
