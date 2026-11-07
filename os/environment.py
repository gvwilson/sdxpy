import heapq
import itertools
from collections import deque

_serial = itertools.count()


# mccole:event
class Event:
    """An awaitable object that processes can wait for."""

    def __init__(self, env):
        self.env = env
        self._value = None
        self._done = False
        self._waiters = []

    def set(self, value=None):
        """Wake every process that is waiting on this event."""
        if self._done:
            return
        self._value = value
        self._done = True
        for process in self._waiters:
            self.env.schedule(process.step)
        self._waiters.clear()

    def _add_waiter(self, process):
        if self._done:
            self.env.schedule(process.step)
        else:
            self._waiters.append(process)

    def __await__(self):
        if not self._done:
            yield self
        return self._value
# mccole:/event


# mccole:timeout
class Timeout(Event):
    """An event that fires after a delay of simulated time."""

    def __init__(self, env, delay):
        super().__init__(env)
        env.schedule_at(env.now + delay, self._fire)

    def _fire(self):
        self.set()
# mccole:/timeout


# mccole:environment
class Environment:
    """The kernel: a ready queue plus a simulated clock."""

    def __init__(self):
        self.now = 0
        self._ready = deque()
        self._heap = []
        self._log = []

    def schedule(self, callback):
        """Queue a callback to run at the current simulated time."""
        self._ready.append(callback)

    def schedule_at(self, time, callback):
        """Queue a callback to run at a future simulated time."""
        heapq.heappush(self._heap, (time, next(_serial), callback))

    def sleep(self, delay):
        """Return an event that fires after ``delay`` time units."""
        return Timeout(self, delay)

    def create_process(self, name, coro):
        """Start a coroutine as a named process."""
        process = Process(name, coro, self)
        self.schedule(process.step)
        return process

    def run(self):
        """Run until there is no work left to do."""
        while True:
            while self._ready:
                callback = self._ready.popleft()
                callback()
            if not self._heap:
                break
            time, _, callback = heapq.heappop(self._heap)
            self.now = time
            callback()

    def log(self, name, message):
        self._log.append((self.now, name, message))

    def get_log(self):
        return self._log
# mccole:/environment


# mccole:process
class Process:
    """A named coroutine that the kernel drives."""

    def __init__(self, name, coro, env):
        self.name = name
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
# mccole:/process
