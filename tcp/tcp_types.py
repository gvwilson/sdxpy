"""Data types for TCP over UDP implementation."""

from dataclasses import dataclass, field
from enum import Enum


# mccole:packettypes
class PacketType(Enum):
    """Types of TCP packets."""

    SYN = "SYN"  # Synchronize (connection establishment)
    SYN_ACK = "SYN_ACK"  # Synchronize-Acknowledge
    ACK = "ACK"  # Acknowledge
    DATA = "DATA"  # Data packet
    FIN = "FIN"  # Finish (connection teardown)
    FIN_ACK = "FIN_ACK"  # Finish-Acknowledge
# mccole:/packettypes


# mccole:connectionstate
class ConnectionState(Enum):
    """TCP connection states."""

    CLOSED = "CLOSED"
    SYN_SENT = "SYN_SENT"
    SYN_RECEIVED = "SYN_RECEIVED"
    ESTABLISHED = "ESTABLISHED"
    FIN_WAIT = "FIN_WAIT"
    CLOSE_WAIT = "CLOSE_WAIT"
    CLOSING = "CLOSING"
# mccole:/connectionstate


# mccole:packet
@dataclass
class Packet:
    """A network packet (simulating IP + TCP)."""

    src_addr: str
    src_port: int
    dst_addr: str | None
    dst_port: int | None
    seq_num: int
    ack_num: int
    packet_type: PacketType
    data: bytes = b""
    window_size: int = 65535
# mccole:/packet

    def __str__(self) -> str:
        data_len = len(self.data)
        return (
            f"Packet({self.packet_type.value}, seq={self.seq_num}, "
            f"ack={self.ack_num}, len={data_len})"
        )


@dataclass
class SegmentBuffer:
    """Buffer for sent but unacknowledged segments."""

    seq_num: int
    data: bytes
    sent_time: float
    retransmit_count: int = 0

    def __str__(self) -> str:
        return f"Segment(seq={self.seq_num}, len={len(self.data)})"


# mccole:receivebuffer
@dataclass
class ReceiveBuffer:
    """Buffer for out-of-order received segments."""

    segments: dict[int, bytes] = field(default_factory=dict)
    next_expected_seq: int = 0

    def add_segment(self, seq_num: int, data: bytes) -> None:
        """Add a segment to the receive buffer."""
        if seq_num >= self.next_expected_seq:
            self.segments[seq_num] = data

    def get_continuous_data(self) -> bytes:
        """Extract continuous data starting from next_expected_seq."""
        result = b""
        current_seq = self.next_expected_seq

        while current_seq in self.segments:
            segment = self.segments.pop(current_seq)
            result += segment
            current_seq += len(segment)

        if result:
            self.next_expected_seq = current_seq

        return result

    def has_data(self) -> bool:
        """Check if buffer has any segments."""
        return len(self.segments) > 0
# mccole:/receivebuffer
