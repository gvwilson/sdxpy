# mccole:event
class Event:
    """An awaitable object that tasks can wait for."""

    def __init__(self, env):
        self.env = env
        self._value = None
        self._done = False
        self._waiters = []

    def set(self, value=None):
        """Wake every task that is waiting on this event."""
        if self._done:
            return
        self._value = value
        self._done = True
        for task in self._waiters:
            self.env.schedule(task.step)
        self._waiters.clear()

    def _add_waiter(self, task):
        """Register a task that is about to await this event."""
        if self._done:
            self.env.schedule(task.step)
        else:
            self._waiters.append(task)

    def __await__(self):
        if not self._done:
            yield self
        return self._value
# mccole:/event
