from compress import compress, decompress

def roundtrip(original, compressed):
    assert compress(original) == compressed
    assert decompress(compressed) == original

def test_empty():
    roundtrip("", '{}\n')

def test_single_character():
    roundtrip("a", '{"0": "a"}\n0')

def test_repeated_character():
    roundtrip("aa", '{"0": "aa"}\n0')

def test_repeated_word():
    roundtrip("abc abc", '{"0": "abc", "1": " "}\n0.1.0')
