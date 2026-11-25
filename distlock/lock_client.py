from asimpy import Process, Queue
from basic_lock_server import LockServer, LockRequest


# mccole:client_init
class LockClient(Process):
    """Client that acquires locks to access resources."""

    def init(
        self,
        client_id: str,
        server: LockServer,
        resource: str,
        work_duration: float,
        initial_delay: float | None = None,
    ):
        self.client_id = client_id
        self.server = server
        self.resource = resource
        self.work_duration = work_duration
        self.initial_delay = initial_delay
        self.current_token: int | None = None
    # mccole:/client_init

    # mccole:client_run
    async def run(self):
        """Acquire lock, do work, release lock."""
        # Possibly delay start
        if self.initial_delay is not None:
            await self.timeout(self.initial_delay)

        # Try to acquire lock
        acquired = await self.acquire_lock()
        if not acquired:
            print(f"[{self.now:.1f}] {self.client_id}: Failed to acquire lock")
            return

        # Do work with the lock held
        print(
            f"[{self.now:.1f}] {self.client_id}: Starting critical section "
            f"(token {self.current_token})"
        )
        await self.timeout(self.work_duration)
        print(f"[{self.now:.1f}] {self.client_id}: Finished critical section")

        # Release lock
        await self.release_lock()
    # mccole:/client_run

    # mccole:client_acquire
    async def acquire_lock(self) -> bool:
        """Request lock from server."""
        response_queue = Queue(self._env)
        request = LockRequest(
            client_id=self.client_id,
            resource=self.resource,
            operation="acquire",
            response_queue=response_queue,
        )

        await self.server.request_queue.put(request)
        response = await response_queue.get()

        if response.success:
            self.current_token = response.token
            return True
        return False
    # mccole:/client_acquire

    # mccole:client_release
    async def release_lock(self):
        """Release lock back to server."""
        response_queue = Queue(self._env)
        request = LockRequest(
            client_id=self.client_id,
            resource=self.resource,
            operation="release",
            response_queue=response_queue,
        )

        await self.server.request_queue.put(request)
        await response_queue.get()
        self.current_token = None
    # mccole:/client_release
