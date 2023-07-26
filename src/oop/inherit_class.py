import math

# [shape]
def shape_density(thing, weight):
    return weight / call(thing, "area")

Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None
}
# [/shape]

def shape_new(name):
    return {
        "name": name,
        "_class": Shape
    }

def square_perimeter(thing):
    return 4 * thing["side"]

def square_area(thing):
    return thing["side"] ** 2

# [square]
Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square",
    "_parent": Shape
}
# [/square]

def square_new(name, side):
    return {
        "name": name,
        "side": side,
        "_class": Square
    }

def circle_perimeter(thing):
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    return math.pi * thing["radius"] ** 2

Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_classname": "Circle",
    "_parent": Shape
}

def circle_new(name, radius):
    return {
        "name": name,
        "radius": radius,
        "_class": Circle
    }

# [search]
def call(thing, method_name, *args):
    method = find(thing["_class"], method_name)
    return method(thing, *args)

def find(cls, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError("method_name")
# [/search]

# [use]
examples = [square_new("sq", 3), circle_new("ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")
# [/use]
