"""Simulation demonstrating concurrent writes creating conflicts."""

from asimpy import Environment
from storage_node import StorageNode
from coordinator import Coordinator
from kv_client import KVClient
from dsdx import dsdx


# mccole:conflictexample
def main():
    env = Environment()

    # Create 5 storage nodes
    nodes = [StorageNode(env, f"Node{i + 1}") for i in range(5)]

    # N=3, R=2, W=2
    coordinator = Coordinator(
        env, nodes, replication_factor=3, read_quorum=2, write_quorum=2
    )

    # Client 1: writes cart=["item1"]
    KVClient(
        env,
        "Client1",
        coordinator,
        [
            ("write", "cart", ["item1"]),
            ("read", "cart", None),
        ],
    )

    # Client 2: concurrently writes cart=["item2"]
    # (without seeing client1's write due to timing)
    KVClient(
        env,
        "Client2",
        coordinator,
        [
            ("write", "cart", ["item2"]),
        ],
        initial_delay=0.2,
    )

    # Client 3: reads the conflicted cart later
    KVClient(
        env,
        "Client3",
        coordinator,
        [
            ("read", "cart", None),
            ("write", "cart", ["item1", "item2"]),  # Resolved value
        ],
        initial_delay=3.0,
    )

    env.run(until=10)
# mccole:/conflictexample


if __name__ == "__main__":
    dsdx(main)
