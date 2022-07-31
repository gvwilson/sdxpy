"""A tiny expression evaluator."""

import json
import sys


# [do_abs]
def do_abs(args):
    """Get absolute value of expression."""
    assert len(args) == 1
    val = do(args[0])
    return abs(val)
# [/do_abs]


# [do_add]
def do_add(args):
    """Add two expressions."""
    assert len(args) == 2
    left = do(args[0])
    right = do(args[1])
    return left + right
# [/do_add]


# [do]
def do(expr):
    """Evaluate an expression."""

    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr

    # Lists trigger function calls.
    assert isinstance(expr, list)
    if expr[0] == "abs":
        return do_abs(expr[1:])
    if expr[0] == "add":
        return do_add(expr[1:])
    assert False, f"Unknown operation {expr[0]}"
# [/do]


# [main]
def main():
    assert len(sys.argv) == 2, "Usage: expr.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do(program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
# [/main]
