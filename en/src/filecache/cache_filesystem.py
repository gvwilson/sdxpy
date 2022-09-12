from cache_base import CacheBase, CacheException


class CacheFilesystem(CacheBase):
    """Cache files using local filesystem."""

    def __init__(self, master_dir, local_dir, local_size):
        """Initialize cache."""
        super().__init__(local_dir, local_size)
        self.master_dir = master_dir

    def has(self, identifier, local_only=False):
        """Is this file available (locally)?"""

    def get_local(self, identifier, download=True):
        """Get the path to a local copy of the file or raise an exception."""

    def add(self, identifier, local_path, update=False):
        """Add a file to the system, replacing existing if told to do so."""
