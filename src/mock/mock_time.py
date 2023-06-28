import time

def elapsed(since):
    return time.time() - since

def mock_time():
    return 200

def test_elapsed():
    time.time = mock_time
    assert elapsed(50) == 150
