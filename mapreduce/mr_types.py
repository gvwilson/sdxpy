"""Core data structures for MapReduce framework."""

from collections import defaultdict
from dataclasses import dataclass, field
import hashlib
from typing import Any


# mccole:map
@dataclass
class MapTask:
    """A map task to be executed."""

    task_id: str
    data: list[Any]
    # mccole:/map

    def __str__(self):
        return f"MapTask({self.task_id})"


# mccole:intermediate
@dataclass
class IntermediateData:
    """Intermediate key-value pairs from map phase."""

    pairs: list[tuple[Any, Any]] = field(default_factory=list)

    def add(self, key: Any, value: Any):
        """Add a key-value pair."""
        self.pairs.append((key, value))

    def partition(self, num_partitions: int) -> list["IntermediateData"]:
        """Partition by key hash."""
        partitions = [IntermediateData() for _ in range(num_partitions)]
        for key, value in self.pairs:
            partition_id = _stable_hash(key) % num_partitions
            partitions[partition_id].add(key, value)

        return partitions

    def group_by_key(self) -> dict[Any, list[Any]]:
        """Group values by key."""
        grouped = defaultdict(list)
        for key, value in self.pairs:
            grouped[key].append(value)
        return dict(grouped)


# mccole:/intermediate


# mccole:reduce
@dataclass
class ReduceTask:
    """A reduce task to be executed."""

    task_id: str
    partition_id: int
    keys: list[Any]  # Keys this reducer is responsible for
    # mccole:/reduce

    def __str__(self):
        return f"ReduceTask({self.task_id}, partition={self.partition_id})"


# mccole:hash
def _stable_hash(key: Any) -> int:
    """Deterministic hash (not affected by PYTHONHASHSEED)."""

    return int(hashlib.md5(str(key).encode()).hexdigest(), 16)


# mccole:/hash
