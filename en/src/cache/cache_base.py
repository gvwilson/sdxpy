from abc import ABC, abstractmethod
from pathlib import Path

from exceptions import CacheException
from hash_stream import hash_stream

class CacheBase(ABC):
    CACHE_SUFFIX = "cache"

    def __init__(self, index, cache_dir):
        self.index = index
        self.cache_dir = cache_dir

    def add(self, local_path):
        identifier = self._make_identifier(local_path)
        self.index.add(identifier)
        self._add(identifier, local_path)
        return identifier

    def get_cache_path(self, identifier):
        if not self.index.has(identifier):
            raise CacheException(f"Unknown file identifier {identifier}")
        return self._make_cache_path(identifier)

    def has(self, identifier):
        return self.index.has(identifier)

    def known(self):
        return self.index.known()

    def _make_identifier(self, local_path):
        with open(local_path, "rb") as reader:
            return hash_stream(reader)

    def _make_cache_path(self, identifier):
        return Path(self.cache_dir, f"{identifier}.{self.CACHE_SUFFIX}")

    @abstractmethod
    def _add(self, identifier, local_path):
        """Add a file with a given identifer from a given local path."""
