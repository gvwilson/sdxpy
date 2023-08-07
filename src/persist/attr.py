class Example:
    def __init__(self, label):
        self.label = label

    def get_size(self):
        return len(self.label)

ex = Example("thing")
print("ex has missing", hasattr(ex, "missing"))
print("ex has label", hasattr(ex, "label"), "with value", getattr(ex, "label"))
print("ex has get_size", hasattr(ex, "get_size"))
method = getattr(ex, "get_size")
print("result of calling method", method())
