"""Simulation demonstrating read repair convergence."""

from asimpy import Environment
from storage_node import StorageNode
from coordinator_with_read_repair import CoordinatorWithReadRepair
from kv_client import KVClient
from dsdx import dsdx


# mccole:readrepairexample
def main():
    env = Environment()

    nodes = [StorageNode(env, f"Node{i + 1}") for i in range(3)]
    coordinator = CoordinatorWithReadRepair(
        env, nodes, replication_factor=3, read_quorum=2, write_quorum=2
    )

    # Initial write that reaches only 2 nodes
    KVClient(
        env,
        "Client1",
        coordinator,
        [
            ("write", "data", "initial"),
        ],
    )

    # Client that reads after delay (triggers read repair)
    KVClient(
        env,
        "Client2",
        coordinator,
        [
            ("read", "data", None),
        ],
        initial_delay=2.0,
    )

    # Another client reads later to verify all nodes have the data
    KVClient(
        env,
        "Client3",
        coordinator,
        [
            ("read", "data", None),
        ],
        initial_delay=4.0,
    )

    env.run(until=10)
# mccole:/readrepairexample


if __name__ == "__main__":
    dsdx(main)
