from io import StringIO

from extend import LoadExtend as Load
from extend import SaveExtend as Save
from user_classes import Child, Parent


def roundtrip(fixture, *extensions):
    writer = StringIO()
    Save(writer).save(fixture)
    reader = StringIO(writer.getvalue())
    return Load(reader, *extensions).load()


def test_extend_no_aliasing():
    fixture = ["a", {"b": True, 7: {"c": "d"}}]
    assert roundtrip(fixture) == fixture


def test_extend_circular():
    fixture = []
    fixture.append(fixture)
    result = roundtrip(fixture)
    assert len(result) == 1
    assert id(result) == id(result[0])


# [test_parent]
def test_extend_extension_class():
    fixture = Parent("subject")
    writer = StringIO()
    Save(writer).save(fixture)
    reader = StringIO(writer.getvalue())
    result = Load(reader, Parent).load()
    assert isinstance(result, Parent)
    assert result.name == fixture.name
# [/test_parent]


def test_extend_derived_class():
    fixture = Child("derived", False)
    result = roundtrip(fixture, Child)
    assert isinstance(result, Child)
    assert result.name == fixture.name
    assert result.check == fixture.check
