from interface import Database

class JustDictRefactored(Database):
    def __init__(self, record_cls):
        super().__init__(record_cls)
        self._data = {}

    def add(self, record):
        key = self._record_cls.key(record)
        self._data[key] = record

    def get(self, key):
        return self._data.get(key, None)
