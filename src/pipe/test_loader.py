import inspect
from loader import load

def test_find_example_in_named_dir():
    cls = load(["."], "example")
    assert inspect.isclass(cls)
    obj = cls("test")
    assert isinstance(obj, cls)
    assert obj._name == "test"

def test_find_in_single_dir():
    actual = load(["."], "head")
    assert inspect.isclass(actual)
