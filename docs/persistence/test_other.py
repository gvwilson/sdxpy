from io import StringIO
from other import SaveOther as Save, LoadOther as Load
from user_classes import Parent, Child

def roundtrip(fixture, extensions, savers, loaders):
    writer = StringIO()
    Save(writer, savers).save(fixture)
    reader = StringIO(writer.getvalue())
    return Load(reader, extensions, loaders).load()

def test_other_no_aliasing():
    fixture = ["a", {"b": True, 7: {"c": "d"}}]
    assert roundtrip(fixture, [], {}, {}) == fixture

def test_other_circular():
    fixture = []
    fixture.append(fixture)
    result = roundtrip(fixture, [], {}, {})
    assert len(result) == 1
    assert id(result) == id(result[0])

def test_other_extension_class():
    fixture = Parent("subject")
    result = roundtrip(fixture, [Parent], {}, {})
    assert isinstance(result, Parent)
    assert result.name == fixture.name

def test_other_derived_class():
    fixture = Child("derived", False)
    result = roundtrip(fixture, [Child], {}, {})
    assert isinstance(result, Child)
    assert result.name == fixture.name
    assert result.check == fixture.check

def save_none(value):
    return {}

def load_none(values):
    assert len(values) == 0
    return None

def test_other_roundtrip_none():
    assert roundtrip(
        None, [],
        {None.__class__: save_none},
        {None.__class__: load_none}
    ) == None
