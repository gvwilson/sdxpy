from headless import HeadlessScreen
from history import HistoryApp

def make_fixture(keys, size=(2, 2), lines=["ab", "cd"]):
    screen = HeadlessScreen(size, keys)
    app = HistoryApp(size, lines)
    app(screen)
    return app

def test_empty_history():
    app = make_fixture(["KEY_DOWN"])
    assert app.get_history() == []

def test_history_after_insert():
    app = make_fixture(["z"])
    assert app.get_history() == [("insert", (0, 0), "z")]

def test_history_after_delete():
    app = make_fixture(["KEY_RIGHT", "DELETE"])
    assert app.get_history() == [("delete", (0, 0), "a")]

def test_history_delete_when_impossible():
    app = make_fixture(["DELETE"])
    assert app.get_history() == []
