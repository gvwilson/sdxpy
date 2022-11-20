import ast
import sys

from collections import Counter

action = sys.argv[1]

call = open("call.py", "r").read()

# [parse]
call_code = ast.parse(call)
# [/parse]
if action == "parse":
    print(ast.dump(call_code, indent=2))

# [make]
def make_count(name):
    return ast.Expr(
        value = ast.Call(
            func=ast.Name(id="count", ctx=ast.Load()),
            args=[ast.Constant(value=name)],
            keywords=[]
        )
    )
constructed = make_count("test")
# [/make]

if action == "make":
    print(ast.dump(constructed, indent=2))

# [modify]
def modify(text):
    code = ast.parse(text)
    for node in ast.walk(code):
        if isinstance(node, ast.FunctionDef):
            node.body = [make_count(node.name), *node.body]
    return ast.unparse(code)
# [/modify]

original = open("add_double.py", "r").read()
modified = modify(original)
if action == "modified":
    print(modified)

# [counter]
class CountCalls:
    def __init__(self):
        self.count = Counter()

    def __call__(self, name):
        self.count[name] += 1
# [/counter]

if action != "exec":
    sys.exit(0)

# [exec]
call_counter = CountCalls()
bytecode = compile(modified, filename="example", mode="exec")
exec(bytecode, {"count": call_counter})
print(call_counter.count)
# [/exec]
