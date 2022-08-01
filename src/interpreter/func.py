"""A tiny little language in one file, with function definitions."""

import json
import sys


def do_add(env, args):
    """Add two values.

    ["add" A B] => A + B
    """
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


# [call]
def do_call(env, args):
    """Call a function.

    ["call" name ...expr...] => env[name](*expr)
    """
    # Set up the call.
    assert len(args) >= 1
    name = args[0]
    values = [do(env, a) for a in args[1:]]

    # Find the function.
    func = env_get(env, name)
    assert isinstance(func, list) and (func[0] == "func")
    params, body = func[1], func[2]
    assert len(values) == len(params)

    # Run in new environment.
    env.append(dict(zip(params, values)))
    result = do(env, body)
    env.pop()

    # Report.
    return result
# [/call]


def do_comment(env, args):
    """Ignore instructions.

    ["comment" "text"] => None
    """
    return None


# [def]
def do_def(env, args):
    """Define a new function.

    ["def" name [...params...] body] => None # and define function
    """
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None
# [/def]


def do_get(env, args):
    """Get the value of a variable from the most recent environment
    or the global environment.

    ["get" name] => env{name}
    """
    assert len(args) == 1
    return env_get(env, args[0])


def do_gt(env, args):
    """Strictly greater than.

    ["gt" A B] => A > B
    """
    assert len(args) == 2
    return do(env, args[0]) > do(env, args[1])


def do_if(env, args):
    """Make a choice: only one sub-expression is evaluated.

    ["if" C A B] => A if C else B
    """
    assert len(args) == 3
    cond = do(env, args[0])
    choice = args[1] if cond else args[2]
    return do(env, choice)


def do_leq(env, args):
    """Less than or equal.

    ["leq" A B] => A <= B
    """
    assert len(args) == 2
    return do(env, args[0]) <= do(env, args[1])


def do_neg(env, args):
    """Arithmetic negation.

    ["neq" A] => -A
    """
    assert len(args) == 1
    return -do(env, args[0])


def do_not(env, args):
    """Logical negation.

    ["not" A] => not A
    """
    assert len(args) == 1
    return not do(env, args[0])


def do_or(env, args):
    """Logical or.
    The second sub-expression is only evaluated if the first is false.

    ["or" A B] => A or B
    """
    assert len(args) == 2
    if temp := do(env, args[0]):
        return temp
    return do(env, args[1])


def do_print(env, args):
    """Print values.

    ["print" ...values...] => None # print each value
    """
    args = [do(env, a) for a in args]
    print(*args)
    return None


def do_repeat(env, args):
    """Repeat instructions some number of times.

    ["repeat" N expr] => expr # last one of N
    """
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        result = do(env, args[1])
    return result


def do_seq(env, args):
    """Do a sequence of operations.

    ["seq" A B...] => last expr # execute in order
    """
    for a in args:
        result = do(env, a)
    return result


def do_set(env, args):
    """Assign to a variable.

    ["seq" name expr] => expr # and env{name} = expr
    """
    assert len(args) == 2
    name = args[0]
    value = do(env, args[1])
    env_set(env, name, value)
    return value


# Lookup table of operations.
OPERATIONS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}


def do(env, instruction):
    """Run the given instruction in the given environments."""
    if not isinstance(instruction, list):
        return instruction
    op, args = instruction[0], instruction[1:]
    assert op in OPERATIONS
    return OPERATIONS[op](env, args)


def env_get(env, name):
    """Get a variable's value."""
    assert isinstance(name, str)
    if name in env[-1]:
        return env[-1][name]
    if name in env[0]:
        return env[0][name]
    assert False, f"Unknown variable {name}"


def env_set(env, name, value):
    """Set a variable's value."""
    assert isinstance(name, str)
    if name in env[-1]:
        env[-1][name] = value
    elif name in env[0]:
        name[name] = value
    else:
        env[-1][name] = value


def main():
    assert len(sys.argv) == 2, "Usage: func.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do([{}], program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
