import re
import struct
import sys


def compress(text):
    """Compress text."""
    tokens = [t for t in re.split(r'\b', text) if len(t) > 0]
    forward, backward = make_lookup_tables(tokens)
    forward = [forward[t] for t in tokens]
    backward = bytes("\0".join(backward.values()), "utf-8")
    fmt = f">II{len(backward)}s{len(tokens)}h"
    return struct.pack(fmt, len(backward), len(tokens), backward, *forward)


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
    len_lookup = struct.unpack(">I", packed[0:4])[0]
    len_tokens = struct.unpack(">I", packed[4:8])[0]
    lookup = struct.unpack(f">{len_lookup}s", packed[8:(8+len_lookup)])[0]
    lookup = {i:t for i, t in enumerate(str(lookup, "utf-8").split("\0"))}
    tokens = struct.unpack(f">{len_tokens}h", packed[(8+len_lookup):])
    return "".join(lookup[t] for t in tokens)


if __name__ == "__main__":
    if sys.argv[1] == "c":
        sys.stdout.buffer.write(compress(sys.stdin.read()))
    elif sys.argv[1] == "d":
        print(len(decompress(sys.stdin.read())))
