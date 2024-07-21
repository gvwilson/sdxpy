from pydes import Component, Queue, Simulator
import random
import sys


class Producer(Component):
    WORK_TIME = (1, 10)

    def __init__(self, sim, queue, num_items):
        self._sim = sim
        self._queue = queue
        self._num_items = num_items

    def main(self):
        for i in range(self._num_items):
            delay = random.randint(*self.WORK_TIME)
            self._sim.sleep(delay)
            self._sim.record(self, "produce")
            self._queue.put(i)


class Consumer(Component):
    WORK_TIME = (1, 10)

    def __init__(self, sim, queue, num_items):
        self._sim = sim
        self._queue = queue
        self._num_items = num_items

    def main(self):
        for i in range(self._num_items):
            self._queue.get()
            self._sim.record(self, "consume")
            delay = random.randint(*self.WORK_TIME)
            self._sim.sleep(delay)


def simulate(num_items, queue_size):
    sim = Simulator(trace=False)
    queue = Queue(sim, queue_size)
    sim.schedule(Producer(sim, queue, num_items))
    sim.schedule(Consumer(sim, queue, num_items))
    sim.run()

    records = sim.records()
    produced = mean_diff(records, "produce")
    consumed = mean_diff(records, "consume")
    print(f"produce {produced:.2f} consume {consumed:.2f}")


def mean_diff(records, which):
    subset = [r.time for r in records if r.value == which]
    diffs = [subset[i] - subset[i-1] for i in range(1, len(subset))]
    return sum(diffs) / len(diffs)


if __name__ == "__main__":
    random.seed(int(sys.argv[1]))
    num_items = int(sys.argv[2])
    queue_size = int(sys.argv[3])
    simulate(num_items, queue_size)
