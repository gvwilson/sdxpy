# mccole:eq
def all_eq(*values):
    return (not values) or all(v == values[0] for v in values)
# mccole:/eq

# mccole:match
def dict_match(d, prototype):
    if set(d.keys()) != set(prototype.keys()):
        return False
    return all(isinstance(d[k], prototype[k]) for k in d)
# mccole:/match
