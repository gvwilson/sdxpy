"""Simulate CRDT counters across replicas using asimpy."""

from dataclasses import dataclass
import random
from asimpy import Environment, Process
from gcounter import GCounter
from pncounter import PNCounter
from dsdx import dsdx


NAMES = ["Ahmed", "Baemi", "Chiti"]
P_DECREMENT = 0.5


@dataclass
class Peer:
    name: str
    counter: GCounter | PNCounter


# mccole:replica
class Replica(Process):
    """A replica that updates its local counter and syncs with peers."""

    def init(self, name, counter, peers, update_interval, sync_interval):
        self.name = name
        self.counter = counter
        self.peers = peers
        self.update_interval = update_interval
        self.sync_interval = sync_interval

    async def run(self):
        """Alternate between local updates and syncing with a random peer."""
        while True:
            # Perform a local update.
            if isinstance(self.counter, PNCounter) and random.random() < P_DECREMENT:
                self.counter.decrement()
                op = "decrement"
            else:
                self.counter.increment()
                op = "increment"
            print(f"[{self.now}] {self.name}: {op} -> {self.counter.value()}")

            await self.timeout(self.update_interval)

            # Sync with a random peer.
            peer = random.choice(self.peers)
            self.counter.merge(peer.counter)
            print(
                f"[{self.now}] {self.name}: synced with {peer.name} -> {self.counter.value()}"
            )

            await self.timeout(self.sync_interval)
# mccole:/replica


# mccole:sim
def run_simulation(counter_cls):
    """Demonstrate GCounter convergence across three replicas."""
    env = Environment()
    replicas = [Peer(name, counter_cls(name)) for name in NAMES]
    processes = []
    for r in replicas:
        peers = [p for p in replicas if p is not r]
        proc = Replica(
            env, r.name, r.counter, peers, update_interval=2, sync_interval=3
        )
        processes.append(proc)

    env.run(until=10)
    print("\n--- Final State")
    for r in replicas:
        print(r.counter)
# mccole:/sim


def main():
    print("=== GCounter")
    run_simulation(GCounter)
    print("\n=== PNCounter")
    run_simulation(PNCounter)


if __name__ == "__main__":
    dsdx(main)
