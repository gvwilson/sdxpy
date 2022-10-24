from datetime import datetime
from pathlib import Path
from unittest.mock import patch
import pytest

from index_base import CacheEntry
from index_csv import IndexCSV

CACHE_DIR = Path("/cache")
INDEX_FILE = Path(CACHE_DIR, IndexCSV.INDEX_FILE)
LOCAL_DIR = Path(".")

@pytest.fixture
def disk(fs):
    fs.create_dir(CACHE_DIR)

def test_csv_loads_initially(disk):
    index = IndexCSV(CACHE_DIR)
    assert index.load() == []
    assert index.known() == set()

def test_csv_saves_changes(disk):
    right_now = datetime(2022, 12, 12)
    index = IndexCSV(CACHE_DIR)
    with patch("index_base.current_time", return_value=right_now):
        index.add("abcd1234")
    assert index.load() == [CacheEntry("abcd1234", right_now)]
    assert index.known() == {"abcd1234"}

def test_csv_has_entry(disk):
    right_now = datetime(2022, 12, 12)
    index = IndexCSV(CACHE_DIR)
    with patch("index_base.current_time", return_value=right_now):
        index.add("abcd1234")
    assert index.has("abcd1234")
    assert not index.has("dcba4321")
