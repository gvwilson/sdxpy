import math

# [square]
def square_perimeter(thing):
    return 4 * thing["side"]

def square_area(thing):
    return thing["side"] ** 2

Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square"
}

def square_new(name, side):
    return {
        "name": name,
        "side": side,
        "_class": Square
    }
# [/square]

def circle_perimeter(thing):
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    return math.pi * thing["radius"] ** 2

Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_classname": "Circle"
}

def circle_new(name, radius):
    return {
        "name": name,
        "radius": radius,
        "_class": Circle
    }

# [call]
def call(thing, method_name):
    return thing["_class"][method_name](thing)

examples = [square_new("sq", 2), circle_new("ci", 3)]
for ex in examples:
    n = ex["name"]
    p = call(ex, "perimeter")
    a = call(ex, "area")
    c = ex["_class"]["_classname"]
    print(f"{n} is a {c}: {p:.2f} {a:.2f}")
# [/call]
