from asimpy import Process
from replicated_lock_manager import ReplicatedLockManager


# mccole:replicatedclient
class ReplicatedLockClient(Process):
    """Client using replicated lock manager."""

    def init(
        self,
        client_id: str,
        manager: ReplicatedLockManager,
        resource: str,
        work_duration: float,
        initial_delay: float | None = None,
    ):
        self.client_id = client_id
        self.manager = manager
        self.resource = resource
        self.work_duration = work_duration
        self.initial_delay = initial_delay

    async def run(self):
        """Acquire lock from majority, do work, release."""
        token = await self.manager.acquire_lock(self.client_id, self.resource)

        if token is None:
            return

        print(f"[{self.now:.1f}] {self.client_id}: Working with lock")
        await self.timeout(self.work_duration)
        print(f"[{self.now:.1f}] {self.client_id}: Work complete")

        await self.manager.release_lock(self.client_id, self.resource)
# mccole:/replicatedclient
