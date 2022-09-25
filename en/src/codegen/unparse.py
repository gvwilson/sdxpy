import ast

original = """\
def double(x):
    return 2 * x

print(double(3))
"""

print(f"original code\n{original}")

code = ast.parse(original)
print_stmt = code.body[1]
code.body.append(print_stmt)

updated = ast.unparse(code)
print(f"updated code\n{updated}")

bytecode = compile(code, filename="example", mode="exec")
exec(bytecode)
