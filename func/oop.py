def make_object(initial_value):
    private = {"value": initial_value}

    def getter():
        return private["value"]

    def setter(new_value):
        private["value"] = new_value

    return {"get": getter, "set": setter}

object = make_object(00)
print("initial value", object["get"]())
object["set"](99)
print("object now contains", object["get"]())
