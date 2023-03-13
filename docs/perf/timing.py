import csv
import sys
import time

from df_col import DfCol
from df_row import DfRow

# [create]
SPREAD = 10

def make_col(nrow, ncol):
    def _col(n, start):
        return [((start + i) % SPREAD) for i in range(n)]

    fill = {f"label_{c}": _col(nrow, c) for c in range(ncol)}
    return DfCol(**fill)

def make_row(nrow, ncol):
    labels = [f"label_{c}" for c in range(ncol)]

    def _row(r):
        return {c: ((r + i) % SPREAD) for (i, c) in enumerate(labels)}

    fill = [_row(r) for r in range(nrow)]
    return DfRow(fill)
# [/create]

# [filter]
def time_filter(df):
    def f(label_0, **args):
        return label_0 % 2 == 1

    start = time.time()
    df.filter(f)
    return time.time() - start
# [/filter]

# [select]
def time_select(df):
    indices = [i for i in range(df.ncol()) if ((i % 3) == 0)]
    labels = [f"label_{i}" for i in indices]
    start = time.time()
    df.select(*labels)
    return time.time() - start
# [/select]

# [sweep]
def sweep(sizes):
    sizes = [s.split("x") for s in sizes]
    sizes = [(int(s[0]), int(s[1])) for s in sizes]
    writer = csv.writer(sys.stdout)
    writer.writerow(
        ["nrow", "ncol", "filter_col", "select_col", "filter_row", "select_row"]
    )
    for (nrow, ncol) in sizes:
        df_col = make_col(nrow, ncol)
        df_row = make_row(nrow, ncol)
        times = [
            time_filter(df_col),
            time_select(df_col),
            time_filter(df_row),
            time_select(df_row),
        ]
        times = [f"{t:.2e}" for t in times]
        writer.writerow([nrow, ncol, *times])
# [/sweep]

if __name__ == "__main__":
    sweep(sys.argv[1:])
