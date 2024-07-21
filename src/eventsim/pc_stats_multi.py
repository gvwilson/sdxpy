from pydes import Component, Queue, Simulator
import random
import sys


class Lag:
    def __init__(self, sim, owner, which):
        self._sim = sim
        self._owner = owner
        self._which = which
        self._previous = None

    def update(self):
        current = self._sim.now()
        if self._previous is None:
            self._previous = current
        else:
            self._sim.record(self._owner, current - self._previous, self._which)
            self._previous = current


class Producer(Component):
    WORK_TIME = (1, 10)

    def __init__(self, sim, queue, num_items):
        self._sim = sim
        self._queue = queue
        self._num_items = num_items
        self._lag = Lag(sim, self, "produce")

    def main(self):
        current = None
        for i in range(self._num_items):
            delay = random.randint(*self.WORK_TIME)
            self._sim.sleep(delay)
            self._lag.update()
            self._queue.put(i)


class Consumer(Component):
    WORK_TIME = (1, 10)

    def __init__(self, sim, queue, num_items):
        self._sim = sim
        self._queue = queue
        self._num_items = num_items
        self._lag = Lag(sim, self, "consume")

    def main(self):
        current = None
        for i in range(self._num_items):
            self._queue.get()
            self._lag.update()
            delay = random.randint(*self.WORK_TIME)
            self._sim.sleep(delay)


def simulate(num_items, queue_size, num_producers):
    sim = Simulator(trace=False)
    queue = Queue(sim, queue_size)
    for i in range(num_producers):
        sim.schedule(Producer(sim, queue, num_items))
    sim.schedule(Consumer(sim, queue, num_items * num_producers))
    sim.run()

    records = sim.records()
    produced = mean_diff(records, "produce")
    consumed = mean_diff(records, "consume")
    print(f"produce {produced:.2f} consume {consumed:.2f}")


def mean_diff(records, which):
    diffs = [r.value for r in records if r.description == which]
    return sum(diffs) / len(diffs)


if __name__ == "__main__":
    random.seed(int(sys.argv[1]))
    num_items = int(sys.argv[2])
    queue_size = int(sys.argv[3])
    num_producers = int(sys.argv[4])
    simulate(num_items, queue_size, num_producers)
