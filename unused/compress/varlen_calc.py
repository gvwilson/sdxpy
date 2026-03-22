from collections import Counter
import re
import struct
import sys


NYBBLE_RANGE = 2 ** 7
BITS_PER_NYBBLE = 4


def calc_compress(text):
    """Calculate compression of text."""
    tokens = [t for t in re.split(r'\b', text) if len(t) > 0]
    counts = Counter(tokens)
    len_token_table = sum(len(bytes(t, 'utf-8')) for t in counts.keys()) + len(counts) - 1
    return len_token_table + count_packed(counts)


def count_packed(counts):
    """Calculate space required for nybble representation."""
    used_per_nybble = NYBBLE_RANGE
    remaining = len(counts)
    result = 0
    i = 1
    while remaining:
        chunk = used_per_nybble ** i
        if remaining < chunk:
            result += remaining * i
            remaining = 0
        else:
            result += chunk * i
            remaining -= chunk
        i += 1
    if result % 2 == 1:
        result += 1
    return (result * BITS_PER_NYBBLE) // 2


if __name__ == "__main__":
    original = sys.stdin.read()
    print(f"original: {len(bytes(original, 'utf-8'))}")
    print(f"compressed: {calc_compress(original)}")
