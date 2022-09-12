from pathlib import Path
import shutil

from cache_base import CacheBase, CacheException


class CacheFilesystem(CacheBase):
    """Cache files using local filesystem."""

    def __init__(self, index, remote_dir, local_dir, local_size):
        """Initialize cache."""
        super().__init__(index, local_dir, local_size)
        self.remote_dir = remote_dir

    def add(self, identifier, local_path, update=False):
        """Add a file to the system, replacing existing if told to do so."""

    def _localize_file(self, identifier, local_path):
        """Get a local copy of the file."""
        remote_path = self._make_remote_path(identifier)
        if not remote_path.exists():
            raise CacheException(f"Remote file {identifier} at {remote_path} does not exist")
        shutil.copyfile(remote_path, local_path)
        self._cleanup(but_not=identifier)
