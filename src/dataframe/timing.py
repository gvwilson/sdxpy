import csv
import sys
import time

from df_col import DfCol
from df_row import DfRow


# [create]
SPREAD = 10


def make_col(nrow, ncol):
    """Make a column-oriented dataframe."""
    def _col(n, start):
        return [((start + i) % SPREAD) for i in range(n)]

    fill = {f"label_{c}":_col(nrow, c) for c in range(ncol)}
    return DfCol(**fill)


def make_row(nrow, ncol):
    """Make a row-oriented dataframe."""
    labels = [f"label_{c}" for c in range(ncol)]

    def _row(r):
        return {c:((r + i) % SPREAD) for (i, c) in enumerate(labels)}

    fill = [_row(r) for r in range(nrow)]
    return DfRow(fill)
# [/create]


# [filter]
def time_filter(df):
    """Time filtering operation."""
    def f(label_0, **args):
        return label_0 % 2 == 1

    start = time.time()
    df.filter(f)
    return time.time() - start
# [/filter]


# [select]
def time_select(df):
    """Time selection operation."""
    indices = [i for i in range(df.ncol()) if ((i % 3) == 0)]
    labels = [f"label_{i}" for i in indices]
    start = time.time()
    df.select(*labels)
    return time.time() - start
# [/select]


# [sweep]
def sweep(sizes):
    """Time operations on various sizes of dataframes."""
    sizes = [s.split("x") for s in sizes]
    sizes = [(int(s[0]), int(s[1])) for s in sizes]
    results = [["nrow", "ncol", "filter col", "select col", "filter row", "select row"]]
    for (nrow, ncol) in sizes:
        df_col = make_col(nrow, ncol)
        df_row = make_row(nrow, ncol)
        results.append([
            nrow, ncol,
            time_filter(df_col), time_select(df_col),
            time_filter(df_row), time_select(df_row)
        ])
    csv.writer(sys.stdout).writerows(results)
# [/sweep]


if __name__ == "__main__":
    sweep(sys.argv[1:])
