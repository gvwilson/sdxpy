def make_object(**kwarg):
    private = kwarg.copy()

    def getter(name):
        return private[name]

    def setter(name, value):
        private[name] = value

    return {"get": getter, "set": setter}

obj = make_object(left=1, right=2)
print("obj['left'] is", obj["get"]("left"))
obj["set"]("right", 99)
print("obj['right'] is now", obj["get"]("right"))
