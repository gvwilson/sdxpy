"""Simulate GCounters converging despite a network partition."""

from dataclasses import dataclass, field
import random
from asimpy import Environment, Process
from gcounter import GCounter
from dsdx import dsdx


# mccole:peer
@dataclass
class Peer:
    name: str
    counter: GCounter
    partitioned_from: set = field(default_factory=set)
# mccole


# mccole:replica
class Replica(Process):
    """A replica that increments and syncs, respecting partitions."""

    def init(self, name, counter, peer_record, all_peers, interval):
        self.name = name
        self.counter = counter
        self.peer_record = peer_record
        self.all_peers = all_peers
        self.interval = interval

    async def run(self):
        while True:
            self.counter.increment()
            print(f"[{self.now}] {self.name}: increment -> {self.counter.value()}")
            await self.timeout(self.interval)

            # Try to sync with a random peer.
            peer = random.choice(
                [p for p in self.all_peers if p is not self.peer_record]
            )
            if peer.name in self.peer_record.partitioned_from:
                print(f"[{self.now}] {self.name}: cannot reach {peer.name}")
            else:
                self.counter.merge(peer.counter)
                print(
                    f"[{self.now}] {self.name}: synced with {peer.name} -> {self.counter.value()}"
                )
            await self.timeout(self.interval)
# mccole:/replica


# mccole:partition
class PartitionController(Process):
    """Create and heal a network partition between two peers."""

    def init(self, peer_a, peer_b, start, end):
        self.peer_a = peer_a
        self.peer_b = peer_b
        self.start = start
        self.end = end

    async def run(self):
        await self.timeout(self.start)
        self.peer_a.partitioned_from.add(self.peer_b.name)
        self.peer_b.partitioned_from.add(self.peer_a.name)
        print(
            f"[{self.now}] *** partition: {self.peer_a.name} <-/-> {self.peer_b.name}"
        )

        await self.timeout(self.end - self.start)
        self.peer_a.partitioned_from.discard(self.peer_b.name)
        self.peer_b.partitioned_from.discard(self.peer_a.name)
        print(f"[{self.now}] *** healed: {self.peer_a.name} <---> {self.peer_b.name}")
# mccole:/partition


# mccole:sim
NAMES = ["Ahmed", "Baemi", "Chiti"]


def main():
    """Show that GCounters converge after a partition heals."""
    env = Environment()
    peers = [Peer(name, GCounter(name)) for name in NAMES]
    for p in peers:
        Replica(env, p.name, p.counter, p, peers, interval=2)

    # Partition Ahmed from Baemi between time 3 and time 8.
    PartitionController(env, peers[0], peers[1], start=3, end=11)

    env.run(until=14)
    print("\n--- Final State")
    for p in peers:
        print(p.counter)
# mccole:/sim


if __name__ == "__main__":
    dsdx(main)
