from abc import ABC, abstractmethod


class Obs(ABC):
    def __init__(self):
        self._observers = []
        self._required = 0
        self._current = 0

    def watch(self, other):
        other.add_observer(self)
        self._required += 1
        return self

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self):
        self._current += 1
        if self._current >= self._required:
            self.action()
            for other in self._observers:
                other.notify()
            self._current = 0

    def stale(self):
        return False

    @abstractmethod
    def action(self):
        pass


class Source(Obs):
    def __init__(self, message):
        super().__init__()
        self._is_stale = True
        self._message = message

    def stale(self):
        return self._is_stale

    def action(self):
        print(self._message)
        self._is_stale = False


class Node(Obs):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def action(self):
        print(self._message)


if __name__ == "__main__":
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Source("D")
    a.watch(b)
    a.watch(c)
    b.watch(d)
    c.watch(d)
    d.notify()

