from abc import ABC, abstractmethod

class CacheException(Exception):
    """Signal a caching error."""
    def __init__(self, message):
        self.message = message


class CacheBase(ABC):
    """Make files locally available."""

    def __init__(self, local_dir, local_size):
        """Initialize cache."""
        self.local_dir = local_dir
        self.local_size = local_size

    @abstractmethod
    def has(self, identifier, local_only=False):
        """Is this file available (locally)?"""

    @abstractmethod
    def get_local(self, identifier, download=True):
        """Get the path to a local copy of the file or raise an exception."""

    @abstractmethod
    def add(self, identifier, local_path, update=False):
        """Add a file to the system, replacing existing if told to do so."""
