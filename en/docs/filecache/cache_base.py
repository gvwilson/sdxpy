"""Define behavior of caches."""

from abc import ABC, abstractmethod
from pathlib import Path

from exceptions import CacheException
from hash_stream import hash_stream


class CacheBase(ABC):
    """Manage file cache."""

    def __init__(self, index):
        """Initialize cache."""
        self.index = index

    def add(self, local_path):
        """Add a file to the system, returning the file ID."""
        identifier = self._make_identifier(local_path)
        self._add(identifier, local_path)
        self.index.add(identifier)
        return identifier

    def get_cache_path(self, identifier):
        """Get the path to a local copy of the file or raise an exception."""
        if not self.index.has(identifier):
            raise CacheException(f"Unknown file identifier {identifier}")
        return self._make_cache_path(identifier)

    def has(self, identifier):
        """Is this file available?"""
        return self.index.has(identifier)

    def known(self):
        """What files are known?"""
        return self.index.known()

    def _make_identifier(self, local_path):
        """Create a unique identifier based on file contents."""
        with open(local_path, "rb") as reader:
            return hash_stream(reader)

    def _make_cache_path(self, identifier):
        """Construct the path to a localized file."""
        return Path(self.index.get_cache_dir(), f"{identifier}.cache")

    @abstractmethod
    def _add(self, identifier, local_path):
        """Add a file using the given identifier."""
