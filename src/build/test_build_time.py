from build_time import BuildTime as Builder


def test_empty():
    assert Builder().build({}) == []


def test_single():
    action_A = "build A"
    config = {"A": {"depends": [], "rule": action_A, "time": 0}}
    assert Builder().build(config) == []


def test_circular():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": ["B"], "rule": action_A, "time": 0},
        "B": {"depends": ["A"], "rule": action_B, "time": 0},
    }
    try:
        Builder().build(config)
        assert False, "should have had exception"
    except ValueError:
        pass


def test_no_dep():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": [], "rule": action_A, "time": 0},
        "B": {"depends": [], "rule": action_B, "time": 0},
    }
    assert Builder().build(config) == []


def test_linear_dep_needs_update():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": ["B"], "rule": action_A, "time": 0},
        "B": {"depends": [], "rule": action_B, "time": 1},
    }
    assert Builder().build(config) == [action_A]


def test_linear_dep_no_need_update():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": ["B"], "rule": action_A, "time": 1},
        "B": {"depends": [], "rule": action_B, "time": 0},
    }
    assert Builder().build(config) == []


# [tests]
def test_diamond_dep():
    action_A = "build A"
    action_B = "build B"
    action_C = "build C"
    action_D = "build D"
    config = {
        "A": {"depends": ["B", "C"], "rule": action_A, "time": 0},
        "B": {"depends": ["D"], "rule": action_B, "time": 0},
        "C": {"depends": ["D"], "rule": action_C, "time": 1},
        "D": {"depends": [], "rule": action_D, "time": 1},
    }
    assert Builder().build(config) == [action_B, action_A]
# [/tests]
