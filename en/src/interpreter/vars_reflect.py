"""A tiny expression evaluator with variables."""

import json
import sys


def do_abs(env, args):
    """Get absolute value of expression."""
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)


def do_add(env, args):
    """Add two expressions."""
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


def do_get(env, args):
    """Get the value of a variable."""
    assert len(args) == 1
    assert isinstance(args[0], str)
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]


def do_seq(env, args):
    """Execute a sequence of operations."""
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result


def do_set(env, args):
    """Set the value of a variable."""
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[args[0]] = value
    return value


# [lookup]
OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}
# [/lookup]


# [do]
def do(env, expr):
    """Evaluate an expression in an environment."""

    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr

    # Lists trigger function calls.
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])


# [/do]


def main():
    assert len(sys.argv) == 2, "Usage: vars_reflect.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do({}, program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
