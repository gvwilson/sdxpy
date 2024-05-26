from abc import ABC, abstractmethod


class Obs(ABC):
    def __init__(self):
        self._watching = []

    def watch(self, other):
        if other not in self._watching:
            self._watching.append(other)
        return self

    def sync(self):
        act = [other.sync() for other in self._watching]
        act = any(act) or self.stale()
        if act:
            self.action()
        return act

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
    a.sync()

