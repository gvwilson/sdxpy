from datetime import datetime
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from cache_filesystem import CacheFilesystem
from index_base import CacheEntry
from index_csv import IndexCSV


REMOTE_DIR = Path("/cache")
LOCAL_DIR = Path(".")
INDEX_FILE = Path(LOCAL_DIR, IndexCSV.INDEX_FILE)


@pytest.fixture
def structure(fs):
    fs.create_dir(REMOTE_DIR)
    fs.create_file(INDEX_FILE)


def test_index_loads_initially(structure):
    index = IndexCSV(LOCAL_DIR)
    assert index.load() == []


def test_index_saves_changes(structure):
    right_now = datetime(2022, 12, 12)
    index = IndexCSV(LOCAL_DIR)
    with patch("index_base.current_time", return_value=right_now):
        index.add("abcd1234")
    assert index.load() == [CacheEntry("abcd1234", right_now)]


def test_index_has_entry(structure):
    right_now = datetime(2022, 12, 12)
    index = IndexCSV(LOCAL_DIR)
    with patch("index_base.current_time", return_value=right_now):
        index.add("abcd1234")
    assert index.has("abcd1234")
    assert not index.has("dcba4321")


def test_index_lru(structure):
    identifiers = ["c3", "b2", "a1"]
    timestamps = [
        datetime(2022, 12, 12),
        datetime(2022, 11, 11),
        datetime(2022, 10, 10)
    ]
    index = IndexCSV(LOCAL_DIR)
    with patch("index_base.current_time", side_effect=timestamps):
        for i in identifiers:
            index.add(i)
    expected = [CacheEntry(i, t) for (i, t) in zip(identifiers, timestamps)]
    expected = [r for r in reversed(expected)]
    assert index.least_recently_used() == expected
