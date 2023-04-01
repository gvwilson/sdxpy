def all_eq(*values):
    return (not values) or all(v == values[0] for v in values)

def dict_match(d, prototype):
    if set(d.keys()) != set(prototype.keys()):
        return False
    return all(type(d[k]) == type(prototype[k]) for k in d)
