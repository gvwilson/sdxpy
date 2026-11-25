from asimpy import Environment, Queue, Process
from ntp_server import NTPServer
from ntp_client import NTPClient
from ntp_message import NTPMessage
from dsdx import dsdx


# mccole:stratumserver
class StratumServerProcess(Process):
    """Server process for a stratum N+1 NTP server."""

    def init(
        self,
        name: str,
        local_queue: Queue,
        stratum: int,
        clock_state: dict,
        network_delay: float = 0.1,
    ):
        self.name = name
        self.local_queue = local_queue
        self.stratum = stratum
        self.clock_state = clock_state  # Shared with client process
        self.network_delay = network_delay

    def get_local_time(self) -> float:
        """Get current time according to local clock."""
        return self.now + self.clock_state["offset"]

    async def run(self):
        """Serve requests from downstream clients."""
        while True:
            client_queue, message = await self.local_queue.get()

            # Record timestamps
            message.t2 = self.get_local_time()
            await self.timeout(0.001)
            message.t3 = self.get_local_time()
            message.stratum = self.stratum

            # Send response
            await self.timeout(self.network_delay)
            await client_queue.put(message)
# mccole:/stratumserver


# mccole:stratumclient
class StratumClientProcess(Process):
    """Client process for a stratum N+1 NTP server."""

    def init(
        self,
        name: str,
        upstream_queue: Queue,
        stratum: int,
        clock_state: dict,
        sync_interval: float,
        network_delay: float = 0.1,
    ):
        self.name = name
        self.upstream_queue = upstream_queue
        self.stratum = stratum
        self.clock_state = clock_state  # Shared with server process
        self.sync_interval = sync_interval
        self.network_delay = network_delay
        self.response_queue = Queue(self._env)

    def get_local_time(self) -> float:
        """Get current time according to local clock."""
        return self.now + self.clock_state["offset"]

    async def run(self):
        """Sync with upstream server."""
        while True:
            await self.timeout(self.sync_interval)

            # Send request to upstream
            message = NTPMessage(t1=self.get_local_time())
            await self.timeout(self.network_delay)
            await self.upstream_queue.put((self.response_queue, message))

            # Wait for response
            response = await self.response_queue.get()
            response.t4 = self.get_local_time()

            # Adjust clock (updates shared state)
            offset = response.calculate_offset()
            self.clock_state["offset"] -= offset

            print(
                f"[{self.now:.3f}] {self.name} (stratum {self.stratum}): "
                f"Synced with upstream, offset={offset:.3f}"
            )
# mccole:/stratumclient


# mccole:hierarchy
def main():
    """Demonstrate NTP stratum hierarchy."""
    env = Environment()

    # Stratum 1: Primary time server
    s1_queue = Queue(env)
    stratum1 = NTPServer(env, "stratum1.time.gov", stratum=1, request_queue=s1_queue)

    # Stratum 2: Secondary servers syncing with stratum 1
    # Each stratum 2 server has both client and server processes
    s2a_queue = Queue(env)
    s2a_clock = {"offset": 0.0}  # Shared clock state
    StratumClientProcess(
        env,
        "stratum2a.org",
        s1_queue,
        stratum=2,
        clock_state=s2a_clock,
        sync_interval=10.0,
    )
    StratumServerProcess(
        env, "stratum2a.org", s2a_queue, stratum=2, clock_state=s2a_clock
    )

    s2b_queue = Queue(env)
    s2b_clock = {"offset": 0.0}  # Shared clock state
    StratumClientProcess(
        env,
        "stratum2b.org",
        s1_queue,
        stratum=2,
        clock_state=s2b_clock,
        sync_interval=10.0,
    )
    StratumServerProcess(
        env, "stratum2b.org", s2b_queue, stratum=2, clock_state=s2b_clock
    )

    # Stratum 3: End clients
    client_a = NTPClient(
        env, "client_a", s2a_queue, sync_interval=5.0, initial_offset=3.0
    )

    client_b = NTPClient(
        env, "client_b", s2b_queue, sync_interval=5.0, initial_offset=-2.0
    )

    # Run simulation
    env.run(until=35)

    print("\n=== Stratum Hierarchy Results ===")
    print(f"Stratum 1 server requests: {stratum1.requests_served}")
    print(f"\nStratum 2a clock offset: {s2a_clock['offset']:.6f}s")
    print(f"Stratum 2b clock offset: {s2b_clock['offset']:.6f}s")
    print(f"\nClient A final offset: {client_a.clock_offset:.6f}s")
    print(f"Client B final offset: {client_b.clock_offset:.6f}s")
# mccole:/hierarchy


if __name__ == "__main__":
    dsdx(main)
