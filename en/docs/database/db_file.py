from pathlib import Path

from util import PAGE_SIZE, DBError, record_size
from page_file import PageFile as Page

class DBFile:
    def __init__(self, db_dir, page_size=PAGE_SIZE):
        self._db_dir = db_dir
        self._page_size = page_size
        self._cache = {}

    def append(self, buf):
        self._ensure_space(buf)
        self._get_current_page().append(buf)

    def size(self):
        return sum(page.size() for page in self._cache.values())

    def num_pages(self):
        return len(self._cache)

    def get(self, index):
        records_per_page = self._page_size // record_size()
        page_number = index // records_per_page
        self._ensure_in_memory(page_number)
        within_page = index % records_per_page
        return self._cache[page_number].get(within_page)

    def fill(self):
        for filename in Path(self._db_dir).iterdir():
            page_number = int(filename.stem)
            self._ensure_in_memory(page_number)

    def flush(self):
        for page in self._cache.values():
            page.save(self._db_dir)

    def _ensure_in_memory(self, page_number):
        if page_number not in self._cache:
            raise DBError(f"Bad bad number {page_number}")

    def _ensure_space(self, buf):
        if len(self._cache) == 0:
            self._cache[0] = Page(0, self._page_size)
            return
        current_page = self._get_current_page()
        if current_page.fits(buf):
            return
        current_page.save(self._db_dir)
        next_page = current_page.page_number() + 1
        self._cache[next_page] = Page(next_page, self._page_size)

    def _get_current_page(self):
        page_id = max(self._cache.keys())
        return self._cache[page_id]
