from binary import compress, decompress

def roundtrip(original):
    assert decompress(compress(original)) == original

def test_empty():
    roundtrip("")

def test_single_character():
    roundtrip("a")

def test_repeated_character():
    roundtrip("aa")

def test_repeated_word():
    roundtrip("abc abc")
