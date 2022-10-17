import datetime
from abc import ABC, abstractmethod
from collections import namedtuple

CacheEntry = namedtuple("CacheEntry", ["identifier", "timestamp"])

class IndexBase(ABC):
    TIME_FORMAT = "%Y-%m-%d:%H:%M:%S"

    def __init__(self, index_dir=None):
        self.set_index_dir(index_dir)

    def get_index_dir(self):
        return self.index_dir

    def set_index_dir(self, index_dir):
        self.index_dir = index_dir
        self._initialize_index()

    def has(self, identifier):
        index = self.load()
        return any(entry.identifier == identifier for entry in index)

    def known(self):
        return {entry.identifier for entry in self.load()}

    def add(self, identifier):
        index = self.load()
        entry = CacheEntry(identifier, current_time())
        index.append(entry)
        self.save(index)

    @abstractmethod
    def load(self):
        """Load entire index."""

    @abstractmethod
    def save(self, index):
        """Save entire index."""

    @abstractmethod
    def _initialize_index(self):
        """Initialize index file if necessary."""

def current_time():
    return datetime.datetime.now()
