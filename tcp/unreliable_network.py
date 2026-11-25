"""Unreliable network layer simulating UDP-like behavior."""

from asimpy import Process, Queue
from typing import Dict
from tcp_types import Packet
import random


# mccole:network_init
class UnreliableNetwork(Process):
    """Simulates unreliable packet delivery (like UDP)."""

    def init(
        self,
        loss_rate: float = 0.1,
        reorder_rate: float = 0.05,
        duplicate_rate: float = 0.02,
        delay_range: tuple = (0.1, 0.5),
    ) -> None:
        self.loss_rate = loss_rate
        self.reorder_rate = reorder_rate
        self.duplicate_rate = duplicate_rate
        self.delay_range = delay_range

        # Network endpoints (address:port -> queue)
        self.endpoints: Dict[str, Queue] = {}

        # Statistics
        self.packets_sent = 0
        self.packets_lost = 0
        self.packets_reordered = 0
        self.packets_duplicated = 0

        print(
            f"[{self.now:.1f}] Network: Started (loss={loss_rate:.0%}, "
            f"reorder={reorder_rate:.0%})"
        )

    async def run(self) -> None:
        """Network doesn't have a main loop - just routes packets."""
        while True:
            await self.timeout(1000)  # Sleep forever

    def register_endpoint(self, address: str, port: int, queue: Queue) -> None:
        """Register an endpoint to receive packets."""
        endpoint_id = f"{address}:{port}"
        self.endpoints[endpoint_id] = queue
        print(f"[{self.now:.1f}] Network: Registered {endpoint_id}")
# mccole:/network_init

    # mccole:network_send
    async def send_packet(self, packet: Packet) -> None:
        """Send packet with simulated unreliability."""
        self.packets_sent += 1

        # Simulate packet loss
        if random.random() < self.loss_rate:
            self.packets_lost += 1
            print(f"[{self.now:.1f}] Network: LOST {packet}")
            return

        # Simulate packet duplication
        if random.random() < self.duplicate_rate:
            self.packets_duplicated += 1
            print(f"[{self.now:.1f}] Network: DUPLICATING {packet}")
            await self._deliver_packet(packet)

        # Deliver the packet
        await self._deliver_packet(packet)

    async def _deliver_packet(self, packet: Packet) -> None:
        """Deliver packet to destination."""
        # Simulate network delay
        delay = random.uniform(*self.delay_range)

        # Simulate reordering by adding extra random delay
        if random.random() < self.reorder_rate:
            self.packets_reordered += 1
            delay += random.uniform(0.2, 0.8)

        await self.timeout(delay)

        # Find destination endpoint
        endpoint_id = f"{packet.dst_addr}:{packet.dst_port}"
        if endpoint_id in self.endpoints:
            await self.endpoints[endpoint_id].put(packet)
        else:
            print(f"[{self.now:.1f}] Network: No endpoint for {endpoint_id}")
    # mccole:/network_send

    def print_statistics(self) -> None:
        """Print network statistics."""
        print("### Network Statistics:")
        print(f"Packets sent: {self.packets_sent}")
        print(
            f"Packets lost: {self.packets_lost} "
            f"({100 * self.packets_lost / max(self.packets_sent, 1):.1f}%)"
        )
        print(f"Packets reordered: {self.packets_reordered}")
        print(f"Packets duplicated: {self.packets_duplicated}")
