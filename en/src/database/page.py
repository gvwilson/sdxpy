from convert import record_size

RECORD_SIZE = record_size()
PAGE_SIZE = 1024


class DBError(Exception):
    def __init__(self, message):
        self.message = message


class Page:
    def __init__(self, page_size=PAGE_SIZE):
        assert page_size > 0
        self.page_size = page_size
        self.record_size = RECORD_SIZE
        self.data = bytearray(self.page_size)
        self.top = 0

    def append(self, buf):
        if not len(buf) == RECORD_SIZE:
            raise DBError("Wrong size of record")
        if not self.fits(buf):
            raise DBError("No room for record")
        for b in buf:
            self.data[self.top] = b
            self.top += 1

    def fits(self, buf):
        if not len(buf) == RECORD_SIZE:
            raise DBError("Wrong size of record")
        return self.top + len(buf) <= self.page_size

    def get(self, index):
        if not (0 <= index < (self.page_size // self.record_size)):
            raise DBError("Index out of range")
        start = self.record_size * index
        return self.data[start:(start+self.record_size)]

    def size(self):
        return self.top
