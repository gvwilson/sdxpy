from pathlib import Path
import pytest

from hash_all import hash_all

@pytest.fixture
def our_fs(fs):
    fs.create_file("a.txt", contents="aaa")
    fs.create_file("b.txt", contents="bbb")
    fs.create_file("subdir/c.txt", contents="ccc")

def test_hashing(our_fs):
    result = hash_all(".")
    assert {r[0] for r in result} == {"a.txt", "b.txt", "subdir/c.txt"}
    assert all(len(r[1]) == 64 for r in result)

# [change]
def test_change(our_fs):
    original = hash_all(".")
    original = [entry for entry in original if entry[0] == "a.txt"][0]
    with open("a.txt", "w") as writer:
        writer.write("this is new content for a.txt")
    changed = hash_all(".")
    changed = [entry for entry in changed if entry[0] == "a.txt"][0]
    assert original != changed
# [/change]
