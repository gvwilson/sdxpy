"""Required behavior of cache index."""

from abc import ABC, abstractmethod
from collections import namedtuple
import datetime


CacheEntry = namedtuple("CacheEntry", ["identifier", "timestamp"])


class IndexBase(ABC):
    """Define operations on cache index."""

    def __init__(self):
        """Initialize."""
        self.local_dir = None

    def set_local_dir(self, local_dir):
        """Specify local directory."""
        self.local_dir = local_dir

    def has(self, identifier):
        """Is the identifier present in the index?"""
        index = self.load()
        return any(entry.id == identifier for entry in index)

    def least_recently_used(self):
        """Return all items, least-recently-used first."""
        index = self.load()
        index.sort(key=lambda x: x.modified)

    def add(self, identifier):
        """Add a record to the index."""
        index = self.load()
        entry = CacheEntry(identifier, current_time())
        index.append(entry)
        self.save(index)

    @abstractmethod
    def load(self):
        """Load entire index."""

    @abstractmethod
    def save(self, index):
        """Save entire index."""


def current_time():
    """Get time (separate to make mocking easier)."""
    return str(datetime.datetime.now())
