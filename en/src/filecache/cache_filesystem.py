import shutil
from pathlib import Path

from cache_base import CacheBase, CacheException


class CacheFilesystem(CacheBase):
    """Cache files using local filesystem."""

    def __init__(self, index, remote_dir, local_dir, local_size):
        """Initialize cache."""
        super().__init__(index, local_dir, local_size)
        self.remote_dir = remote_dir

    def _add(self, identifier, local_path):
        """Add a file to the system."""
        remote_path = self._make_remote_path(identifier)
        if not remote_path.exists():
            shutil.copyfile(local_path, remote_path)

    def _localize_file(self, identifier, local_path):
        """Get a local copy of the file."""
        remote_path = self._make_remote_path(identifier)
        if not remote_path.exists():
            raise CacheException(f"Remote file {identifier} not found at {remote_path}")
        shutil.copyfile(remote_path, local_path)
        self._cleanup(but_not=identifier)

    def _make_remote_path(self, identifier):
        """Construct the path to a remote file."""
        return Path(self.remote_dir, f"{identifier}.cache")
