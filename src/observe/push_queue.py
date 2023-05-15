from abc import ABC, abstractmethod


class Obs(ABC):
    def __init__(self, queue):
        self._observers = []
        self._required = 0
        self._current = 0
        self._queue = queue

    def watch(self, other):
        other.add_observer(self)
        self._required += 1
        return self

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self, source=None):
        assert source != self, "Circular dependency!"
        self._current += 1
        if self._current >= self._required:
            self._queue.add(self)
            for other in self._observers:
                other.notify(source if source is not None else self)
            self._current = 0

    def stale(self):
        return False

    @abstractmethod
    def action(self):
        pass


class Source(Obs):
    def __init__(self, queue, message):
        super().__init__(queue)
        self._is_stale = True
        self._message = message

    def stale(self):
        return self._is_stale

    def action(self):
        print(self._message)
        self._is_stale = False


class Node(Obs):
    def __init__(self, queue, message):
        super().__init__(queue)
        self._message = message

    def action(self):
        print(self._message)


class Queue:
    def __init__(self):
        self._items = []

    def add(self, thing):
        self._items.append(thing)

    def run(self):
        while self._items:
            self._items.pop(0).action()


if __name__ == "__main__":
    queue = Queue()
    a = Node(queue, "A")
    b = Node(queue, "B")
    c = Node(queue, "C")
    d = Source(queue, "D")
    a.watch(b)
    a.watch(c)
    b.watch(d)
    c.watch(d)
    d.notify()
    queue.run()
