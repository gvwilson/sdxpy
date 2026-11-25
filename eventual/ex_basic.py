"""Basic simulation demonstrating operations and conflict resolution."""

from asimpy import Environment
from storage_node import StorageNode
from coordinator import Coordinator
from kv_client import KVClient
from dsdx import dsdx


# mccole:basicexample
def main():
    env = Environment()

    # Create 3 storage nodes
    nodes = [
        StorageNode(env, "Node1"),
        StorageNode(env, "Node2"),
        StorageNode(env, "Node3"),
    ]

    # Create coordinator with R=2, W=2, N=3
    coordinator = Coordinator(
        env, nodes, replication_factor=3, read_quorum=2, write_quorum=2
    )

    # Client 1: writes X=1, then X=2
    KVClient(
        env,
        "Client1",
        coordinator,
        [
            ("write", "X", 1),
            ("write", "X", 2),
        ],
    )

    # Client 2: reads X after a delay
    KVClient(
        env,
        "Client2",
        coordinator,
        [
            ("read", "X", None),
        ],
        initial_delay=3.0,
    )

    env.run(until=10)
# mccole:/basicexample


if __name__ == "__main__":
    dsdx(main)
