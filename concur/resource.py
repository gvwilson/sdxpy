import greenlet


class Resource:
    def __init__(self):
        self._current = None

    def acquire(self, who):
        if self._current is not None:
            return False
        self._current = who
        return True

    def release(self):
        assert self._current is not None
        self._current = None

    def heldby(self, who):
        return self._current == who


class Task(greenlet.greenlet):
    def __init__(self, name, resource, activity):
        self._name = name
        self._resource = resource
        self._activity = activity

    def run(self):
        for (which, (kind, duration)) in enumerate(self._activity):
            if kind == "work":
                self._work(which, duration)
            elif kind == "use":
                i = 0
                while i < duration:
                    if self._resource.heldby(self):
                        i = self._use_once(which, duration, i)
                    elif self._resource.acquire(self):
                        print(f"{self._name} {which} use/acquire")
                    else:
                        print(f"{self._name} {which} use/waiting")
                    self.parent.switch()
            else:
                assert False, f"{self._name}: unknown activity kind {kind}"

    def _use_once(self, which, duration, i):
        print(f"{self._name} {which} use/hold {i}/{duration}")
        i += 1
        if i == duration:
            self._resource.release()
            print(f"{self._name} {which} use/release")
        return i

    def _work(self, which, duration):
        for i in range(duration):
            print(f"{self._name} {which} work {i}/{duration}")
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
    resource = Resource()
    task_a = Task("A", resource, (("work", 1), ("use", 3), ("use", 1)))
    task_b = Task("B", resource, (("work", 1), ("use", 2)))
    scheduler = Scheduler(task_a, task_b)
    scheduler.run()
