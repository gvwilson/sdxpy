from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest
from cache_filesystem import CacheFilesystem
from index_csv import IndexCSV

CACHE_DIR = Path("/cache")


@pytest.fixture
def disk(fs):
    fs.create_dir(CACHE_DIR)
    return fs


@pytest.fixture
def cache():
    return CacheFilesystem(IndexCSV(CACHE_DIR))


def test_filesystem_no_files_before_add(disk, cache):
    assert cache.known() == set()


def test_filesystem_single_file_present_after_add(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    ident = cache.add("test.txt")
    assert cache.has(ident)
    assert cache.known() == {ident}
    cache_path = cache.get_cache_path(ident)
    assert str(cache_path.parent) == str(CACHE_DIR)


def test_filesystem_two_files_present_after_add(disk, cache):
    idents = {}
    for prefix in ["a", "b"]:
        contents = prefix * 3
        filename = f"{prefix}.txt"
        disk.create_file(filename, contents=contents)
        idents[prefix] = cache.add(filename)
    assert len(cache.known()) == 2


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
