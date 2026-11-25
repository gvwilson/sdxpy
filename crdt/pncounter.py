"""Positive-Negative counter (state-based CRDT)."""

from dataclasses import dataclass, field
from gcounter import GCounter


# mccole:pncounter
@dataclass
class PNCounter:
    """Positive-Negative counter supporting increment and decrement."""

    replica_id: str
    increments: GCounter = field(default_factory=lambda: GCounter(""))
    decrements: GCounter = field(default_factory=lambda: GCounter(""))

    def __post_init__(self):
        self.increments.replica_id = self.replica_id
        self.decrements.replica_id = self.replica_id

    def increment(self, amount: int = 1):
        """Increment the counter."""
        self.increments.increment(amount)

    def decrement(self, amount: int = 1):
        """Decrement the counter."""
        self.decrements.increment(amount)

    def value(self) -> int:
        """Get the current value (increments - decrements)."""
        return self.increments.value() - self.decrements.value()

    def merge(self, other: "PNCounter"):
        """Merge another counter's state."""
        self.increments.merge(other.increments)
        self.decrements.merge(other.decrements)

    def copy(self) -> "PNCounter":
        """Create a copy of this counter."""
        result = PNCounter(self.replica_id)
        result.increments = self.increments.copy()
        result.decrements = self.decrements.copy()
        return result

    # mccole:/pncounter

    def __str__(self):
        return f"PNCounter(id={self.replica_id}, value={self.value()})"
