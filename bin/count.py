"""Reformat chapter counts."""

import re
import sys


EXCLUDE = {"total"}
FIG_PAT = re.compile(r"(.+):(\d+)")
WC_PAT = re.compile(r"(\d+)\s+(.+)")


def main():
    words, figures = _parse()
    assert set(words.keys()) == set(figures.keys())

    longest = max(len(k) for k in words.keys())
    fmt = f"{{:{longest}}} {{:5}} {{:5}}"

    print(fmt.format("file", "words", "figures"))
    for key in sorted(words.keys()):
        print(fmt.format(key, words[key], figures[key]))

    print(fmt.format("Total", sum(words.values()), sum(figures.values())))


def _parse():
    """Read input."""
    words, figures = {}, {}
    for ln in sys.stdin.readlines():
        ln = ln.strip()
        if (match := WC_PAT.search(ln)):
            if match.group(2) not in EXCLUDE:
                words[match.group(2)] = int(match.group(1))
        elif (match := FIG_PAT.search(ln)):
            figures[match.group(1)] = int(match.group(2))
    return words, figures


if __name__ == "__main__":
    main()
