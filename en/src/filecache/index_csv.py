"""CSV-based index."""

import csv
from pathlib import Path

from index_base import IndexBase, CacheEntry
from exceptions import CacheException


class IndexCSV(IndexBase):
    """Store index as CSV file."""

    INDEX_FILE = "index.csv"

    def load(self):
        """Load entire index."""
        if not self.local_dir:
            raise CacheException("Local directory not set in index")

        indexpath = Path(self.local_dir, self.INDEX_FILE)
        if not indexpath.exists():
            raise CacheException(f"Index file {indexpath} not found")

        with open(indexpath, "r") as stream:
            reader = csv.reader(stream)
            return [CacheEntry(r[0], r[1]) for r in reader]

    def save(self, index):
        """Save entire index."""
        if not self.local_dir:
            raise CacheException("Local directory not set in index")

        indexpath = Path(self.local_dir, self.INDEX_FILE)
        with open(indexpath, "r") as stream:
            writer = csv.writer(stream)
            for entry in index:
                writer.write((entry.identifier, entry.timestamp))
