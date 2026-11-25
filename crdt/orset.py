"""Observed-Remove Set (state-based CRDT)."""

from dataclasses import dataclass, field
from typing import Any


# mccole:orset
@dataclass
class ORSet:
    """Observed-Remove Set (state-based CRDT)."""

    replica_id: str
    elements: dict[Any, set[str]] = field(
        default_factory=dict
    )  # element -> set of unique tags
    tag_counter: int = 0

    def add(self, element: Any) -> str:
        """Add an element with a unique tag."""
        self.tag_counter += 1
        tag = f"{self.replica_id}-{self.tag_counter}"
        if element not in self.elements:
            self.elements[element] = set()
        self.elements[element].add(tag)
        return tag

    def remove(self, element: Any):
        """Remove an element (removes all observed tags)."""
        if element in self.elements:
            del self.elements[element]

    def contains(self, element: Any) -> bool:
        """Check if element is in the set."""
        return element in self.elements and len(self.elements[element]) > 0

    def value(self) -> set[Any]:
        """Get the current set of elements."""
        return {elem for elem, tags in self.elements.items() if tags}

    def merge(self, other: "ORSet"):
        """Merge another set's state."""
        # Union of all tags for each element
        all_elements = set(self.elements.keys()) | set(other.elements.keys())

        for element in all_elements:
            self_tags = self.elements.get(element, set())
            other_tags = other.elements.get(element, set())
            merged_tags = self_tags | other_tags
            if merged_tags:
                self.elements[element] = merged_tags

    def copy(self) -> "ORSet":
        """Create a copy of this set."""
        result = ORSet(self.replica_id)
        result.elements = {k: v.copy() for k, v in self.elements.items()}
        result.tag_counter = self.tag_counter
        return result

    # mccole:/orset

    def __str__(self):
        return f"ORSet(id={self.replica_id}, value={self.value()})"
