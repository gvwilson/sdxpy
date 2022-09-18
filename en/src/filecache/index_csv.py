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
        if not self.local_dir:
            raise CacheException("Local directory not set in index")

        indexpath = Path(self.local_dir, self.INDEX_FILE)
        if not indexpath.exists():
            raise CacheException(f"Index file {indexpath} not found")

        with open(indexpath, "r") as stream:
            reader = csv.reader(stream)
            return [
                CacheEntry(r[0], datetime.strptime(r[1], self.TIME_FORMAT))
                for r in reader
            ]

    def save(self, index):
        """Save entire index."""
        if not self.local_dir:
            raise CacheException("Local directory not set in index")

        indexpath = Path(self.local_dir, self.INDEX_FILE)
        with open(indexpath, "w") as stream:
            writer = csv.writer(stream)
            for entry in index:
                when = entry.timestamp.strftime(self.TIME_FORMAT)
                writer.writerow((entry.identifier, when))
