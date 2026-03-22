from interface_original import Database

class JustDict(Database):
    def __init__(self, key_func):
        super().__init__(key_func)
        self._data = {}

    def add(self, record):
        key = self._key_func(record)
        self._data[key] = record

    def get(self, key):
        return self._data.get(key, None)
