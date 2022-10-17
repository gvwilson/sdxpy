from functions import left, right

def make_table(*functions):
    return {f.__name__: f for f in functions}

table = make_table(left, right)
print(table)
