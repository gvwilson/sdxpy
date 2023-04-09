import inspect
from loader import load

def test_find_example_in_named_dir():
    cls = load(["first"], "example")
    assert inspect.isclass(cls)
    obj = cls("test")
    assert isinstance(obj, cls)
    assert obj._name == "test"

def test_find_in_single_dir():
    actual = load(["first"], "head")
    assert inspect.isclass(actual)
