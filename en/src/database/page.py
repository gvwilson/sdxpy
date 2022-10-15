from convert import record_size

RECORD_SIZE = record_size()
PAGE_SIZE = 1024


class DBError(Exception):
    def __init__(self, message):
        self.message = message


class Page:
    def __init__(self, page_size=PAGE_SIZE):
        assert page_size > 0
        self._page_size = page_size
        self._record_size = RECORD_SIZE
        self._data = bytearray(self._page_size)
        self._top = 0

    def append(self, buf):
        if not len(buf) == RECORD_SIZE:
            raise DBError("Wrong size of record")
        if not self.fits(buf):
            raise DBError("No room for record")
        for b in buf:
            self._data[self._top] = b
            self._top += 1

    def fits(self, buf):
        if not len(buf) == RECORD_SIZE:
            raise DBError("Wrong size of record")
        return self._top + len(buf) <= self._page_size

    def get(self, index):
        if not (0 <= index < (self._page_size // self._record_size)):
            raise DBError("Index out of range")
        start = self._record_size * index
        return self._data[start:(start+self._record_size)]

    def size(self):
        return self._top
