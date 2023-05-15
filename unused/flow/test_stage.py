from head import Head
from tail import Tail
from cat import Cat

def test_head():
    head = Head(3)
    assert not head.ready()
    head.notify("input", ["a", "b", "c", "d", "e"])
    assert head.result() == ["a", "b", "c"]

def test_head_tail():
    head = Head(3)
    tail = Tail(2)
    head.tell(tail, "input")

    assert not head.ready()
    assert not tail.ready()
    head.notify("input", ["a", "b", "c", "d", "e"])

    assert head.result() == ["a", "b", "c"]
    assert tail.result() == ["b", "c"]

def test_head_tail_tail_join():
    head = Head(3)

    left = Tail(2)
    right = Tail(1)
    head.tell(left, "input")
    head.tell(right, "input")

    cat = Cat()
    left.tell(cat, "second")
    right.tell(cat, "first")

    head.notify("input", ["a", "b", "c", "d", "e"])
    assert head.result() == ["a", "b", "c"]
    assert left.result() == ["b", "c"]
    assert right.result() == ["c"]
    assert cat.result() == ["c", "b", "c"]
