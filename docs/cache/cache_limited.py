import shutil
from pathlib import Path

from cache_filesystem import CacheFilesystem

# [constructor]
class CacheLimited(CacheFilesystem):
    def __init__(self, index, cache_dir, archive_dir, local_limit):
        super().__init__(index, cache_dir)
        self.archive_dir = archive_dir
        self.local_limit = local_limit
# [/constructor]

    # [get]
    def get_cache_path(self, identifier):
        cache_path = super().get_cache_path(identifier)
        if not cache_path.exists():
            self._ensure_cache_space()
            archive_path = self._make_archive_path(identifier)
            shutil.copyfile(archive_path, cache_path)
        return cache_path
    # [/get]

    # [ensure]
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
    # [/ensure]

    # [add]
    def _add(self, identifier, local_path):
        self._add_archive(identifier, local_path)
        self._ensure_cache_space()
        super()._add(identifier, local_path)
    # [/add]

    def _add_archive(self, identifier, local_path):
        archive_path = self._make_archive_path(identifier)
        if not archive_path.exists():
            shutil.copyfile(local_path, archive_path)

    def _make_archive_path(self, identifier):
        return Path(self.archive_dir, f"{identifier}.{self.CACHE_SUFFIX}")
