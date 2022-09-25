"""Required behavior of cache index."""

import datetime
from abc import ABC, abstractmethod
from collections import namedtuple

CacheEntry = namedtuple("CacheEntry", ["identifier", "timestamp"])


class IndexBase(ABC):
    """Define operations on cache index."""

    TIME_FORMAT = "%Y-%m-%d:%H:%M:%S"

    def __init__(self, cache_dir=None):
        """Initialize."""
        self.set_cache_dir(cache_dir)

    def get_cache_dir(self):
        """Where are files cached?"""
        return self.cache_dir

    def set_cache_dir(self, cache_dir):
        """Post-initialize."""
        self.cache_dir = cache_dir
        self._initialize_index()

    def has(self, identifier):
        """Is the identifier present in the index?"""
        index = self.load()
        return any(entry.identifier == identifier for entry in index)

    def known(self):
        """What entries are known?"""
        return {entry.identifier for entry in self.load()}

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

    @abstractmethod
    def _initialize_index(self):
        """Initialize index file if necessary."""

def current_time():
    """Get time (separate to make mocking easier)."""
    return datetime.datetime.now()
