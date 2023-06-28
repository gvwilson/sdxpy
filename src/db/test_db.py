from pathlib import Path

import pytest

from records import Experiment
from just_dict_original import JustDict
from just_dict_refactored import JustDictRefactored
from file_backed import FileBacked
from blocked import Blocked
from blocked_file import BlockedFile
from cleanup import Cleanup

TEST_DIR = "/test"

CORE = [
    (JustDict, Experiment.key),
    (JustDictRefactored, Experiment),
    (FileBacked, Experiment, "test.db")
]

BLOCKED = [
    (Blocked, Experiment),
    (BlockedFile, Experiment, TEST_DIR),
    (Cleanup, Experiment, TEST_DIR)
]

@pytest.fixture(params=CORE + BLOCKED)
def db_core(request):
    cls = request.param[0]
    args = request.param[1:]
    return cls(*args)

@pytest.fixture(params=BLOCKED)
def db_block(request):
    cls = request.param[0]
    args = request.param[1:]
    return cls(*args)

@pytest.fixture
def ex01():
    return Experiment("ex01", 12345, [1, 2])

@pytest.fixture
def ex02():
    return Experiment("ex02", 67890, [3, 4])

@pytest.fixture
def filesys(fs):
    Path(TEST_DIR).mkdir()
    return fs

def test_construct(filesys, db_core):
    assert db_core

def test_get_nothing_from_empty_db(filesys, db_core):
    assert db_core.get("something") is None

def test_add_without_get(filesys, db_core, ex01):
    db_core.add(ex01)

def test_add_then_get(filesys, db_core, ex01):
    db_core.add(ex01)
    assert db_core.get("ex01") == ex01

def test_add_two_then_get_both(filesys, db_core, ex01, ex02):
    db_core.add(ex01)
    db_core.add(ex02)
    assert db_core.get("ex01") == ex01
    assert db_core.get("ex02") == ex02

def test_add_then_overwrite(filesys, db_core, ex01):
    db_core.add(ex01)
    ex01._timestamp = 67890
    db_core.add(ex01)
    assert db_core.get("ex01") == ex01

def test_blocked_creates_blocks_multiple_records(filesys, db_block):
    num_recs = 7
    for i in range(num_recs):
        db_block.add(Experiment(f"ex{i}", 1000 + i, []))
    size = Blocked.size()
    assert db_block.num_records() == num_recs
    assert db_block.num_blocks() == (num_recs + (size - 1)) // size

def test_blocked_creates_blocks_duplicate_records(filesys, db_block):
    num_reps = 7
    for i in range(num_reps):
        db_block.add(Experiment("ex", 1000 + i, []))
    assert db_block.num_records() == 1

def test_blocked_restart(filesys):
    first = BlockedFile(Experiment, TEST_DIR)
    num_recs = 3
    for i in range(num_recs):
        ex = Experiment(f"ex{i}", 1000 + i, [1, 2])
        first.add(ex)

    second = BlockedFile(Experiment, TEST_DIR)
    record = second.get(Experiment.key(ex))
    assert record == ex
