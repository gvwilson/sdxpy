from collections import deque

from environment import Event


# mccole:queue
class Queue:
    """A FIFO device that processes can block on."""

    def __init__(self, env):
        self.env = env
        self._items = deque()
        self._getters = deque()  # Event objects waiting for data

    def get(self):
        """Return an Event that resolves to the next item."""
        if self._items:
            item = self._items.popleft()
            evt = Event(self.env)
            evt.set(item)
            return evt
        evt = Event(self.env)
        self._getters.append(evt)
        return evt

    def put(self, item):
        """Deliver an item, waking a waiting getter if there is one."""
        if self._getters:
            getter = self._getters.popleft()
            getter.set(item)
        else:
            self._items.append(item)
        evt = Event(self.env)
        evt.set(True)
        return evt
# mccole:/queue
