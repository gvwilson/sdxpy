from headless import HeadlessScreen
from insert_delete import InsertDeleteApp

def make_fixture(keys, size, lines):
    screen = HeadlessScreen(size, keys)
    app = InsertDeleteApp(size, lines)
    app(screen)
    return app

def test_insert_upper_left():
    app = make_fixture(["Z"], (2, 2), ["", ""])
    assert app.get_log()[-1] == ("CONTROL_X", (0, 0), ["Z_", "__"])

def test_delete_left_edge():
    app = make_fixture(["DELETE"], (1, 3), ["abc"])
    assert app.get_log()[-1] == ("CONTROL_X", (0, 0), ["bc_"])

def test_delete_middle():
    app = make_fixture(["KEY_RIGHT", "DELETE"], (1, 3), ["abc"])
    assert app.get_log()[-1] == ("CONTROL_X", (0, 1), ["ac_"])

def test_delete_right():
    app = make_fixture(["KEY_RIGHT", "KEY_RIGHT", "DELETE"], (1, 3), ["abc"])
    assert app.get_log()[-1] == ("CONTROL_X", (0, 2), ["ab_"])

def test_delete_empty_line():
    app = make_fixture(["DELETE"], (1, 1), ["a"])
    assert app.get_log()[-1] == ("CONTROL_X", (0, 0), ["_"])

def test_delete_when_impossible():
    try:
        make_fixture(["DELETE"], (1, 1), [""])
    except AssertionError:
        pass
