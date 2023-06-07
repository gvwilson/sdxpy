from model_original import Model
from controller_original import Controller
from view_original import View
from recorder import Recorder


def build(lines, height):
    model = Model(lines)
    recorder = Recorder()
    view = View(height, recorder)
    controller = Controller(model, view)
    return model, view, controller, recorder


def expected(lines):
    return list(enumerate(lines))


def test_3_lines_3_screen():
    lines = ["a", "b", "c"]
    model, view, controller, recorder = build(lines, 3)
    controller.display()
    assert recorder.get() == expected(lines)


def test_3_lines_4_screen():
    lines = ["a", "b", "c"]
    model, view, controller, recorder = build(lines, 4)
    controller.display()
    assert recorder.get() == expected(lines + [""])


def test_4_lines_3_screen():
    lines = ["a", "b", "c", "d"]
    model, view, controller, recorder = build(lines, 3)
    controller.display()
    assert recorder.get() == expected(lines[:3])


def test_4_lines_3_screen_down():
    lines = ["a", "b", "c", "d"]
    model, view, controller, recorder = build(lines, 3)
    controller.down()
    assert recorder.get() == expected(lines[1:])


def test_4_lines_3_screen_down_up():
    lines = ["a", "b", "c", "d"]
    model, view, controller, recorder = build(lines, 3)
    controller.down()
    recorder.clear()
    controller.up()
    assert recorder.get() == expected(lines[:3])

def test_cannot_go_above_first_line():
    lines = ["a", "b", "c", "d"]
    model, view, controller, recorder = build(lines, 3)
    assert model.y() == 0
    controller.up()
    assert model.y() == 0

def test_cannot_go_below_last_line():
    lines = ["a", "b", "c", "d"]
    model, view, controller, recorder = build(lines, 3)
    model.y(3)
    assert model.y() == 3
    controller.down()
    assert model.y() == 3

def test_moving_changes_display():
    lines = ["a", "b", "c", "d"]
    model, view, controller, recorder = build(lines, 3)
    controller.display()
    assert recorder.get() == expected(lines[:3])
    recorder.clear()
    controller.down()
    assert recorder.get() == expected(lines[1:])
