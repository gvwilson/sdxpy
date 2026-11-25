"""Grow-only counter (state-based CRDT)."""

from dataclasses import dataclass, field


# mccole:gcounter
@dataclass
class GCounter:
    """Grow-only counter (state-based CRDT)."""

    replica_id: str
    counts: dict[str, int] = field(default_factory=dict)

    def increment(self, amount: int = 1):
        """Increment this replica's counter."""
        current = self.counts.get(self.replica_id, 0)
        self.counts[self.replica_id] = current + amount

    def value(self) -> int:
        """Get the total count across all replicas."""
        return sum(self.counts.values())

    def merge(self, other: "GCounter"):
        """Merge another counter's state by taking the max of each replica."""
        all_replicas = set(self.counts.keys()) | set(other.counts.keys())
        for replica in all_replicas:
            self.counts[replica] = max(
                self.counts.get(replica, 0), other.counts.get(replica, 0)
            )

    def copy(self) -> "GCounter":
        """Create a copy of this counter."""
        return GCounter(replica_id=self.replica_id, counts=self.counts.copy())

    # mccole:/gcounter

    def __str__(self):
        return f"GCounter(id={self.replica_id}, value={self.value()}, counts={self.counts})"
