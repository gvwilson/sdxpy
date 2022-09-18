"""A tiny expression evaluator with variables."""

import json
import sys


# [do_abs]
def do_abs(env, args):
    """Get absolute value of expression."""
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)


# [/do_abs]


def do_add(env, args):
    """Add two expressions."""
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


# [do_get]
def do_get(env, args):
    """Get the value of a variable."""
    assert len(args) == 1
    assert isinstance(args[0], str)
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]


# [/do_get]


# [do_seq]
def do_seq(env, args):
    """Execute a sequence of operations."""
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result


# [/do_seq]


# [do_set]
def do_set(env, args):
    """Set the value of a variable."""
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[args[0]] = value
    return value


# [/do_set]


# [do]
def do(env, expr):
    """Evaluate an expression in an environment."""

    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr

    # Lists trigger function calls.
    assert isinstance(expr, list)
    if expr[0] == "abs":
        return do_abs(env, expr[1:])
    if expr[0] == "add":
        return do_add(env, expr[1:])
    if expr[0] == "get":
        return do_get(env, expr[1:])
    if expr[0] == "seq":
        return do_seq(env, expr[1:])
    if expr[0] == "set":
        return do_set(env, expr[1:])
    assert False, f"Unknown operation {expr[0]}"


# [/do]


def main():
    assert len(sys.argv) == 2, "Usage: vars.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do({}, program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
