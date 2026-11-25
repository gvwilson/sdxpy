"""Simulate LWW registers across replicas using asimpy."""

from dataclasses import dataclass
import random
from asimpy import Environment, Process
from lwwregister import LWWRegister
from dsdx import dsdx


@dataclass
class Peer:
    name: str
    register: LWWRegister


# mccole:replica
NAMES = ["Ahmed", "Baemi", "Chiti"]
VALUES = ["red", "green", "blue", "yellow"]


class Replica(Process):
    """A replica that writes to its local register and syncs with peers."""

    def init(self, name, register, peers, write_interval, sync_interval):
        self.name = name
        self.register = register
        self.peers = peers
        self.write_interval = write_interval
        self.sync_interval = sync_interval

    async def run(self):
        """Alternate between local writes and syncing with a random peer."""
        while True:
            # Write a random value using simulation time as the timestamp.
            value = random.choice(VALUES)
            self.register.set(value, self.now, self.name)
            print(f"[{self.now}] {self.name}: set '{value}'")

            await self.timeout(self.write_interval)

            # Sync with a random peer.
            peer = random.choice(self.peers)
            self.register.merge(peer.register)
            print(
                f"[{self.now}] {self.name}: synced with {peer.name} -> '{self.register.value}'"
            )

            await self.timeout(self.sync_interval)
# mccole:/replica


# mccole:sim
def main():
    """Demonstrate LWWRegister convergence across three replicas."""
    env = Environment()
    replicas = [Peer(name, LWWRegister()) for name in NAMES]
    processes = []
    for r in replicas:
        peers = [p for p in replicas if p is not r]
        proc = Replica(
            env, r.name, r.register, peers, write_interval=2, sync_interval=3
        )
        processes.append(proc)

    env.run(until=10)
    print("\n--- Final State")
    for r in replicas:
        print(f"{r.name}: {r.register}")
# mccole:/sim


if __name__ == "__main__":
    dsdx(main)
