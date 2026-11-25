"""Coordinator that manages replication with quorum protocol."""

from asimpy import Environment, Queue
from typing import Any
from storage_node import StorageNode
from vector_clock import VectorClock
from versioned_value import VersionedValue
from messages import ReadRequest, WriteRequest


# mccole:coord_init
class Coordinator:
    """Coordinates read/write operations across replicas."""

    def __init__(
        self,
        env: Environment,
        nodes: list[StorageNode],
        replication_factor: int = 3,
        read_quorum: int = 2,
        write_quorum: int = 2,
    ):
        self.env = env
        self.nodes = nodes
        self.replication_factor = replication_factor
        self.read_quorum = read_quorum
        self.write_quorum = write_quorum

        # Simple consistent hashing: hash key to determine replicas
        # In production, use proper consistent hashing ring

    def _get_replicas(self, key: str) -> list[StorageNode]:
        """Determine which nodes should store this key."""
        # Hash key to starting position, then take N consecutive nodes
        hash_val = hash(key) % len(self.nodes)
        replicas = []
        for i in range(self.replication_factor):
            idx = (hash_val + i) % len(self.nodes)
            replicas.append(self.nodes[idx])
        return replicas
    # mccole:/coord_init

    # mccole:coord_read
    async def read(self, key: str, client_id: str) -> list[VersionedValue]:
        """Read from R replicas and return all versions."""
        replicas = self._get_replicas(key)

        # Send read requests to all replicas
        response_queues = []
        for replica in replicas:
            response_queue = Queue(self.env)
            response_queues.append(response_queue)

            request = ReadRequest(key, client_id, response_queue)
            await replica.request_queue.put(request)

        # Wait for quorum of responses
        responses = []
        for i in range(self.read_quorum):
            response = await response_queues[i].get()
            responses.append(response)

        # Merge all versions from all responses
        all_versions = []
        for response in responses:
            all_versions.extend(response.versions)

        # Remove duplicates and superseded versions
        merged_versions = self._merge_versions(all_versions)

        # Read repair: if we got different versions, update lagging replicas
        if len(responses) < len(replicas):
            # Some replicas didn't respond yet, but we can still do read repair
            pass  # Simplified: skip read repair for now

        return merged_versions
    # mccole:/coord_read

    # mccole:coord_write
    async def write(
        self, key: str, value: Any, context: VectorClock | None, client_id: str
    ) -> VectorClock | None:
        """Write to W replicas."""
        replicas = self._get_replicas(key)

        # Send write requests to all replicas
        response_queues = []
        for replica in replicas:
            response_queue = Queue(self.env)
            response_queues.append(response_queue)

            request = WriteRequest(key, value, context, client_id, response_queue)
            await replica.request_queue.put(request)

        # Wait for quorum of responses
        responses = []
        for i in range(self.write_quorum):
            response = await response_queues[i].get()
            responses.append(response)

        # Return the highest clock
        clocks = [r.clock for r in responses]
        merged_clock = clocks[0].copy()
        for clock in clocks[1:]:
            merged_clock.merge(clock)

        return merged_clock
    # mccole:/coord_write

    # mccole:coord_merge
    def _merge_versions(self, versions: list[VersionedValue]) -> list[VersionedValue]:
        """Merge versions, keeping only concurrent ones."""
        if not versions:
            return []

        # Remove duplicates (same clock)
        unique = {}
        for v in versions:
            clock_str = str(v.clock)
            if clock_str not in unique:
                unique[clock_str] = v

        versions = list(unique.values())

        # Remove superseded versions
        result = []
        for i, v1 in enumerate(versions):
            superseded = False
            for j, v2 in enumerate(versions):
                if i != j and v1.clock.happens_before(v2.clock):
                    superseded = True
                    break
            if not superseded:
                result.append(v1)

        return result
    # mccole:/coord_merge
