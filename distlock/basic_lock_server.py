# basic_lock_server.py
"""Basic lock server with lease-based locking."""

from asimpy import Process, Queue
from dataclasses import dataclass, field


# mccole:lockclasses
@dataclass
class LockRequest:
    """Request to acquire or release a lock."""

    client_id: str
    resource: str
    operation: str  # "acquire" or "release"
    response_queue: Queue


@dataclass
class LockResponse:
    """Response to a lock request."""

    success: bool
    token: int | None = None
    message: str = ""


@dataclass
class LockState:
    """State of a single lock."""

    holder: str | None = None
    token: int = 0
    lease_expiry: float = 0
    waiters: list = field(default_factory=list)
# mccole:/lockclasses


# mccole:server_init
class LockServer(Process):
    """A single lock server managing multiple resources."""

    def init(self, name: str, lease_duration: float = 5.0):
        self.name = name
        self.lease_duration = lease_duration
        self.request_queue = Queue(self._env)
        self.locks: dict[str, LockState] = {}
        self.next_token = 1

    async def run(self):
        """Process lock requests."""
        while True:
            request = await self.request_queue.get()

            if request.operation == "acquire":
                response = await self._handle_acquire(request)
            elif request.operation == "release":
                response = await self._handle_release(request)
            else:
                response = LockResponse(False, message="Unknown operation")

            await request.response_queue.put(response)
    # mccole:/server_init

    # mccole:handle_acquire
    async def _handle_acquire(self, request: LockRequest) -> LockResponse:
        """Try to acquire a lock."""
        resource = request.resource

        # Create lock state if needed
        if resource not in self.locks:
            self.locks[resource] = LockState()

        lock = self.locks[resource]

        # Check if lock is expired
        if lock.holder and self.now >= lock.lease_expiry:
            print(
                f"[{self.now:.1f}] {self.name}: Lock on {resource} "
                f"expired (was held by {lock.holder})"
            )
            lock.holder = None

        # Try to acquire
        if lock.holder is None:
            lock.holder = request.client_id
            lock.token = self.next_token
            self.next_token += 1
            lock.lease_expiry = self.now + self.lease_duration

            print(
                f"[{self.now:.1f}] {self.name}: Granted lock on {resource} "
                f"to {request.client_id} (token {lock.token})"
            )

            return LockResponse(True, token=lock.token)

        elif lock.holder == request.client_id:
            # Renew lease for current holder
            lock.lease_expiry = self.now + self.lease_duration
            print(
                f"[{self.now:.1f}] {self.name}: Renewed lease on {resource} "
                f"for {request.client_id}"
            )
            return LockResponse(True, token=lock.token)

        else:
            # Lock is held by someone else
            return LockResponse(False, message=f"Lock held by {lock.holder}")
    # mccole:/handle_acquire

    # mccole:handle_release
    async def _handle_release(self, request: LockRequest) -> LockResponse:
        """Release a lock."""
        resource = request.resource

        if resource not in self.locks:
            return LockResponse(False, message="Lock not found")

        lock = self.locks[resource]

        if lock.holder == request.client_id:
            print(
                f"[{self.now:.1f}] {self.name}: Released lock on {resource} "
                f"by {request.client_id}"
            )
            lock.holder = None
            return LockResponse(True)
        else:
            return LockResponse(False, message=f"Lock not held by {request.client_id}")
    # mccole:/handle_release
