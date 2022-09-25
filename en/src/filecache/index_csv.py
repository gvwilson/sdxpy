"""CSV-based index."""

import csv
from datetime import datetime
from pathlib import Path

from exceptions import CacheException
from index_base import CacheEntry, IndexBase


class IndexCSV(IndexBase):
    """Store index as CSV file."""

    INDEX_FILE = "index.csv"

    def load(self):
        """Load entire index."""
        if not self.index_dir:
            raise CacheException("Cache directory not set in index")

        index_path = self._make_index_path()
        if not index_path.exists():
            raise CacheException(f"Index file {index_path} not found")

        with open(index_path, "r") as stream:
            reader = csv.reader(stream)
            return [
                CacheEntry(r[0], datetime.strptime(r[1], self.TIME_FORMAT))
                for r in reader
            ]

    def save(self, index):
        """Save entire index."""
        if not self.index_dir:
            raise CacheException("Cache directory not set in index")

        index_path = self._make_index_path()
        with open(index_path, "w") as stream:
            writer = csv.writer(stream)
            for entry in index:
                when = entry.timestamp.strftime(self.TIME_FORMAT)
                writer.writerow((entry.identifier, when))

    def _initialize_index(self):
        """Initialize index file if necessary."""
        self._make_index_path().touch()

    def _make_index_path(self):
        """Create index file path."""
        if not self.index_dir:
            raise CacheException("Cache directory not set in index")
        return Path(self.index_dir, self.INDEX_FILE)
