from pathlib import Path

import pytest


@pytest.fixture
def our_fs(fs):
    fs.create_file("a.txt", contents="aaa")
    fs.create_file("b.txt", contents="bbb")
    fs.create_file("subdir/c.txt", contents="ccc")


def test_nested_example(our_fs):
    assert Path("a.txt").exists()
    assert Path("b.txt").exists()
    assert Path("subdir/c.txt").exists()


def test_deletion_example(our_fs):
    assert Path("a.txt").exists()
    Path("a.txt").unlink()
    assert not Path("a.txt").exists()
