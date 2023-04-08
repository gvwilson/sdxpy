from loader import load

def test_head():
    Head = load(["first"], "head")
    head = Head(3)
    assert not head.ready()
    head.notify("input", ["a", "b", "c", "d", "e"])
    assert head.result() == ["a", "b", "c"]

def test_head_tail():
    Head = load(["first"], "head")
    head = Head(3)
    Tail = load(["first"], "tail")
    tail = Tail(2)
    head.tell(tail, "input")

    assert not head.ready()
    assert not tail.ready()
    head.notify("input", ["a", "b", "c", "d", "e"])

    assert head.result() == ["a", "b", "c"]
    assert tail.result() == ["b", "c"]

def test_head_tail_tail_join():
    Head = load(["first"], "head")
    head = Head(3)

    Tail = load(["first"], "tail")
    left = Tail(2)
    right = Tail(1)
    head.tell(left, "input")
    head.tell(right, "input")
    
    Cat = load(["first"], "cat")
    cat = Cat()
    left.tell(cat, "second")
    right.tell(cat, "first")

    head.notify("input", ["a", "b", "c", "d", "e"])
    assert head.result() == ["a", "b", "c"]
    assert left.result() == ["b", "c"]
    assert right.result() == ["c"]
    assert cat.result() == ["c", "b", "c"]
