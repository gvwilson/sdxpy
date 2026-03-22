import math

def square_perimeter(thing):
    return 4 * thing["side"]

def square_area(thing):
    return thing["side"] ** 2

# mccole:square
def square_larger(thing, size):
    return call(thing, "area") > size

Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "larger": square_larger,
    "_classname": "Square"
}
# mccole:/square

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

# mccole:circle
def circle_larger(thing, size):
    return call(thing, "area") > size
# mccole:/circle

Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "larger": circle_larger,
    "_classname": "Circle"
}

def circle_new(name, radius):
    return {
        "name": name,
        "radius": radius,
        "_class": Circle
    }

# mccole:call
def call(thing, method_name, *args):
    return thing["_class"][method_name](thing, *args)
# mccole:/call

# mccole:example
examples = [square_new("sq", 3), circle_new("ci", 2)]
for ex in examples:
    result = call(ex, "larger", 10)
    print(f"is {ex['name']} larger? {result}")
# mccole:/example
