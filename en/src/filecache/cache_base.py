from abc import ABC, abstractmethod

class CacheException(Exception):
    """Signal a caching error."""
    def __init__(self, message):
        self.message = message


class CacheBase(ABC):
    """Make files locally available."""

    def __init__(self, index, local_dir, local_size):
        """Initialize cache."""
        self.index = index
        self.local_dir = local_dir
        self.local_size = local_size

    @abstractmethod
    def add(self, identifier, local_path, update=False):
        """Add a file to the system, replacing existing if told to do so."""

    @abstractmethod
    def _localize_file(self, identifier, local_path):
        """Get a local copy of a file."""

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

    def _make_local_path(self, identifier):
        """Construct the path to a localized file."""
        return Path(self.local_dir, f"{identifier}.cache")

