from pydes import Component, Simulator
from util import format_log


class Worker(Component):
    NUM_STEPS = 3
    WORK_TIME = 2

    def __init__(self, sim):
        self._sim = sim

    def main(self):
        for i in range(self.NUM_STEPS):
            self._sim.record(self, "start work")
            self._sim.sleep(self.WORK_TIME)
        self._sim.record(self, "finished")


def simulate():
    sim = Simulator(trace=False)
    worker = Worker(sim)
    sim.schedule(worker)
    sim.run()
    print(format_log(sim.records()))


if __name__ == "__main__":
    simulate()
