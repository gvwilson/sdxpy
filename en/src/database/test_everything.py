from datetime import datetime

import pytest

from convert import record_pack, record_unpack, record_size
from page import DBError, Page
from db_memory import DBMemory

def test_pack_unpack():
    userid = 12345
    username = "ghopper"
    timestamp = int(datetime(2022, 1, 2, 3, 4, 5).timestamp())
    buf = record_pack(userid, username, timestamp)
    result = record_unpack(buf)
    assert result == (userid, username, timestamp)

def test_page():
    page_size = 2 * record_size() + 1

    page = Page(page_size)
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
