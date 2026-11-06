from filesystem import FileSystem

# mccole:make
def make_fs():
    fs = FileSystem()
    fs.format()
    return fs
# mccole:/make

# mccole:sample
def test_create_and_read_file():
    fs = make_fs()
    fs.write("/hello.txt", b"Hello, world!")
    assert fs.read("/hello.txt") == b"Hello, world!"
# mccole:/sample


def test_write_overwrites_file():
    fs = make_fs()
    fs.write("/hello.txt", b"first")
    fs.write("/hello.txt", b"second")
    assert fs.read("/hello.txt") == b"second"


def test_listdir_root():
    fs = make_fs()
    fs.write("/a.txt", b"A")
    fs.mkdir("/sub")
    assert sorted(fs.listdir("/")) == ["a.txt", "sub"]


def test_nested_path():
    fs = make_fs()
    fs.mkdir("/docs")
    fs.write("/docs/hello.txt", b"hi")
    assert fs.read("/docs/hello.txt") == b"hi"
    assert sorted(fs.listdir("/docs")) == ["hello.txt"]


def test_read_missing_file():
    fs = make_fs()
    try:
        fs.read("/nope.txt")
        assert False, "expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_remove_file():
    fs = make_fs()
    fs.write("/a.txt", b"A")
    fs.remove("/a.txt")
    assert sorted(fs.listdir("/")) == []


def test_file_larger_than_one_block():
    fs = make_fs()
    fs.write("/big.bin", bytes(range(100)))
    assert fs.read("/big.bin") == bytes(range(100))


def test_name_too_long():
    fs = make_fs()
    try:
        fs.write("/" + "x" * 13 + ".txt", b"hi")
        assert False, "expected ValueError"
    except ValueError:
        pass
