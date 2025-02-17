import math

def square_perimeter(thing):
    return 4 * thing["side"]

def square_area(thing):
    return thing["side"] ** 2

# [square]
def square_larger(thing, size):
    return call(thing, "area") > size

Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "larger": square_larger,
    "_classname": "Square"
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

# [circle]
def circle_larger(thing, size):
    return call(thing, "area") > size
# [/circle]

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

# [call]
def call(thing, method_name, *args):
    return thing["_class"][method_name](thing, *args)
# [/call]

# [example]
examples = [square_new("sq", 2), circle_new("ci", 3)]
for ex in examples:
    result = call(ex, "larger", 10)
    print(f"is {ex['name']} larger? {result}")
# [/example]
