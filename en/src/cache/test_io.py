from pathlib import Path

import pytest

from cache_limited import CacheLimited
from index_csv import IndexCSV
from cache_io import cache_open, cache_save, CACHE_SUFFIX

CACHE_DIR = Path("/cache")
PERMANENT_DIR = Path("/permanent")
LOCAL_LIMIT = 10


@pytest.fixture
def disk(fs):
    fs.create_dir(CACHE_DIR)
    fs.create_dir(PERMANENT_DIR)
    return fs


@pytest.fixture
def cache(disk):
    index = IndexCSV(PERMANENT_DIR)
    return CacheLimited(index, CACHE_DIR, PERMANENT_DIR, LOCAL_LIMIT)


def test_io_cannot_save_nonexistent_file(cache):
    with pytest.raises(FileNotFoundError):
        cache_save(cache, "nonexistent.txt")


def test_io_saving_file_creates_marker(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    cache_save(cache, "test.txt")
    assert Path(f"test.txt.{CACHE_SUFFIX}").exists()


def test_io_cannot_open_with_no_cache_file(cache):
    with pytest.raises(FileNotFoundError):
        cache_open(cache, "nonexistent.txt")


def test_io_can_read_file_from_marker(disk, cache):
    disk.create_file("test.txt", contents="xyz")
    cache_save(cache, "test.txt")
    Path("test.txt").unlink()
    data = cache_open(cache, "test.txt").read()
    assert data == "xyz"
