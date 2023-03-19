from build_better import BuildBetter as Builder


def test_empty():
    assert Builder().build({}) == []


def test_single():
    action_A = "build A"
    config = {"A": {"depends": [], "rule": action_A}}
    assert Builder().build(config) == [action_A]


# [tests]
def test_circular():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": ["B"], "rule": action_A},
        "B": {"depends": ["A"], "rule": action_B},
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
        "A": {"depends": [], "rule": action_A},
        "B": {"depends": [], "rule": action_B},
    }
    assert Builder().build(config) == [action_A, action_B]
# [/tests]


def test_linear_dep():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": ["B"], "rule": action_A},
        "B": {"depends": [], "rule": action_B},
    }
    assert Builder().build(config) == [action_B, action_A]


def test_diamond_dep():
    action_A = "build A"
    action_B = "build B"
    action_C = "build C"
    action_D = "build D"
    config = {
        "A": {"depends": ["B", "C"], "rule": action_A},
        "B": {"depends": ["D"], "rule": action_B},
        "C": {"depends": ["D"], "rule": action_C},
        "D": {"depends": [], "rule": action_D},
    }
    assert Builder().build(config) == [
        action_D,
        action_B,
        action_C,
        action_A,
    ]
