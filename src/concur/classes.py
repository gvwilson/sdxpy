import greenlet


class Task(greenlet.greenlet):
    def __init__(self, name):
        self._name = name
        self._other = None

    def set_other(self, other):
        self._other = other

    def run(self):
        print(f"=> {self._name}")
        self._other.switch()
        print(f"=> {self._name}")
        return "finished"


first = Task("first")
second = Task("second")
first.set_other(second)
second.set_other(first)
first.switch()
