import shutil
from pathlib import Path

from cache_base import CacheBase, CacheException

class CacheFilesystem(CacheBase):
    def _add(self, identifier, local_path):
        cache_path = self._make_cache_path(identifier)
        if not cache_path.exists():
            shutil.copyfile(local_path, cache_path)
