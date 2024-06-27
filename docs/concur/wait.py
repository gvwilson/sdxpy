import greenlet


class Resource:
    def __init__(self):
        self._current = None
        self._ready = None
        self._waiting = []

    def acquire(self, who):
        if self._current is None:
            assert self._ready is None
            self._current = who
        else:
            self._waiting.append(who)
        return self._current is who

    def release(self, who):
        assert self._current is who, f"current {self._current} who {who}"
        assert self._ready is None
        self._current = None
        if self._waiting:
            self._ready = self._waiting.pop(0)

    def heldby(self, who):
        return self._current is who

    def take(self):
        who = self._ready
        self._ready = None
        return who

    def __str__(self):
        return f"R({self._current}, {self._ready}, [{', '.join(str(t) for t in self._waiting)}])"


class Task(greenlet.greenlet):
    def __init__(self, name, resource, activity):
        self._name = name
        self._resource = resource
        self._activity = activity

    def run(self):
        for (which, (kind, duration)) in enumerate(self._activity):
            if kind == "work":
                for i in range(duration):
                    print(f"{self._name} {which} work {i}/{duration}")
                    self.parent.switch(True)
            elif kind == "use":
                print(f"{self._name} {which} acquiring")
                if not self._resource.acquire(self):
                    print(f"...failed to acquire")
                    self.parent.switch(False)
                    assert self._resource.acquire(self)
                for i in range(duration):
                    print(f"{self._name} {which} using {i}/{duration}")
                    self.parent.switch(True)
                print(f"{self._name} {which} releasing")
                self._resource.release(self)
                self.parent.switch(True)
            else:
                assert False, f"{self._name}: unknown activity kind {kind}"

    def __str__(self):
        return self._name


class Scheduler(greenlet.greenlet):
    def __init__(self, resource, *tasks):
        self._resource = resource
        self._queue = list(tasks)

    def run(self):
        while self._queue:
            task = self._queue.pop(0)
            active = task.switch()
            another = self._resource.take()
            if another is not None:
                self._queue.append(another)
            if active and (not task.dead):
                self._queue.append(task)

    def __str__(self):
        return f"S({self._resource}, [{', '.join(str(t) for t in self._queue)}])"


if __name__ == "__main__":
    resource = Resource()
    task_a = Task("A", resource, (("work", 1), ("use", 3), ("use", 1)))
    task_b = Task("B", resource, (("work", 1), ("use", 2)))
    scheduler = Scheduler(resource, task_a, task_b)
    scheduler.run()
