#!/usr/bin/env python

"""Remove code and math before spell-checking."""


import re
import sys

PATTERNS = [
    re.compile(r"<pre\b.*?>.+?</pre>", re.DOTALL),
    re.compile(r"<code\b.*?>.+?</code>", re.DOTALL),
    re.compile(r"\\\(.+?\\\)", re.DOTALL),
]


def main():
    """Main driver."""
    text = sys.stdin.read()
    for pattern in PATTERNS:
        text = pattern.sub(" ", text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
