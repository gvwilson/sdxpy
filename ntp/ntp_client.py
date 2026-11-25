from asimpy import Process, Queue
from ntp_message import NTPMessage


# mccole:client_init
class NTPClient(Process):
    """An NTP client that synchronizes its clock with a server."""

    def init(
        self,
        name: str,
        server_queue: Queue,
        sync_interval: float,
        network_delay: float = 0.1,
        initial_offset: float = 0.0,
    ):
        self.name = name
        self.server_queue = server_queue
        self.sync_interval = sync_interval
        self.network_delay = network_delay

        # Client's local clock offset from true time
        self.clock_offset = initial_offset
        self.response_queue = Queue(self._env)

        # Statistics
        self.syncs_performed = 0
        self.offset_history = []

    def get_local_time(self) -> float:
        """Get current time according to client's local clock."""
        return self.now + self.clock_offset
# mccole:/client_init

    # mccole:client_run
    async def run(self):
        """Periodically sync with NTP server."""
        while True:
            # Wait for sync interval
            await self.timeout(self.sync_interval)

            # Perform NTP sync
            await self._sync_with_server()
    # mccole:/client_run

    # mccole:client_sync
    async def _sync_with_server(self):
        """Execute one NTP synchronization cycle."""
        # Create request message with client send time (t1)
        message = NTPMessage(t1=self.get_local_time())

        print(
            f"[{self.now:.3f}] {self.name}: Sending sync request "
            f"(local_time={message.t1:.3f}, offset={self.clock_offset:.3f})"
        )

        # Send request with network delay
        await self.timeout(self.network_delay)
        await self.server_queue.put((self.response_queue, message))

        # Wait for response
        response = await self.response_queue.get()

        # Record client receive time (t4)
        response.t4 = self.get_local_time()

        # Calculate offset and delay
        offset = response.calculate_offset()
        delay = response.calculate_delay()

        print(
            f"[{self.now:.3f}] {self.name}: Received response "
            f"(offset={offset:.3f}, delay={delay:.3f})"
        )

        # Adjust clock by the calculated offset
        self.clock_offset -= offset
        self.syncs_performed += 1
        self.offset_history.append(abs(offset))

        print(
            f"[{self.now:.3f}] {self.name}: Clock adjusted, "
            f"new offset from true time: {self.clock_offset:.3f}"
        )
    # mccole:/client_sync
