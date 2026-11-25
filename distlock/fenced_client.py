from asimpy import Process, Queue
from basic_lock_server import LockServer, LockRequest
from protected_resource import ProtectedResource


# mccole:fenced_init
class FencedClient(Process):
    """Client that uses fencing tokens when accessing resources."""

    def init(
        self,
        client_id: str,
        server: LockServer,
        resource_name: str,
        protected_resource: ProtectedResource,
        work_duration: float,
        pause_duration: float = 0,
        initial_delay: float | None = None,
    ):
        self.client_id = client_id
        self.server = server
        self.resource_name = resource_name
        self.protected_resource = protected_resource
        self.work_duration = work_duration
        self.pause_duration = pause_duration
        self.initial_delay = initial_delay
        self.current_token: int = 0
    # mccole:/fenced_init

    # mccole:fenced_run
    async def run(self):
        """Acquire lock and access resource with token."""
        # Potentially delay start
        if self.initial_delay is not None:
            self.timeout(self.initial_delay)

        # Acquire lock
        acquired = await self.acquire_lock()
        if not acquired:
            return

        # Simulate pause (GC, network delay, etc.)
        if self.pause_duration > 0:
            print(
                f"[{self.now:.1f}] {self.client_id}: Pausing for {self.pause_duration}s"
            )
            await self.timeout(self.pause_duration)
            print(f"[{self.now:.1f}] {self.client_id}: Resuming")

        # Try to access resource with our token
        success = await self.protected_resource.access(
            self.client_id, self.current_token, self.work_duration
        )

        if success:
            await self.release_lock()
    # mccole:/fenced_run

    # mccole:fenced_acquire
    async def acquire_lock(self) -> bool:
        """Acquire lock from server."""
        response_queue = Queue(self._env)
        request = LockRequest(
            client_id=self.client_id,
            resource=self.resource_name,
            operation="acquire",
            response_queue=response_queue,
        )

        await self.server.request_queue.put(request)
        response = await response_queue.get()

        if response.success:
            self.current_token = response.token
            print(
                f"[{self.now:.1f}] {self.client_id}: Acquired lock "
                f"(token {self.current_token})"
            )
            return True
        return False
    # mccole:/fenced_acquire

    # mccole:fenced_release
    async def release_lock(self):
        """Release lock."""
        response_queue = Queue(self._env)
        request = LockRequest(
            client_id=self.client_id,
            resource=self.resource_name,
            operation="release",
            response_queue=response_queue,
        )

        await self.server.request_queue.put(request)
        await response_queue.get()
    # mccole:/fenced_release
