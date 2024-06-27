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


scheduler = Scheduler(Task("first", 2), Task("second", 3))
scheduler.run()
