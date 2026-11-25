"""Last-Write-Wins register (state-based CRDT)."""

from dataclasses import dataclass
from typing import Any


# mccole:lww
@dataclass
class LWWRegister:
    """Last-Write-Wins register (state-based CRDT)."""

    value: Any = None
    timestamp: float = 0.0
    replica_id: str = ""

    def set(self, value: Any, timestamp: float, replica_id: str):
        """Set the value with a timestamp."""
        # Use timestamp to break ties, replica_id for determinism
        if timestamp > self.timestamp or (
            timestamp == self.timestamp and replica_id > self.replica_id
        ):
            self.value = value
            self.timestamp = timestamp
            self.replica_id = replica_id

    def merge(self, other: "LWWRegister"):
        """Merge another register (keep higher timestamp)."""
        if other.timestamp > self.timestamp or (
            other.timestamp == self.timestamp and other.replica_id > self.replica_id
        ):
            self.value = other.value
            self.timestamp = other.timestamp
            self.replica_id = other.replica_id

    # mccole:/lww

    def copy(self) -> "LWWRegister":
        """Create a copy of this register."""
        return LWWRegister(
            value=self.value, timestamp=self.timestamp, replica_id=self.replica_id
        )

    def __str__(self):
        return f"LWWRegister(value={self.value}, ts={self.timestamp:.2f})"
