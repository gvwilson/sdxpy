from pathlib import Path

from convert import record_size
from page import PAGE_SIZE, DBError
from page_file import PageFile

class DBFile:
    def __init__(self, db_dir, cache_size, page_size=PAGE_SIZE):
        self._db_dir = db_dir
        self._cache_size = cache_size
        self._page_size = page_size
        self._num_pages = 0
        self._cache = {}
        self._used = []
        self._add_new_page()

    def append(self, buf):
        current_index = self._num_pages - 1
        assert current_index in self._cache
        page = self._cache[current_index]
        if not page.fits(buf):
            page = self._add_new_page()
        page.append(buf)

    def size(self):
        if self._num_pages == 0:
            return 0

        current_index = self._num_pages - 1
        assert current_index in self._cache
        current_size = self._cache[current_index].size()

        records_per_page = self._page_size // record_size()
        preceding_size = (self._num_pages - 1) * records_per_page * record_size()

        return preceding_size + current_size

    def num_pages(self):
        return self._num_pages

    def get(self, index):
        records_per_page = self._page_size // record_size()
        page_number = index // records_per_page
        if page_number >= self.num_pages():
            raise DBError("Index out of range")
        self._ensure_in_memory(page_number)
        within_page = index % records_per_page
        return self._cache[page_number].get(within_page)

    def flush(self):
        for page in self._cache.values():
            page.save(self._db_dir)

    def _add_new_page(self):
        assert self._num_pages not in self._cache
        page = PageFile(self._num_pages, self._page_size)
        self._cache[self._num_pages] = page
        self._used.insert(0, self._num_pages)
        self._num_pages += 1
        self._clean_cache()
        return page

    def _clean_cache(self):
        if len(self._used) <= self._cache_size:
            return
        drop = self._used.pop()
        assert drop in self._cache
        self._cache[drop].save(self._db_dir)
        del self._cache[drop]

    def _ensure_in_memory(self, page_number):
        if page_number in self._cache:
            return
        page = PageFile(page_number)
        page.load(self._db_dir)
        self._cache[page_number] = page
        self._used.insert(0, page_number)
        self._clean_cache()
