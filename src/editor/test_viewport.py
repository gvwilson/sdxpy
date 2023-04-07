from model_original import Model
from viewport_viewport import Viewport


def build(lines, height):
    model = Model(lines)
    viewport = Viewport(model, height)
    return viewport


def test_2_lines_2_screen_init():
    lines = ["a", "b"]
    viewport = build(lines, 2)
    assert viewport.current() == (0, 2)
    assert viewport.lines() == lines
    assert viewport.cursor() == (0, 0)
    

def test_2_lines_3_screen_init():
    lines = ["a", "b"]
    viewport = build(lines, 3)
    assert viewport.current() == (0, 2)
    assert viewport.lines() == lines
    assert viewport.cursor() == (0, 0)
    

def test_3_lines_2_screen_init():
    lines = ["a", "b", "c"]
    viewport = build(lines, 2)
    assert viewport.current() == (0, 2)
    assert viewport.lines() == lines[:2]
    assert viewport.cursor() == (0, 0)
    

def test_3_lines_2_screen_move_down():
    lines = ["a", "b", "c"]
    viewport = build(lines, 2)
    assert viewport.current() == (0, 2)
    assert viewport.lines() == ["a", "b"]

    viewport.down()
    assert viewport.current() == (0, 2)
    assert viewport.lines() == ["a", "b"]
    assert viewport.cursor() == (1, 0)

    viewport.down()
    assert viewport.current() == (1, 3)
    assert viewport.lines() == ["b", "c"]
    assert viewport.cursor() == (1, 0)
    

def test_3_lines_2_screen_move_down_then_up():
    lines = ["a", "b", "c"]
    viewport = build(lines, 2)

    for i in range(2):
        viewport.down()
    assert viewport.current() == (1, 3)
    assert viewport.lines() == ["b", "c"]
    assert viewport.cursor() == (1, 0)

    viewport.up()
    assert viewport.current() == (1, 3)
    assert viewport.lines() == ["b", "c"]
    assert viewport.cursor() == (0, 0)

    viewport.up()
    assert viewport.current() == (0, 2)
    assert viewport.lines() == ["a", "b"]
    assert viewport.cursor() == (0, 0)
