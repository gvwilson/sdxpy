from datetime import datetime
from pathlib import Path

import pytest

from util import record_pack, record_unpack, record_size
from page_memory import DBError, PageMemory
from db_memory import DBMemory
from page_file import PageFile
from db_file import DBFile
from db_swap import DBSwap

DB_DIR = "/db"
TEST_PAGE_SIZE = 2 * record_size() + 1
RECORDS_PER_PAGE = 2
RECORD_A = b"a" * record_size()
RECORD_B = b"b" * record_size()
RECORD_C = b"c" * record_size()

@pytest.fixture
def our_fs(fs):
    fs.create_dir(DB_DIR)
    return fs

def num_page_files():
    return len(list(Path(DB_DIR).iterdir()))

def test_pack_unpack():
    userid = 12345
    username = "ghopper"
    timestamp = int(datetime(2022, 1, 2, 3, 4, 5).timestamp())
    buf = record_pack(userid, username, timestamp)
    result = record_unpack(buf)
    assert result == (userid, username, timestamp)

def test_page():
    page = PageMemory(TEST_PAGE_SIZE)
    assert page.size() == 0

    page.append(RECORD_A)
    assert page.size() == len(RECORD_A)
    assert page.get(0) == RECORD_A

    page.append(RECORD_B)
    assert page.get(1) == RECORD_B

    with pytest.raises(DBError):
        page.append(RECORD_B)

def test_db_memory():
    db = DBMemory(TEST_PAGE_SIZE)
    assert db.size() == 0
    assert db.num_pages() == 1

    test_len = 5
    for i in range(test_len):
        db.append(RECORD_A)
        assert db.size() == (i + 1) * record_size()
        assert db.num_pages() == 1 + (i // RECORDS_PER_PAGE)
        assert db.get(i) == RECORD_A

    with pytest.raises(DBError):
        db.get(test_len + 1)

def do_common_tests(db):
    assert num_page_files() == 0

    db.append(RECORD_A)
    assert db.size() == record_size()
    assert db.num_pages() == 1
    assert db.get(0) == RECORD_A

    db.append(RECORD_B)
    assert num_page_files() == 0
    db.append(RECORD_C)
    assert num_page_files() == 1
    assert db.size() == 3 * record_size()

    assert db.get(0) == RECORD_A
    assert db.get(1) == RECORD_B
    assert db.get(2) == RECORD_C

def test_db_file(our_fs):
    db = DBFile(DB_DIR, TEST_PAGE_SIZE)
    do_common_tests(db)

def test_db_swap_no_swapping(our_fs):
    db = DBSwap(DB_DIR, 1000, TEST_PAGE_SIZE)
    do_common_tests(db)

def test_db_swap_with_swapping(our_fs):
    db = DBSwap(DB_DIR, 2, TEST_PAGE_SIZE)
    test_len = 10
    record = RECORD_A
    for i in range(test_len):
        db.append(record)
        record = RECORD_B
        assert db.num_pages() == 1 + (i // RECORDS_PER_PAGE)
        assert len(db.in_memory()) <= TEST_PAGE_SIZE
        assert db.get(0) == RECORD_A
    db.flush()
    assert num_page_files() == (test_len + 1) // RECORDS_PER_PAGE
