"""Difference two lists of words."""

import sys

def main():
    assert len(sys.argv) == 2
    actual = {x.strip() for x in sys.stdin}
    expected = {x.strip() for x in open(sys.argv[1], "r").readlines()}
    diff("unexpected", actual - expected)
    diff("unused", expected - actual)


def diff(title, values):
    if not values:
        return
    print(f"# {title}")
    for word in sorted(values, key=lambda x: x.lower()):
        print(word)


if __name__ == "__main__":
    main()
