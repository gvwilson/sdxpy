import pytest
from better_iterator import BetterIterator

def gather(buffer):
    result = ""
    for char in buffer:
        result += char
    return result

def test_naive_buffer():
    buffer = BetterIterator(["ab", "c"])
    assert gather(buffer) == "abc"

def test_naive_buffer_nested_loop():
    buffer = BetterIterator(["a", "b"])
    result = ""
    for outer in buffer:
        for inner in buffer:
            result += inner
    assert result == "abab"
