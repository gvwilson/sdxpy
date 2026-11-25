from lock_client import LockClient
from basic_lock_server import LockServer


# mccole:failingclient
class FailingClient(LockClient):
    """Client that crashes while holding a lock."""

    def init(
        self,
        client_id: str,
        server: LockServer,
        resource: str,
        work_duration: float,
        initial_delay: float | None = None,
        fail_after: float = 0.0,
    ):
        super().init(
            client_id, server, resource, work_duration, initial_delay=initial_delay
        )
        self.fail_after = fail_after

    async def run(self):
        """Acquire lock, work, then crash."""
        acquired = await self.acquire_lock()
        if not acquired:
            return

        print(f"[{self.now:.1f}] {self.client_id}: Starting work")

        # Simulate crash after some time
        await self.timeout(self.fail_after)
        print(f"[{self.now:.1f}] {self.client_id}: CRASHED!")
        # Client stops here without releasing the lock
# mccole:/failingclient
