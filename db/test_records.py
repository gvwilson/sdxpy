from records import Experiment

def test_construct():
    ex = Experiment("abc", 12345, [1, 2])
    assert ex._name == "abc"
    assert ex._timestamp == 12345
    assert ex._readings == [1, 2]

def test_key():
    ex = Experiment("abc", 12345, [1, 2])
    assert Experiment.key(ex) == "abc"

def test_pack():
    ex = Experiment("abc", 12345, [1, 2])
    p = Experiment.pack(ex)
    assert len(p) == Experiment.RECORD_LEN
    expected = "\0".join(["abc", "12345", "1", "2"])
    assert p.startswith(expected)
    assert all(c == "\0" for c in p[len(expected):])

def test_pack_empty():
    ex = Experiment("abc", 12345, [])
    p = Experiment.pack(ex)
    assert len(p) == Experiment.RECORD_LEN
    expected = "\0".join(["abc", "12345"])
    assert p.startswith(expected)
    assert all(c == "\0" for c in p[len(expected):])

def test_unpack():
    p = "\0".join(str(x) for x in ["abc", 12345, 1, 2])
    p += "\0" * (Experiment.RECORD_LEN - len(p))
    ex = Experiment.unpack(p)
    assert ex == Experiment("abc", 12345, [1, 2])

def test_unpack_empty():
    p = "\0".join(str(x) for x in ["abc", 12345])
    p += "\0" * (Experiment.RECORD_LEN - len(p))
    ex = Experiment.unpack(p)
    assert ex == Experiment("abc", 12345, [])
