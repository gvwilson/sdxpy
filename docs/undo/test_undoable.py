from headless import HeadlessScreen
from undoable import UndoableApp

LINES = ["ab", "cd"]

def make_fixture(keys, size=(2, 2), lines=LINES):
    screen = HeadlessScreen(size, keys)
    app = UndoableApp(size, lines)
    app(screen)
    return app

def get_screen(app):
    return app.get_log()[-1][-1]

def test_insert_undo():
    app = make_fixture(["z", "UNDO"])
    assert get_screen(app) == ["ab", "cd"]
