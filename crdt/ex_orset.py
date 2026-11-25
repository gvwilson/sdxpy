"""Simulate OR-Sets across replicas using asimpy."""

from dataclasses import dataclass
import random
from asimpy import Environment, Process
from orset import ORSet
from dsdx import dsdx


@dataclass
class Peer:
    name: str
    orset: ORSet


# mccole:replica
NAMES = ["Ahmed", "Baemi", "Chiti"]
ITEMS = ["apple", "banana", "cherry"]
P_REMOVE = 0.3


class Replica(Process):
    """A replica that adds/removes items and syncs with peers."""

    def init(self, name, orset, peers, update_interval, sync_interval):
        self.name = name
        self.orset = orset
        self.peers = peers
        self.update_interval = update_interval
        self.sync_interval = sync_interval

    async def run(self):
        """Alternate between local updates and syncing with a random peer."""
        while True:
            # Add or remove an item.
            item = random.choice(ITEMS)
            if self.orset.contains(item) and random.random() < P_REMOVE:
                self.orset.remove(item)
                print(
                    f"[{self.now}] {self.name}: remove '{item}' -> {sorted(self.orset.value())}"
                )
            else:
                self.orset.add(item)
                print(
                    f"[{self.now}] {self.name}: add '{item}' -> {sorted(self.orset.value())}"
                )

            await self.timeout(self.update_interval)

            # Sync with a random peer.
            peer = random.choice(self.peers)
            self.orset.merge(peer.orset)
            print(
                f"[{self.now}] {self.name}: synced with {peer.name} -> {sorted(self.orset.value())}"
            )

            await self.timeout(self.sync_interval)
# mccole:/replica


# mccole:sim
def main():
    """Demonstrate OR-Set convergence across three replicas."""
    env = Environment()
    replicas = [Peer(name, ORSet(name)) for name in NAMES]
    processes = []
    for r in replicas:
        peers = [p for p in replicas if p is not r]
        proc = Replica(env, r.name, r.orset, peers, update_interval=2, sync_interval=3)
        processes.append(proc)

    env.run(until=10)
    print("\n--- Final State")
    for r in replicas:
        print(f"{r.name}: {sorted(r.orset.value())}")
# mccole:/sim


if __name__ == "__main__":
    dsdx(main)
