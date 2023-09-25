import pytest

from record_original import BasicRec as BasicExperiment
from just_dict_original import JustDict

# [fixture]
@pytest.fixture
def db():
    return JustDict(BasicExperiment.key)

@pytest.fixture
def ex01():
    return BasicExperiment("ex01", 12345, [1, 2])

@pytest.fixture
def ex02():
    return BasicExperiment("ex02", 67890, [3, 4])
# [/fixture]

# [test]
def test_construct(db):
    assert db

def test_get_nothing_from_empty_db(db):
    assert db.get("something") is None

def test_add_then_get(db, ex01):
    db.add(ex01)
    assert db.get("ex01") == ex01

def test_add_two_then_get_both(db, ex01, ex02):
    db.add(ex01)
    db.add(ex02)
    assert db.get("ex01") == ex01
    assert db.get("ex02") == ex02

def test_add_then_overwrite(db, ex01):
    db.add(ex01)
    ex01._timestamp = 67890
    db.add(ex01)
    assert db.get("ex01") == ex01
# [/test]
