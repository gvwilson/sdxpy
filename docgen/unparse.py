import ast
import sys

action = sys.argv[1]

with open("double_and_print.py", "r") as reader:
    original = reader.read()

if action == "original":
    print(original)

# mccole:modify
code = ast.parse(original)
print_stmt = code.body[1]
code.body.append(print_stmt)
modified = ast.unparse(code)
# mccole:/modify
if action == "modified":
    print(modified)

if action != "exec":
    sys.exit(0)
# mccole:exec
bytecode = compile(code, filename="example", mode="exec")
exec(bytecode)
# mccole:/exec
