#!/usr/bin/env python

"""Compare standard input words to known words."""


import sys


def main(wordlist):
    """Main driver."""
    actual = {x.strip() for x in sys.stdin.readlines()}
    with open(wordlist, "r") as reader:
        expected = {x.strip() for x in reader.readlines()}
    report("unknown", actual - expected)
    report("unused", expected - actual)


def report(title, words):
    """Report a set of words."""
    if not words:
        return
    print(f"# {title}")
    for w in sorted(words):
        print(w)


if __name__ == "__main__":
    main(sys.argv[1])
