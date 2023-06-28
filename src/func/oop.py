def make_object(**kwarg):
    private = kwarg.copy()

    def getter(name):
        return private[name]

    def setter(name, value):
        private[name] = value

    return {"get": getter, "set": setter}

obj = make_object(thing=0)
print("initial value", obj["get"]("thing"))
obj["set"]("thing", 99)
print("obj['thing'] is now", obj["get"]("thing"))
