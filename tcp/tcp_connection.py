"""TCP connection implementation with reliability over unreliable network."""

from asimpy import Process, Queue
from typing import TYPE_CHECKING
from tcp_types import Packet, PacketType, ConnectionState, SegmentBuffer, ReceiveBuffer
import random

if TYPE_CHECKING:
    from unreliable_network import UnreliableNetwork


# mccole:retransmission
class RetransmissionTimer(Process):
    """Timer process for retransmitting unacknowledged segments."""

    def init(self, connection: "TCPConnection", segment: SegmentBuffer) -> None:
        self.connection = connection
        self.segment = segment

    async def run(self) -> None:
        """Wait for timeout, then retransmit if not acknowledged."""
        await self.timeout(self.connection.rto)

        # Check if still in send buffer (not yet acknowledged)
        if self.segment in self.connection.send_buffer:
            print(
                f"[{self.now:.1f}] TCP: TIMEOUT - Retransmitting "
                f"seq={self.segment.seq_num}"
            )

            self.connection.packets_retransmitted += 1
            self.segment.retransmit_count += 1
            self.segment.sent_time = self.now

            # Retransmit
            packet = Packet(
                src_addr=self.connection.local_addr,
                dst_addr=self.connection.remote_addr,
                src_port=self.connection.local_port,
                dst_port=self.connection.remote_port,
                seq_num=self.segment.seq_num,
                ack_num=self.connection.recv_buffer.next_expected_seq,
                packet_type=PacketType.DATA,
                data=self.segment.data,
            )

            await self.connection.network.send_packet(packet)

            # Restart timer
            RetransmissionTimer(self._env, self.connection, self.segment)
# mccole:/retransmission


# mccole:tcpinit
class TCPConnection(Process):
    """TCP connection with reliability over unreliable network."""

    def init(
        self,
        local_addr: str,
        local_port: int,
        network: "UnreliableNetwork",
        mtu: int = 1400,
        window_size: int = 4,
        timeout: float = 2.0,
    ) -> None:
        self.local_addr = local_addr
        self.local_port = local_port
        self.network = network
        self.mtu = mtu  # Maximum transmission unit
        self.window_size = window_size  # Sliding window size
        self.rto = timeout  # Retransmission timeout

        # Connection state
        self.state = ConnectionState.CLOSED
        self.remote_addr: str | None = None
        self.remote_port: int | None = None

        # Sequence numbers
        self.send_seq = random.randint(1000, 9999)  # Initial sequence number
        self.recv_seq = 0

        # Send buffer
        self.send_buffer: list[SegmentBuffer] = []
        self.send_base = self.send_seq  # Oldest unacknowledged sequence
        self.next_seq_num = self.send_seq  # Next sequence to use

        # Receive buffer
        self.recv_buffer = ReceiveBuffer()

        # Queues
        self.recv_queue: Queue = Queue(self._env)  # Incoming packets
        self.data_ready: Queue = Queue(self._env)  # Data for application

        # Register with network
        network.register_endpoint(local_addr, local_port, self.recv_queue)

        # Statistics
        self.bytes_sent = 0
        self.bytes_received = 0
        self.packets_retransmitted = 0

        print(
            f"[{self.now:.1f}] TCP {self.local_addr}:{self.local_port}: "
            f"Created (ISN={self.send_seq})"
        )
# mccole:/tcpinit

    # mccole:tcp_run
    async def run(self) -> None:
        """Main TCP loop: handle incoming packets."""
        while True:
            packet = await self.recv_queue.get()
            await self.handle_packet(packet)

    async def handle_packet(self, packet: Packet) -> None:
        """Process incoming packet based on type."""
        if packet.packet_type == PacketType.SYN:
            await self.handle_syn(packet)

        elif packet.packet_type == PacketType.SYN_ACK:
            print(
                f"[{self.now:.1f}] TCP: Received SYN-ACK "
                f"(seq={packet.seq_num}, ack={packet.ack_num})"
            )

            self.recv_seq = packet.seq_num + 1
            self.recv_buffer.next_expected_seq = self.recv_seq
            self.send_base = packet.ack_num

            # Send final ACK
            ack = Packet(
                src_addr=self.local_addr,
                dst_addr=packet.src_addr,
                src_port=self.local_port,
                dst_port=packet.src_port,
                seq_num=self.send_base,
                ack_num=self.recv_seq,
                packet_type=PacketType.ACK,
            )

            await self.network.send_packet(ack)
            self.state = ConnectionState.ESTABLISHED
            print(f"[{self.now:.1f}] TCP: Sent ACK, connection established")

        elif packet.packet_type == PacketType.ACK:
            if self.state == ConnectionState.SYN_RECEIVED:
                print(
                    f"[{self.now:.1f}] TCP: Received final ACK, connection established"
                )
                self.state = ConnectionState.ESTABLISHED
            else:
                await self.handle_ack(packet)

        elif packet.packet_type == PacketType.DATA:
            await self.handle_data(packet)
    # mccole:/tcp_run

    # mccole:tcpconnect
    async def connect(self, remote_addr: str, remote_port: int) -> bool:
        """Initiate TCP connection (3-way handshake)."""
        self.remote_addr = remote_addr
        self.remote_port = remote_port

        print(
            f"\n[{self.now:.1f}] TCP: Starting connection to "
            f"{remote_addr}:{remote_port}"
        )

        # Send SYN
        self.state = ConnectionState.SYN_SENT
        syn = Packet(
            src_addr=self.local_addr,
            dst_addr=remote_addr,
            src_port=self.local_port,
            dst_port=remote_port,
            seq_num=self.send_seq,
            ack_num=0,
            packet_type=PacketType.SYN,
        )

        await self.network.send_packet(syn)
        print(f"[{self.now:.1f}] TCP: Sent SYN (seq={self.send_seq})")

        # Wait for SYN-ACK with timeout
        timeout_time = self.now + 5.0
        while self.state != ConnectionState.ESTABLISHED and self.now < timeout_time:
            await self.timeout(0.1)

        if self.state == ConnectionState.ESTABLISHED:
            print(f"[{self.now:.1f}] TCP: Connection ESTABLISHED\n")
            return True
        else:
            print(f"[{self.now:.1f}] TCP: Connection FAILED (timeout)\n")
            self.state = ConnectionState.CLOSED
            return False
    # mccole:/tcpconnect

    # mccole:server_accept
    async def listen_and_accept(self) -> bool:
        """Listen for incoming connection (server side)."""
        print(f"[{self.now:.1f}] TCP {self.local_addr}:{self.local_port}: Listening...")

        # Wait for SYN
        while True:
            packet = await self.recv_queue.get()
            if packet.packet_type == PacketType.SYN:
                await self.handle_syn(packet)
                break

        # Wait for final ACK
        timeout_time = self.now + 5.0
        while self.state != ConnectionState.ESTABLISHED and self.now < timeout_time:
            await self.timeout(0.1)

        return self.state == ConnectionState.ESTABLISHED

    async def handle_syn(self, packet: Packet) -> None:
        """Handle incoming SYN."""
        print(
            f"[{self.now:.1f}] TCP: Received SYN from "
            f"{packet.src_addr}:{packet.src_port}"
        )

        self.remote_addr = packet.src_addr
        self.remote_port = packet.src_port
        self.recv_seq = packet.seq_num + 1
        self.recv_buffer.next_expected_seq = self.recv_seq

        # Send SYN-ACK
        self.state = ConnectionState.SYN_RECEIVED
        syn_ack = Packet(
            src_addr=self.local_addr,
            dst_addr=packet.src_addr,
            src_port=self.local_port,
            dst_port=packet.src_port,
            seq_num=self.send_seq,
            ack_num=self.recv_seq,
            packet_type=PacketType.SYN_ACK,
        )

        await self.network.send_packet(syn_ack)
        print(
            f"[{self.now:.1f}] TCP: Sent SYN-ACK (seq={self.send_seq}, "
            f"ack={self.recv_seq})"
        )
    # mccole:/server_accept

    # mccole:handleack
    async def handle_ack(self, packet: Packet) -> None:
        """Handle ACK packet."""
        ack_num = packet.ack_num

        # Remove acknowledged segments from send buffer
        acknowledged = []
        for seg in self.send_buffer[:]:
            if seg.seq_num < ack_num:
                acknowledged.append(seg)
                self.send_buffer.remove(seg)

        if acknowledged:
            self.send_base = ack_num
            print(
                f"[{self.now:.1f}] TCP: ACK {ack_num} "
                f"(acknowledged {len(acknowledged)} segments)"
            )
    # mccole:/handleack

    # mccole:handle_data
    async def handle_data(self, packet: Packet) -> None:
        """Handle DATA packet."""
        seq_num = packet.seq_num
        data = packet.data

        print(f"[{self.now:.1f}] TCP: Received DATA (seq={seq_num}, len={len(data)})")

        # Add to receive buffer
        self.recv_buffer.add_segment(seq_num, data)

        # Extract continuous data
        continuous_data = self.recv_buffer.get_continuous_data()
        if continuous_data:
            self.bytes_received += len(continuous_data)
            await self.data_ready.put(continuous_data)
            print(
                f"[{self.now:.1f}] TCP: Delivered {len(continuous_data)} "
                f"bytes to application"
            )

        # Send ACK
        ack = Packet(
            src_addr=self.local_addr,
            dst_addr=packet.src_addr,
            src_port=self.local_port,
            dst_port=packet.src_port,
            seq_num=self.next_seq_num,
            ack_num=self.recv_buffer.next_expected_seq,
            packet_type=PacketType.ACK,
        )

        await self.network.send_packet(ack)
        print(
            f"[{self.now:.1f}] TCP: Sent ACK (ack={self.recv_buffer.next_expected_seq})"
        )
    # mccole:/handle_data

    # mccole:tcpsend
    async def send(self, data: bytes) -> None:
        """Send data reliably using TCP."""
        if self.state != ConnectionState.ESTABLISHED:
            print(f"[{self.now:.1f}] TCP: Cannot send - not connected")
            return

        # Split data into segments (respecting MTU)
        offset = 0
        while offset < len(data):
            chunk = data[offset : offset + self.mtu]

            # Wait if send window is full
            while len(self.send_buffer) >= self.window_size:
                await self.timeout(0.1)

            # Create and send segment
            seq_num = self.next_seq_num
            segment = Packet(
                src_addr=self.local_addr,
                dst_addr=self.remote_addr,
                src_port=self.local_port,
                dst_port=self.remote_port,
                seq_num=seq_num,
                ack_num=self.recv_buffer.next_expected_seq,
                packet_type=PacketType.DATA,
                data=chunk,
            )

            await self.network.send_packet(segment)

            # Add to send buffer for potential retransmission
            buffer_entry = SegmentBuffer(
                seq_num=seq_num, data=chunk, sent_time=self.now
            )
            self.send_buffer.append(buffer_entry)

            self.next_seq_num += len(chunk)
            self.bytes_sent += len(chunk)

            print(f"[{self.now:.1f}] TCP: Sent DATA (seq={seq_num}, len={len(chunk)})")

            # Start retransmission timer for this segment
            RetransmissionTimer(self._env, self, buffer_entry)

            offset += len(chunk)
    # mccole:/tcpsend

    async def receive(self) -> bytes:
        """Receive data from connection."""
        return await self.data_ready.get()

    def print_statistics(self) -> None:
        """Print connection statistics."""
        print(f"### TCP Connection Statistics ({self.local_addr}:{self.local_port}):")
        print(f"Bytes sent: {self.bytes_sent}")
        print(f"Bytes received: {self.bytes_received}")
        print(f"Packets retransmitted: {self.packets_retransmitted}")
        print(f"Send buffer size: {len(self.send_buffer)}")
