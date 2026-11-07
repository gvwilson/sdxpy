from collections import deque

from event import Event


# mccole:environment
class Environment:
    """Runs tasks one ``await`` at a time."""

    def __init__(self):
        self._ready = deque()
        self._log = []

    def schedule(self, callback):
        """Queue a callback to run at the current simulated time."""
        self._ready.append(callback)

    def create_task(self, coro):
        """Start a coroutine as a new task."""
        task = Task(coro, self)
        self.schedule(task.step)
        return task

    def run(self):
        """Run until there is no work left to do."""
        while self._ready:
            callback = self._ready.popleft()
            callback()

    def log(self, name, message):
        self._log.append((name, message))

    def get_log(self):
        return self._log
# mccole:/environment


# mccole:task
class Task:
    """A wrapper that drives a single coroutine."""

    def __init__(self, coro, env):
        self.coro = coro
        self.env = env
        self.done = False

    def step(self):
        if self.done:
            return
        try:
            yielded = self.coro.send(None)
        except StopIteration:
            self.done = True
            return
        if isinstance(yielded, Event):
            yielded._add_waiter(self)
        else:
            self.env.schedule(self.step)
# mccole:/task
