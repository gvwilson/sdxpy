import inspect

def example(first, second):
    pass

sig = inspect.signature(example)
print("signature:", sig)
print("type:", type(sig))
print("names:", sig.parameters)
print("parameters:", list(sig.parameters.keys()))
