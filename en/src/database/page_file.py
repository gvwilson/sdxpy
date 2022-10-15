from pathlib import Path

from page import PAGE_SIZE, Page

class PageFile(Page):
    def __init__(self, page_number, page_size=PAGE_SIZE):
        super().__init__(page_size)
        self._page_number = page_number

    def page_number(self):
        return self._page_number

    def load(self, db_dir):
        with open(self._make_path(db_dir), "rb") as reader:
            self._data = bytearray(reader.read())

    def save(self, db_dir):
        with open(self._make_path(db_dir), "wb") as writer:
            writer.write(self._data)

    def _make_path(self, db_dir):
        return Path(db_dir, f"{self._page_number:04x}.page")
