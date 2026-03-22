from headless import HeadlessScreen
from history import HistoryApp

LINES = ["ab", "cd"]

def make_fixture(keys, size=(2, 2), lines=LINES):
    screen = HeadlessScreen(size, keys)
    app = HistoryApp(size, lines)
    app(screen)
    return app

def get_screen(app):
    return app.get_log()[-1][-1]

def test_empty_history():
    app = make_fixture(["KEY_DOWN"])
    assert app.get_history() == []
    assert get_screen(app) == LINES

def test_history_after_insert():
    app = make_fixture(["z"])
    assert app.get_history() == [("insert", (0, 0), "z")]
    assert get_screen(app) == ["za", "cd"]

def test_history_after_delete():
    app = make_fixture(["KEY_RIGHT", "DELETE"])
    assert app.get_history() == [("delete", (0, 1), "b")]
    assert get_screen(app) == ["a_", "cd"]
