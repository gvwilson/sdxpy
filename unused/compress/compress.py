import json
import re
import sys


def compress(text):
    """Compress text."""
    tokens = [t for t in re.split(r'\b', text) if len(t) > 0]
    forward, backward = make_lookup_tables(tokens)
    data = ".".join(f"{forward[t]}" for t in tokens)
    backward = json.dumps(backward)
    return f"{backward}\n{data}"


def make_lookup_tables(tokens):
    """Create forward and backward tables."""
    forward = {}
    backward = {}
    number = 0
    for t in tokens:
        if (len(t) == 0) or (t in forward):
            continue
        forward[t] = number
        backward[number] = t
        number += 1
    return forward, backward


def decompress(packed):
    """Decompress packed representation."""
    lookup, data = packed.split("\n")
    lookup = {int(k):v for k, v in json.loads(lookup).items()}
    data = [lookup[int(t)] for t in data.split(".") if len(t) > 0]
    return "".join(data)


if __name__ == "__main__":
    if sys.argv[1] == "c":
        print(compress(sys.stdin.read()))
    elif sys.argv[1] == "d":
        print(decompress(sys.stdin.read()))
