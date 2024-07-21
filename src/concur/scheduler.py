import greenlet


class Task(greenlet.greenlet):
    def __init__(self, name, count):
        self._name = name
        self._count = count

    def run(self):
        while self._count:
            print(f"=> {self._name} {self._count}")
            self._count -= 1
            self.parent.switch()


class Scheduler(greenlet.greenlet):
    def __init__(self, *tasks):
        self._queue = list(tasks)

    def run(self):
        while self._queue:
            task = self._queue.pop(0)
            task.switch()
            if not task.dead:
                self._queue.append(task)


if __name__ == "__main__":
    scheduler = Scheduler(Task("A", 2), Task("B", 3))
    scheduler.run()
