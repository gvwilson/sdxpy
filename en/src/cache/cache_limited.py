import shutil
from pathlib import Path

from cache_filesystem import CacheFilesystem

class CacheLimited(CacheFilesystem):
    def __init__(self, index, cache_dir, permanent_dir, local_limit):
        super().__init__(index, cache_dir)
        self.permanent_dir = permanent_dir
        self.local_limit = local_limit

    def get_cache_path(self, identifier):
        cache_path = super().get_cache_path(identifier)
        if not cache_path.exists():
            self._ensure_cache_space()
            permanent_path = self._make_permanent_path(identifier)
            shutil.copyfile(permanent_path, cache_path)
        return cache_path

    def _add(self, identifier, local_path):
        self._add_permanent(identifier, local_path)
        self._ensure_cache_space()
        super()._add(identifier, local_path)

    def _add_permanent(self, identifier, local_path):
        permanent_path = self._make_permanent_path(identifier)
        if not permanent_path.exists():
            shutil.copyfile(local_path, permanent_path)

    def _ensure_cache_space(self):
        # Check size.
        cache_dir = Path(self.cache_dir)
        assert cache_dir.exists()
        cache_files = list(cache_dir.iterdir())
        if len(cache_files) < self.local_limit:
            return

        # Remove a file.
        choice = cache_files.pop()
        assert len(cache_files) < self.local_limit
        Path(choice).unlink()

    def _make_permanent_path(self, identifier):
        return Path(self.permanent_dir, f"{identifier}.{self.CACHE_SUFFIX}")
