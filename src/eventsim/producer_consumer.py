from pydes import Component, Queue, Simulator
from util import format_log


NUM_ITEMS = 10
QUEUE_SIZE = 3


class Producer(Component):
    WORK_TIME = 2

    def __init__(self, sim, queue):
        self._sim = sim
        self._queue = queue

    def main(self):
        for i in range(NUM_ITEMS):
            self._sim.sleep(self.WORK_TIME)
            self._sim.record(self, f"produce={i} queue@{self._queue.size()}")
            self._queue.put(i)


class Consumer(Component):
    WORK_TIME = 4

    def __init__(self, sim, queue):
        self._sim = sim
        self._queue = queue

    def main(self):
        for i in range(NUM_ITEMS):
            value = self._queue.get()
            self._sim.record(self, f"consume={i}")
            self._sim.sleep(self.WORK_TIME)


def simulate():
    sim = Simulator(trace=False)
    queue = Queue(sim, QUEUE_SIZE)
    sim.schedule(Producer(sim, queue))
    sim.schedule(Consumer(sim, queue))
    sim.run()
    print(format_log(sim.records()))


if __name__ == "__main__":
    simulate()
