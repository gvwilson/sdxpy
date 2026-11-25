"""Client for reading and writing to the key-value store."""

from asimpy import Process
from typing import Any
from coordinator import Coordinator
from vector_clock import VectorClock


# mccole:kv_init
class KVClient(Process):
    """Client that reads and writes to the key-value store."""

    def init(
        self,
        client_id: str,
        coordinator: Coordinator,
        operations: list[tuple[str, str, Any]],
        initial_delay: float | None = None,
    ):
        self.client_id = client_id
        self.coordinator = coordinator
        self.operations = operations  # list of (op, key, value) tuples
        self.initial_delay = initial_delay
        self.context: dict[str, VectorClock | None] = {}  # Track causality per key

    async def run(self):
        """Execute operations."""
        # Wait for initial delay if specified
        if self.initial_delay is not None:
            await self.timeout(self.initial_delay)

        for op, key, value in self.operations:
            if op == "write":
                await self.write(key, value)
                await self.timeout(0.5)  # Small delay between operations
            elif op == "read":
                await self.read(key)
                await self.timeout(0.5)
    # mccole:/kv_init

    # mccole:kv_read
    async def read(self, key: str) -> Any:
        """Read a key and handle conflicts."""
        versions = await self.coordinator.read(key, self.client_id)

        if not versions:
            print(f"[{self.now:.1f}] {self.client_id}: Read {key} -> NOT FOUND")
            return None

        if len(versions) == 1:
            # No conflict
            version = versions[0]
            self.context[key] = version.clock.copy()
            print(
                f"[{self.now:.1f}] {self.client_id}: Read {key} -> "
                f"{version.value} (clock: {version.clock})"
            )
            return version.value
        else:
            # Conflict: multiple concurrent versions
            print(
                f"[{self.now:.1f}] {self.client_id}: Read {key} -> "
                f"CONFLICT: {len(versions)} versions"
            )
            for v in versions:
                print(f"  - {v.value} (clock: {v.clock}, ts: {v.timestamp})")

            # Resolve conflict: last-write-wins based on timestamp
            latest = max(versions, key=lambda v: v.timestamp)

            # Merge all clocks to preserve causality
            merged_clock = versions[0].clock.copy()
            for v in versions[1:]:
                merged_clock.merge(v.clock)

            self.context[key] = merged_clock
            print(f"[{self.now:.1f}] {self.client_id}: Resolved to {latest.value}")
            return latest.value
    # mccole:/kv_read

    # mccole:kv_write
    async def write(self, key: str, value: Any):
        """Write a key with causal context."""
        context = self.context.get(key)

        clock = await self.coordinator.write(key, value, context, self.client_id)
        self.context[key] = clock

        print(f"[{self.now:.1f}] {self.client_id}: Wrote {key} = {value}")
    # mccole:/kv_write
