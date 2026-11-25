"""Coordinator that performs read repair to converge replicas."""

from asimpy import Queue
from coordinator import Coordinator
from storage_node import StorageNode
from versioned_value import VersionedValue
from messages import ReadRequest, WriteRequest, ReadResponse


# mccole:repair_read
class CoordinatorWithReadRepair(Coordinator):
    """Coordinator that performs read repair."""

    async def read(self, key: str, client_id: str) -> list[VersionedValue]:
        """Read from R replicas and repair inconsistencies."""
        replicas = self._get_replicas(key)

        # Send read requests to ALL replicas (not just quorum)
        response_queues = []
        for replica in replicas:
            response_queue = Queue(self.env)
            response_queues.append(response_queue)

            request = ReadRequest(key, client_id, response_queue)
            await replica.request_queue.put(request)

        # Wait for quorum, but collect all responses for repair
        responses = []
        for i in range(min(self.read_quorum, len(response_queues))):
            response = await response_queues[i].get()
            responses.append(response)

        # Collect remaining responses in background for read repair
        remaining_responses = []
        for i in range(self.read_quorum, len(response_queues)):
            try:
                # Non-blocking check if response available
                # In real async, we'd use timeout or try_get
                response = await response_queues[i].get()
                remaining_responses.append(response)
            except Exception:
                pass

        all_responses = responses + remaining_responses

        # Merge all versions
        all_versions = []
        for response in all_responses:
            all_versions.extend(response.versions)

        merged_versions = self._merge_versions(all_versions)

        # Read repair: identify replicas that are missing versions
        if len(merged_versions) > 0 and len(all_responses) > 1:
            await self._perform_read_repair(
                key, merged_versions, replicas, all_responses
            )

        return merged_versions
    # mccole:/repair_read

    # mccole:repair_perform
    async def _perform_read_repair(
        self,
        key: str,
        merged_versions: list[VersionedValue],
        replicas: list[StorageNode],
        responses: list[ReadResponse],
    ):
        """Update lagging replicas."""
        # Determine which replicas need updates
        for i, response in enumerate(responses):
            replica = replicas[i]

            # Check if this replica is missing any versions
            replica_clocks = {str(v.clock) for v in response.versions}
            merged_clocks = {str(v.clock) for v in merged_versions}

            if replica_clocks != merged_clocks:
                print(
                    f"[{self.env.now:.1f}] READ REPAIR: Updating {replica.node_id} "
                    f"for key {key}"
                )

                # Write missing versions to this replica
                for version in merged_versions:
                    if str(version.clock) not in replica_clocks:
                        response_queue = Queue(self.env)
                        request = WriteRequest(
                            key,
                            version.value,
                            version.clock,
                            "read-repair",
                            response_queue,
                        )
                        await replica.request_queue.put(request)
                        await response_queue.get()
    # mccole:/repair_perform
