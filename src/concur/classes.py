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


task_a = Task("A")
task_b = Task("B")
task_a.set_other(task_b)
task_b.set_other(task_a)
task_a.switch()
