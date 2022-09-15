import os
from pathlib import Path

import pytest

from cache_filesystem import CacheFilesystem
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
