"""Vector clock for tracking causality in distributed systems."""

from dataclasses import dataclass, field


# mccole:vectorclock
@dataclass
class VectorClock:
    """Vector clock for tracking causality."""

    clocks: dict[str, int] = field(default_factory=dict)

    def increment(self, replica_id: str):
        """Increment the clock for a replica."""
        self.clocks[replica_id] = self.clocks.get(replica_id, 0) + 1

    def merge(self, other: "VectorClock"):
        """Merge with another vector clock (take max of each component)."""
        all_replicas = set(self.clocks.keys()) | set(other.clocks.keys())
        for replica in all_replicas:
            self.clocks[replica] = max(
                self.clocks.get(replica, 0), other.clocks.get(replica, 0)
            )

    def happens_before(self, other: "VectorClock") -> bool:
        """Check if this clock happens before another."""
        # self <= other and self != other
        all_replicas = set(self.clocks.keys()) | set(other.clocks.keys())

        at_least_one_less = False
        for replica in all_replicas:
            self_val = self.clocks.get(replica, 0)
            other_val = other.clocks.get(replica, 0)

            if self_val > other_val:
                return False
            if self_val < other_val:
                at_least_one_less = True

        return at_least_one_less

    def concurrent_with(self, other: "VectorClock") -> bool:
        """Check if this clock is concurrent with another."""
        return not self.happens_before(other) and not other.happens_before(self)

    def copy(self) -> "VectorClock":
        """Create a copy of this vector clock."""
        return VectorClock(clocks=self.clocks.copy())
# mccole:/vectorclock

    def __str__(self):
        items = sorted(self.clocks.items())
        return "{" + ", ".join(f"{k}:{v}" for k, v in items) + "}"
