import inspect
from loader import load

def test_find_example_in_named_dir():
    loaded = load(["verbs"])
    assert "Example" in loaded
    cls = loaded["Example"]
    assert inspect.isclass(cls)
    obj = cls("test")
    assert isinstance(obj, cls)
    assert obj._name == "test"
