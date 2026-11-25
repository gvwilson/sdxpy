"""Simulate operation-based counters across replicas using asimpy."""

from dataclasses import dataclass, field
import random
from asimpy import Environment, Process
from opbased_counter import OpBasedCounter
from dsdx import dsdx


NAMES = ["Ahmed", "Baemi", "Chiti"]
P_DECREMENT = 0.3


@dataclass
class Peer:
    name: str
    counter: OpBasedCounter
    inbox: list = field(default_factory=list)


# mccole:replica
class Replica(Process):
    """A replica that creates operations and broadcasts them to peers."""

    def init(self, name, counter, peer_record, all_peers, interval):
        self.name = name
        self.counter = counter
        self.peer_record = peer_record
        self.all_peers = all_peers
        self.interval = interval
        self.op_counter = 0

    async def run(self):
        """Create operations, apply locally, and broadcast to peers."""
        while True:
            # Create an operation.
            if random.random() < P_DECREMENT:
                op = self.counter.decrement()
                label = "decrement"
            else:
                op = self.counter.increment()
                label = "increment"

            # Generate a unique ID and apply locally.
            self.op_counter += 1
            op_id = f"{self.name}-{self.op_counter}"
            self.counter.apply(op, op_id)
            print(f"[{self.now}] {self.name}: {label} -> {self.counter.value}")

            # Broadcast to all peers' inboxes.
            for peer in self.all_peers:
                if peer is not self.peer_record:
                    peer.inbox.append((op, op_id))

            await self.timeout(self.interval)

            # Process any operations received from peers.
            for op, op_id in self.peer_record.inbox:
                self.counter.apply(op, op_id)
            self.peer_record.inbox.clear()
            print(f"[{self.now}] {self.name}: applied inbox -> {self.counter.value}")

            await self.timeout(self.interval)
# mccole:/replica


# mccole:sim
def main():
    """Demonstrate OpBasedCounter convergence across three replicas."""
    env = Environment()
    peers = [Peer(name, OpBasedCounter(name)) for name in NAMES]
    for p in peers:
        Replica(env, p.name, p.counter, p, peers, interval=2)

    env.run(until=10)
    print("\n--- Final State")
    for p in peers:
        print(p.counter)
# mccole:/sim


if __name__ == "__main__":
    dsdx(main)
