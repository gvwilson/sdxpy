"""Simulation demonstrating behavior during network partition."""

from asimpy import Environment, Process
from storage_node import StorageNode
from partitioned_coordinator import PartitionedCoordinator
from kv_client import KVClient
from dsdx import dsdx


class PartitionManager(Process):
    """Process that creates and heals network partitions."""

    def init(self, coordinator: PartitionedCoordinator):
        self.coordinator = coordinator

    async def run(self):
        """Create partition, wait, then heal."""
        await self.timeout(2.0)
        self.coordinator.partition_node("Node3")

        # Wait for partition to heal
        await self.timeout(3.0)
        self.coordinator.heal_partition("Node3")


# mccole:partitionexample
def main():
    """Demonstrate behavior during network partition."""
    env = Environment()

    nodes = [StorageNode(env, f"Node{i + 1}") for i in range(5)]
    coordinator = PartitionedCoordinator(
        env, nodes, replication_factor=3, read_quorum=2, write_quorum=2
    )

    # Initial write
    KVClient(
        env,
        "Client1",
        coordinator,
        [
            ("write", "status", "healthy"),
            ("read", "status", None),
        ],
    )

    # Client that writes after partition
    KVClient(
        env,
        "Client2",
        coordinator,
        [
            ("write", "status", "degraded"),
            ("read", "status", None),
        ],
        initial_delay=3.0,
    )

    # Create partition manager
    PartitionManager(env, coordinator)

    env.run(until=10)
# mccole:/partitionexample


if __name__ == "__main__":
    dsdx(main)
