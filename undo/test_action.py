from headless import HeadlessScreen
from action import ActionApp

LINES = ["ab", "cd"]

def make_fixture(keys, size=(2, 2), lines=LINES):
    screen = HeadlessScreen(size, keys)
    app = ActionApp(size, lines)
    app(screen)
    return app

def get_screen(app):
    return app.get_log()[-1][-1]

def test_no_action():
    app = make_fixture(["KEY_DOWN"])
    assert get_screen(app) == LINES

def test_immediate_insert():
    app = make_fixture(["z"])
    assert get_screen(app) == ["za", "cd"]

def test_move_and_delete():
    app = make_fixture(["KEY_RIGHT", "DELETE"])
    assert get_screen(app) == ["a_", "cd"]
