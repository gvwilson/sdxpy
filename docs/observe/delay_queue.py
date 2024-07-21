from abc import ABC, abstractmethod


class Obs(ABC):
    def __init__(self, queue):
        self._observers = []
        self._required = 0
        self._current = 0
        self._queue = queue
        self._notifier = None

    def watch(self, other):
        if other.add_observer(self):
            self._required += 1

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
            return True
        return False

    def notify(self, source=None):
        assert source != self, "Circular dependency!"
        self._current += 1
        if self._current >= self._required:
            self._notifier = source if source is not None else self
            self._queue.add(self)

    def downstream(self):
        for other in self._observers:
            other.notify(self._notifier)

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
        self._pending = []
        self._complete = []

    def add(self, thing):
        self._pending.append(thing)

    def run(self, verbose=False):
        while self._pending or self._complete:
            while self._pending:
                obj = self._pending.pop(0)
                if verbose:
                    print(f'{obj._message} action')
                obj.action()
                self._complete.append(obj)
            while self._complete:
                obj = self._complete.pop(0)
                if verbose:
                    print(f'{obj._message} complete')
                obj.downstream()


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
