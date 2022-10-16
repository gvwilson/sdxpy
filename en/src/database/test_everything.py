from datetime import datetime
import os

import pytest

from util import record_pack, record_unpack, record_size
from page_memory import DBError, PageMemory
from db_memory import DBMemory
from page_file import PageFile
from db_file import DBFile
from db_swap import DBSwap

DB_DIR = "/db"

@pytest.fixture
def our_fs(fs):
    fs.create_dir(DB_DIR)
    return fs

def test_pack_unpack():
    userid = 12345
    username = "ghopper"
    timestamp = int(datetime(2022, 1, 2, 3, 4, 5).timestamp())
    buf = record_pack(userid, username, timestamp)
    result = record_unpack(buf)
    assert result == (userid, username, timestamp)

def test_page():
    page_size = 2 * record_size() + 1

    page = PageMemory(page_size)
    assert page.size() == 0

    first = b"a" * record_size()
    page.append(first)
    assert page.size() == len(first)
    assert page.get(0) == first

    second = b"b" * record_size()
    page.append(second)
    assert page.size() == 2 * record_size()
    assert page.get(1) == second

    with pytest.raises(DBError):
        page.append(second)

def test_db_memory():
    page_size = 2 * record_size() + 1

    db = DBMemory(page_size)
    assert db.size() == 0
    assert db.num_pages() == 1

    record = b"x" * record_size()
    for i in range(5):
        db.append(record)
        assert db.size() == (i + 1) * record_size()
        assert db.num_pages() == 1 + (i // 2)
        assert db.get(i) == record

    with pytest.raises(DBError):
        db.get(6)

def do_common_tests(db):
    assert len(os.listdir(DB_DIR)) == 0

    record = b"a" * record_size()
    db.append(record)
    assert db.size() == record_size()
    assert db.num_pages() == 1
    assert db.get(0) == record

    db.append(b"b" * record_size())
    assert len(os.listdir(DB_DIR)) == 0
    db.append(b"c" * record_size())
    assert len(os.listdir(DB_DIR)) == 1

    assert db.get(0) == record
    assert db.get(1) == b"b" * record_size()
    assert db.get(2) == b"c" * record_size()

def test_db_file(our_fs):
    page_size = 2 * record_size() + 1
    db = DBFile(DB_DIR, page_size)
    do_common_tests(db)

def test_db_swap_no_swapping(our_fs):
    page_size = 2 * record_size() + 1
    db = DBSwap(DB_DIR, 1000, page_size)
    do_common_tests(db)
