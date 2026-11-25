"""Storage node that maintains replicas of keys."""

from asimpy import Process, Queue
from collections import defaultdict
from vector_clock import VectorClock
from versioned_value import VersionedValue
from messages import ReadRequest, WriteRequest, ReadResponse, WriteResponse


# mccole:storage_init
class StorageNode(Process):
    """A storage node that maintains replicas of keys."""

    def init(self, node_id: str):
        self.node_id = node_id
        self.request_queue = Queue(self._env)
        # Key -> list of concurrent versioned values
        self.data: dict[str, list[VersionedValue]] = defaultdict(list)
        self.clock = VectorClock()

    async def run(self):
        """Process read and write requests."""
        while True:
            request = await self.request_queue.get()

            if isinstance(request, ReadRequest):
                response = self._handle_read(request)
                await request.response_queue.put(response)
            elif isinstance(request, WriteRequest):
                response = self._handle_write(request)
                await request.response_queue.put(response)
    # mccole:/storage_init

    # mccole:storage_read
    def _handle_read(self, request: ReadRequest) -> ReadResponse:
        """Read all concurrent versions of a key."""
        versions = self.data.get(request.key, [])

        print(
            f"[{self.now:.1f}] {self.node_id}: Read {request.key} -> "
            f"{len(versions)} version(s)"
        )

        return ReadResponse(key=request.key, versions=versions.copy())
    # mccole:/storage_read

    # mccole:storage_write
    def _handle_write(self, request: WriteRequest) -> WriteResponse:
        """Write a value, handling concurrent versions."""
        # Increment our clock
        self.clock.increment(self.node_id)

        # If client provided context, merge it
        new_clock = self.clock.copy()
        if request.context:
            new_clock.merge(request.context)
            new_clock.increment(self.node_id)

        # Create new versioned value
        new_version = VersionedValue(
            value=request.value, clock=new_clock, timestamp=self.now
        )

        # Remove versions that this new version supersedes
        existing = self.data[request.key]
        new_versions = []

        for version in existing:
            # Keep version if it's concurrent with new version
            if version.clock.concurrent_with(new_clock):
                new_versions.append(version)
            elif new_clock.happens_before(version.clock):
                # The existing version supersedes the new one
                # (shouldn't happen with proper client context)
                new_versions.append(version)

        # Add the new version
        new_versions.append(new_version)
        self.data[request.key] = new_versions

        print(
            f"[{self.now:.1f}] {self.node_id}: Wrote {request.key} = "
            f"{request.value} with clock {new_clock}"
        )

        return WriteResponse(key=request.key, success=True, clock=new_clock)
    # mccole:/storage_write
