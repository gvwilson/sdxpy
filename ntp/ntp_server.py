from asimpy import Process, Queue


# mccole:ntpserver
class NTPServer(Process):
    """An NTP time server that responds to client requests."""

    def init(
        self,
        name: str,
        stratum: int,
        request_queue: Queue,
        network_delay: float = 0.1,
    ):
        self.name = name
        self.stratum = stratum
        self.request_queue = request_queue
        self.network_delay = network_delay
        self.requests_served = 0

    async def run(self):
        """Process incoming NTP requests."""
        while True:
            # Wait for a request
            client_queue, message = await self.request_queue.get()

            # Record server receive time (t2)
            message.t2 = self.now

            # Simulate processing time
            await self.timeout(0.001)

            # Record server transmit time (t3)
            message.t3 = self.now
            message.stratum = self.stratum

            print(
                f"[{self.now:.3f}] {self.name} (stratum {self.stratum}): "
                f"Responding to request (t2={message.t2:.3f}, t3={message.t3:.3f})"
            )

            # Send response back to client with network delay
            await self.timeout(self.network_delay)
            await client_queue.put(message)

            self.requests_served += 1
# mccole:/ntpserver
