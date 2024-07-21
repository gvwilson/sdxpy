from pydes import Component, Simulator


class Worker(Component):
    NUM_STEPS = 3
    WORK_TIME = 2

    def __init__(self, sim):
        self._sim = sim

    def main(self):
        for i in range(self.NUM_STEPS):
            print(f"start to work at {self._sim.now()}")
            self._sim.sleep(self.WORK_TIME)
        print(f"finished working at {self._sim.now()}")


def simulate():
    sim = Simulator()
    worker = Worker(sim)
    sim.schedule(worker)
    sim.run()


if __name__ == "__main__":
    simulate()
