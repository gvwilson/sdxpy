from pydes import Component, Event, Simulator
from util import format_log


class Worker(Component):
    NUM_STEPS = 3
    WORK_TIME = 2

    def __init__(self, sim, event, wait_at_start):
        self._sim = sim
        self._event = event
        self._wait_at_start = wait_at_start

    def main(self):
        if self._wait_at_start:
            self._sim.record(self, "start work")
            self._event.wait()
        for i in range(self.NUM_STEPS):
            self._sim.record(self, "start work")
            self._sim.sleep(self.WORK_TIME)
        self._sim.record(self, "finished")
        if not self._wait_at_start:
            self._event.set()


def simulate():
    sim = Simulator(trace=False)
    event = Event(sim)
    sim.schedule(Worker(sim, event, True))
    sim.schedule(Worker(sim, event, False))
    sim.run()
    print(format_log(sim.records()))


if __name__ == "__main__":
    simulate()
