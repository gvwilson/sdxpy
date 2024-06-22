from collections import Counter
from prettytable import PrettyTable
import re
import sys


def main(text):
    """Calculate token frequency."""
    counts = Counter(t for t in re.split(r'\b', text) if len(t) > 0)
    rows = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
    table = PrettyTable(field_names=('token', 'count'))
    table.align["token"] = "l"
    table.align["count"] = "r"
    table.add_rows(rows)
    return table


if __name__ == "__main__":
    print(main(sys.stdin.read()))
