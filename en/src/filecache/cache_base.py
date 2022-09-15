"""Define behavior of caches."""

from abc import ABC, abstractmethod

from exceptions import CacheException
from hash_stream import hash_stream


class CacheBase(ABC):
    """Make files locally available."""

    def __init__(self, index, local_dir, local_size):
        """Initialize cache."""
        self.index = index
        self.local_dir = local_dir
        self.local_size = local_size
        self.index.set_local_dir(self.local_dir)

    def add(self, local_path):
        """Add a file to the system, returning the file ID."""
        identifier = self._make_identifier(local_path)
        self._add(identifier, local_path)
        self.index.add(identifier)
        return identifier

    def has(self, identifier, local_only=False):
        """Is this file available (locally)?"""
        if not self.index.has(identifier):
            return False
        if local_only:
            local_path = self._make_local_path(identifier)
            return local_path.exists()
        return True

    def get_local_path(self, identifier, download=True):
        """Get the path to a local copy of the file or raise an exception."""
        if not self.index.has(identifier):
            raise CacheException(f"Unknown file identifier {identifier}")
        local_path = self._make_local_path(identifier)
        if not local_path.exists():
            self._localize_file(identifier, local_path)
        return local_path

    def _cleanup(self, but_not=None):
        """Clean up the local cache."""
        for identifier in index.least_recently_used():
            if shutil.disk_usage(self.local_dir) <= self.local_size:
                break
            if (but_not is not None) and (identifier == but_not):
                continue
            delete_path = self._make_local_path(identifier)
            delete_path.unlink()

    def _make_identifier(self, local_path):
        """Create a unique identifier based on file contents."""
        with open(local_path, "rb") as reader:
            return hash_stream(reader)

    def _make_local_path(self, identifier):
        """Construct the path to a localized file."""
        return Path(self.local_dir, f"{identifier}.cache")

    @abstractmethod
    def _add(self, identifier, local_path):
        """Add a file using the given identifier."""

    @abstractmethod
    def _localize_file(self, identifier, local_path):
        """Get a local copy of a file."""
