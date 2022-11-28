from datetime import datetime
from pathlib import Path
from unittest.mock import patch
import pytest

from cache_filesystem import CacheFilesystem
from index_csv import IndexCSV

# [setup]
CACHE_DIR = Path("/cache")

@pytest.fixture
def disk(fs):
    fs.create_dir(CACHE_DIR)
    return fs

@pytest.fixture
def cache():
    return CacheFilesystem(IndexCSV(CACHE_DIR), CACHE_DIR)
# [/setup]

# [empty]
def test_filesystem_no_files_before_add(disk, cache):
    assert cache.known() == set()
# [/empty]

def test_filesystem_single_file_present_after_add(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    ident = cache.add("test.txt")
    assert cache.has(ident)
    assert cache.known() == {ident}
    cache_path = cache.get_cache_path(ident)
    assert str(cache_path.parent) == str(CACHE_DIR)

# [two]
def test_filesystem_two_files_present_after_add(disk, cache):
    names = "ab"
    for name in names:
        filename = f"{name}.txt"
        disk.create_file(filename, contents=name)
        cache.add(filename)
    assert len(cache.known()) == 2
# [/two]

def test_filesystem_single_file_can_be_reloaded(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    ident = cache.add("test.txt")
    with open(cache.get_cache_path(ident), "r") as reader:
        assert reader.read() == "xyz"

def test_filesystem_file_can_be_reloaded_after_deletion(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    ident = cache.add("test.txt")
    Path("test.txt").unlink()
    with open(cache.get_cache_path(ident), "r") as reader:
        assert reader.read() == "xyz"
    assert len(cache.known()) == 1

def test_filesystem_duplicate_content_only_saved_once(disk, cache):
    contents = "xyz"
    disk.create_file("first.txt", contents=contents)
    ident_first = cache.add("first.txt")
    disk.create_file("second.txt", contents=contents)
    ident_second = cache.add("second.txt")
    assert ident_first == ident_second
    assert len(cache.known()) == 1
