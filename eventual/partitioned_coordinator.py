"""Coordinator that can simulate network partitions."""

from asimpy import Environment, Queue
from typing import Any
from coordinator import Coordinator
from storage_node import StorageNode
from vector_clock import VectorClock
from versioned_value import VersionedValue
from messages import ReadRequest, WriteRequest


# mccole:partition_init
class PartitionedCoordinator(Coordinator):
    """Coordinator that can simulate network partitions."""

    def __init__(
        self,
        env: Environment,
        nodes: list[StorageNode],
        replication_factor: int = 3,
        read_quorum: int = 2,
        write_quorum: int = 2,
    ):
        super().__init__(env, nodes, replication_factor, read_quorum, write_quorum)
        self.partitioned_nodes: set[str] = set()

    def partition_node(self, node_id: str):
        """Simulate network partition for a node."""
        self.partitioned_nodes.add(node_id)
        print(f"[{self.env.now:.1f}] PARTITION: {node_id} is unreachable")

    def heal_partition(self, node_id: str):
        """Heal network partition for a node."""
        self.partitioned_nodes.discard(node_id)
        print(f"[{self.env.now:.1f}] HEALED: {node_id} is reachable")
    # mccole:/partition_init

    # mccole:partition_read
    async def read(self, key: str, client_id: str) -> list[VersionedValue]:
        """Read, skipping partitioned nodes."""
        replicas = self._get_replicas(key)
        available_replicas = [
            r for r in replicas if r.node_id not in self.partitioned_nodes
        ]

        if len(available_replicas) < self.read_quorum:
            print(f"[{self.env.now:.1f}] Read failed: insufficient replicas")
            return []

        # Send to available replicas
        response_queues = []
        for replica in available_replicas[: self.read_quorum]:
            response_queue = Queue(self.env)
            response_queues.append(response_queue)

            request = ReadRequest(key, client_id, response_queue)
            await replica.request_queue.put(request)

        responses = []
        for queue in response_queues:
            response = await queue.get()
            responses.append(response)

        all_versions = []
        for response in responses:
            all_versions.extend(response.versions)

        return self._merge_versions(all_versions)
    # mccole:/partition_read

    # mccole:partition_write
    async def write(
        self, key: str, value: Any, context: VectorClock | None, client_id: str
    ) -> VectorClock | None:
        """Write, skipping partitioned nodes."""
        replicas = self._get_replicas(key)
        available_replicas = [
            r for r in replicas if r.node_id not in self.partitioned_nodes
        ]

        if len(available_replicas) < self.write_quorum:
            print(f"[{self.env.now:.1f}] Write failed: insufficient replicas")
            return None

        # Send to available replicas
        response_queues = []
        for replica in available_replicas[: self.write_quorum]:
            response_queue = Queue(self.env)
            response_queues.append(response_queue)

            request = WriteRequest(key, value, context, client_id, response_queue)
            await replica.request_queue.put(request)

        responses = []
        for queue in response_queues:
            response = await queue.get()
            responses.append(response)

        clocks = [r.clock for r in responses]
        merged_clock = clocks[0].copy()
        for clock in clocks[1:]:
            merged_clock.merge(clock)

        return merged_clock
    # mccole:/partition_write
