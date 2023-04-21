class Database:
    def __init__(self, key_func):
        """Initialize with function to get key."""
        self._key_func = key_func

    def add(self, record):
        """Store the given record."""
        raise NotImplementedError("add")
        
    def get(self, key):
        """Return record associated with key or None."""
        raise NotImplementedError("get")
