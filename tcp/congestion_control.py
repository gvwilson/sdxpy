"""TCP congestion control: AIMD (Additive Increase, Multiplicative Decrease).

TCP uses the network itself as a signal: packet loss means congestion.
The sender tracks a *congestion window* (cwnd) that limits how many unacknowledged
segments can be in flight simultaneously.  Two mechanisms adjust cwnd:

  Slow Start:
      Begin with cwnd = 1 segment and double it every round-trip until loss
      is detected or a threshold (ssthresh) is crossed.  Despite the name,
      doubling is exponential—this phase is "slow" only compared to sending
      at full speed from the start.

  Congestion Avoidance:
      Once cwnd exceeds ssthresh, increase it by 1 segment per RTT (additive
      increase) rather than doubling.  This probes for additional capacity
      without overshooting.

  Multiplicative Decrease:
      When a segment is lost (timeout or three duplicate ACKs), cut cwnd in
      half and reduce ssthresh to the same value.  This backs off quickly.

Together these give AIMD (Additive Increase, Multiplicative Decrease), which
has been proven to converge to a fair share of bandwidth among competing flows.
"""

from dataclasses import dataclass
from asimpy import Process, Queue
from tcp_types import Packet, PacketType
from unreliable_network import UnreliableNetwork


# Minimum number of duplicate ACKs that triggers fast retransmit.
FAST_RETRANSMIT_THRESHOLD = 3


# mccole:cwnd_state
@dataclass
class CongestionState:
    """Congestion window state for one TCP sender.

    cwnd (congestion window):
        Maximum number of unacknowledged segments allowed.
    ssthresh (slow-start threshold):
        cwnd below this → slow start (exponential); above → congestion avoidance (linear).
    dup_ack_count:
        Number of consecutive duplicate ACKs for the same sequence number.
    """

    cwnd: float = 1.0          # Start with one segment
    ssthresh: float = 16.0     # Initial threshold (segments)
    dup_ack_count: int = 0
    last_acked_seq: int = -1

    def on_new_ack(self) -> None:
        """A new (non-duplicate) ACK arrived: increase cwnd."""
        self.dup_ack_count = 0
        if self.cwnd < self.ssthresh:
            # Slow start: double cwnd each RTT (approximately 1 per ACK).
            self.cwnd += 1.0
        else:
            # Congestion avoidance: increase by 1/cwnd per ACK ≈ +1 per RTT.
            self.cwnd += 1.0 / self.cwnd

    def on_duplicate_ack(self, seq: int) -> bool:
        """A duplicate ACK arrived.  Returns True if fast retransmit should fire."""
        if seq != self.last_acked_seq:
            self.dup_ack_count = 1
            self.last_acked_seq = seq
        else:
            self.dup_ack_count += 1
        return self.dup_ack_count >= FAST_RETRANSMIT_THRESHOLD

    def on_timeout(self) -> None:
        """Timeout detected: multiplicative decrease and restart slow start."""
        self.ssthresh = max(self.cwnd / 2.0, 2.0)
        self.cwnd = 1.0   # Back to slow start
        self.dup_ack_count = 0

    def on_fast_retransmit(self) -> None:
        """Three duplicate ACKs: less severe than timeout, so halve cwnd."""
        self.ssthresh = max(self.cwnd / 2.0, 2.0)
        self.cwnd = self.ssthresh   # Stay in congestion avoidance
        self.dup_ack_count = 0

    def effective_window(self, receiver_window: int) -> int:
        """Effective window is the min of cwnd and the receiver's advertised window."""
        return min(int(self.cwnd), receiver_window)
# mccole:/cwnd_state


# mccole:cc_sender
class CongestionControlledSender(Process):
    """TCP sender with AIMD congestion control.

    This class demonstrates how the congestion window interacts with the
    retransmission timer and fast-retransmit to dynamically adjust the
    sending rate.  It is intentionally separate from TCPConnection so
    the congestion-control logic is easy to read in isolation.
    """

    def init(
        self,
        sender_id: str,
        network: UnreliableNetwork,
        remote_addr: str,
        remote_port: int,
        data: list[str],
    ) -> None:
        self.sender_id = sender_id
        self.network = network
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.data = data

        self.local_addr = sender_id
        self.local_port = 9000

        # Register receive queue with the network.
        receive_queue: Queue = Queue(self._env)
        self.network.register(self.local_addr, self.local_port, receive_queue)
        self.receive_queue = receive_queue

        self.cong = CongestionState()
        self.next_seq: int = 0
        self.unacked: dict[int, str] = {}   # seq -> data
        self.ack_queue: Queue = Queue(self._env)

        # Statistics
        self.cwnd_history: list[tuple[float, float]] = []

    async def run(self) -> None:
        """Send all data, adapting window based on ACKs and losses."""
        for chunk in self.data:
            # Wait until the congestion window allows another segment in flight.
            while len(self.unacked) >= self.cong.effective_window(64):
                await self.timeout(0.05)

            seq = self.next_seq
            self.next_seq += 1
            self.unacked[seq] = chunk

            pkt = Packet(
                src_addr=self.local_addr,
                dst_addr=self.remote_addr,
                src_port=self.local_port,
                dst_port=self.remote_port,
                seq_num=seq,
                ack_num=0,
                packet_type=PacketType.DATA,
                data=chunk,
            )
            await self.network.send_packet(pkt)

            _TimeoutChecker(self._env, self, seq, chunk)

            self.cwnd_history.append((self.now, self.cong.cwnd))
            print(
                f"[{self.now:.2f}] {self.sender_id}: Sent seq={seq} "
                f"cwnd={self.cong.cwnd:.1f} in_flight={len(self.unacked)}"
            )

        # Wait for all ACKs.
        while self.unacked:
            await self.timeout(0.1)

        print(f"[{self.now:.2f}] {self.sender_id}: All data delivered.")

    def on_ack(self, ack_seq: int) -> None:
        """Called when an ACK arrives."""
        if ack_seq in self.unacked:
            del self.unacked[ack_seq]
            self.cong.on_new_ack()
            self.cong.last_acked_seq = ack_seq
            print(
                f"[{self.now:.2f}] {self.sender_id}: ACK seq={ack_seq} "
                f"cwnd={self.cong.cwnd:.1f}"
            )
        else:
            # Duplicate ACK.
            fire = self.cong.on_duplicate_ack(ack_seq)
            if fire:
                print(
                    f"[{self.now:.2f}] {self.sender_id}: "
                    f"3 dup ACKs for seq={ack_seq} — fast retransmit"
                )
                self.cong.on_fast_retransmit()
# mccole:/cc_sender


class _AckHandler(Process):
    """Continuously reads ACKs from the network and calls back the sender."""

    def init(self, sender: CongestionControlledSender) -> None:
        self.sender = sender

    async def run(self) -> None:
        while True:
            pkt = await self.sender.receive_queue.get()
            if pkt.packet_type == PacketType.ACK:
                self.sender.on_ack(pkt.ack_num)


class _TimeoutChecker(Process):
    """Fires after rto and performs multiplicative decrease if seq is still unacked."""

    RTO = 2.0   # Fixed retransmission timeout (seconds)

    def init(self, sender: CongestionControlledSender, seq: int, data: str) -> None:
        self.sender = sender
        self.seq = seq
        self.data = data

    async def run(self) -> None:
        await self.timeout(self.RTO)
        if self.seq in self.sender.unacked:
            print(
                f"[{self.now:.2f}] {self.sender.sender_id}: "
                f"TIMEOUT seq={self.seq} — cwnd halved"
            )
            self.sender.cong.on_timeout()
            # Retransmit.
            pkt = Packet(
                src_addr=self.sender.local_addr,
                dst_addr=self.sender.remote_addr,
                src_port=self.sender.local_port,
                dst_port=self.sender.remote_port,
                seq_num=self.seq,
                ack_num=0,
                packet_type=PacketType.DATA,
                data=self.data,
            )
            await self.sender.network.send_packet(pkt)
            # Restart timer.
            _TimeoutChecker(self._env, self.sender, self.seq, self.data)
