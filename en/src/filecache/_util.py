"""Utilities for caching."""

class CacheException(Exception):
    """Signal a caching error."""
    def __init__(self, message):
        self.message = message
