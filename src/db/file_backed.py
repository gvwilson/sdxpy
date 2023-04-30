from pathlib import Path

from interface import Database

# [core]
class FileBacked(Database):
    def __init__(self, record_cls, filename):
        super().__init__(record_cls)
        self._filename = Path(filename)
        if not self._filename.exists():
            self._filename.touch()
        self._load()

    def add(self, record):
        key = self._record_cls.key(record)
        self._data[key] = record
        self._save()

    def get(self, key):
        return self._data.get(key, None)
# [/core]

    # [helper]
    def _save(self):
        packed = self._record_cls.pack_multi(self._data.values())
        with open(self._filename, "w") as writer:
            writer.write(packed)

    def _load(self):
        assert self._filename.exists()
        with open(self._filename, "r") as reader:
            raw = reader.read()
        records = self._record_cls.unpack_multi(raw)
        self._data = {self._record_cls.key(r): r for r in records}
    # [/helper]
