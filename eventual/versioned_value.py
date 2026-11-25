"""Versioned value with vector clock."""

from dataclasses import dataclass
from typing import Any
from vector_clock import VectorClock


# mccole:versionedvalue
@dataclass
class VersionedValue:
    """A value with its vector clock."""

    value: Any
    clock: VectorClock
    timestamp: float  # For last-write-wins conflict resolution
# mccole:/versionedvalue

    def __str__(self):
        return f"Value({self.value}, {self.clock})"
