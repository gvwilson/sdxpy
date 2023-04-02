class Database:
    def __init__(self, record_cls):
        """Initialize with data manipulation functions."""
        self._record_cls = record_cls
        
    def add(self, record):
        """Store the given record."""
        raise NotImplementedError("add")

    def get(self, key):
        """Return record associated with key or None."""
        raise NotImplementedError("get")
