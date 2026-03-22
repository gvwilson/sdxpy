import greenlet


class Task(greenlet.greenlet):
    def __init__(self, name):
        self._name = name

    def run(self, *args):
        print(f"{self._name} starts with {args[0]}")
        while True:
            value = self.parent.switch(self._name)
            print(f"{self._name} continue with {value}")
            if value <= 0:
                break


class Scheduler(greenlet.greenlet):
    def __init__(self, *tasks):
        self._queue = list(tasks)

    def run(self):
        ticks = 3
        while self._queue:
            task = self._queue.pop(0)
            value = task.switch(ticks)
            print(f"scheduler got {value}")
            ticks -= 1
            if not task.dead:
                self._queue.append(task)


if __name__ == "__main__":
    scheduler = Scheduler(Task("A"), Task("B"))
    scheduler.run()
