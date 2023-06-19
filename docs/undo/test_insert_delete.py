from headless import HeadlessScreen
from insert_delete import InsertDeleteApp

def test_insert_upper_left():
    size = (2, 2)
    lines = ["", ""]
    keys = ["Z"]
    screen = HeadlessScreen(size, keys)
    app = InsertDeleteApp(size, lines)
    app(screen)
    assert app.get_log()[-1] == ("CONTROL_X", (0, 0), ["Z_", "__"])

def test_delete_left_edge():
    size = (1, 3)
    lines = ["abc"]
    keys = ["DELETE"]
    screen = HeadlessScreen(size, keys)
    app = InsertDeleteApp(size, lines)
    app(screen)
    assert app.get_log()[-1] == ("CONTROL_X", (0, 0), ["bc_"])

def test_delete_middle():
    size = (1, 3)
    lines = ["abc"]
    keys = ["KEY_RIGHT", "DELETE"]
    screen = HeadlessScreen(size, keys)
    app = InsertDeleteApp(size, lines)
    app(screen)
    assert app.get_log()[-1] == ("CONTROL_X", (0, 1), ["ac_"])

def test_delete_right():
    size = (1, 3)
    lines = ["abc"]
    keys = ["KEY_RIGHT", "KEY_RIGHT", "DELETE"]
    screen = HeadlessScreen(size, keys)
    app = InsertDeleteApp(size, lines)
    app(screen)
    assert app.get_log()[-1] == ("CONTROL_X", (0, 2), ["ab_"])
