from datetime import datetime
from pathlib import Path
from glob import glob
from unittest.mock import patch
import pytest

from cache_limited import CacheLimited
from index_csv import IndexCSV

CACHE_DIR = Path("/cache")
PERMANENT_DIR = Path("/permanent")
LOCAL_LIMIT = 2

@pytest.fixture
def disk(fs):
    fs.create_dir(CACHE_DIR)
    fs.create_dir(PERMANENT_DIR)
    return fs

@pytest.fixture
def cache(disk):
    index = IndexCSV(PERMANENT_DIR)
    return CacheLimited(index, CACHE_DIR, PERMANENT_DIR, LOCAL_LIMIT)

def test_limited_no_files_before_add(cache):
    assert cache.known() == set()

def test_limited_single_file_present_after_add(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    ident = cache.add("test.txt")
    assert cache.has(ident)
    assert cache.known() == {ident}
    cache_path = cache.get_cache_path(ident)
    assert str(cache_path.parent) == str(CACHE_DIR)
    permanent_path = cache._make_permanent_path(ident)
    assert Path(permanent_path).exists()

def test_limited_two_files_present_after_add(disk, cache):
    names = "ab"
    assert len(names) <= LOCAL_LIMIT
    for name in names:
        filename = f"{name}.txt"
        disk.create_file(filename, contents=name)
        cache.add(filename)
    assert len(cache.known()) == 2

def test_limited_single_file_can_be_reloaded(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    ident = cache.add("test.txt")
    with open(cache.get_cache_path(ident), "r") as reader:
        assert reader.read() == "xyz"

def test_limited_file_can_be_reloaded_after_deletion(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    ident = cache.add("test.txt")
    Path("test.txt").unlink()
    with open(cache.get_cache_path(ident), "r") as reader:
        assert reader.read() == "xyz"
    assert len(cache.known()) == 1

def test_limited_duplicate_content_only_saved_once(disk, cache):
    contents = "xyz"
    disk.create_file("first.txt", contents=contents)
    ident_first = cache.add("first.txt")
    disk.create_file("second.txt", contents=contents)
    ident_second = cache.add("second.txt")
    assert ident_first == ident_second
    assert len(cache.known()) == 1

def test_limited_local_cache_size_stays_small(disk, cache):
    names = "abcdefg"
    assert len(names) > LOCAL_LIMIT
    for name in names:
        local_file = f"{name}.txt"
        disk.create_file(local_file, contents=name)
        cache.add(local_file)
    assert len(cache.known()) == len(names)
    assert len(list(Path(CACHE_DIR).iterdir())) == LOCAL_LIMIT
    assert len(list(Path(PERMANENT_DIR).iterdir())) == len(names) + 1

def test_limited_all_files_can_be_retrieved(disk, cache):
    names = "abcdefg"
    assert len(names) > LOCAL_LIMIT
    idents = {}

    for name in names:
        local_file = f"{name}.txt"
        disk.create_file(local_file, contents=name)
        idents[local_file] = cache.add(local_file)

    for (name, ident) in idents.items():
        assert len(list(Path(CACHE_DIR).iterdir())) == LOCAL_LIMIT
        local_file = f"{name}.txt"
        cache_path = cache.get_cache_path(ident)
        assert cache_path.exists()
