from util import PAGE_SIZE, DBError, record_size
from page_file import PageFile as Page
from db_file import DBFile

class DBSwap(DBFile):
    def __init__(self, db_dir, max_pages, page_size=PAGE_SIZE):
        super().__init__(db_dir, page_size)
        self._max_pages = max_pages
        self._current_page = Page(0, self._page_size)
        self._cache[0] = self._current_page

    def size(self):
        records_per_page = self._page_size // record_size()
        previous = (self.num_pages() - 1) * records_per_page * record_size()
        return previous + self._current_page.size()

    def num_pages(self):
        return self._current_page.page_number() + 1

    def _ensure_in_memory(self, page_number):
        if page_number in self._cache:
            return
        page = Page(page_number, self._page_size)
        page.load(self._db_dir)
        self._cache[page_number] = page
        self._maintain_cache()

    def _ensure_space(self, buf):
        current_page = self._get_current_page()
        if current_page.fits(buf):
            return

        current_page.save(self._db_dir)
        next_number = current_page.page_number() + 1
        self._current_page = Page(next_number, self._page_size)
        self._cache[next_number] = self._current_page
        self._maintain_cache()

    def _get_current_page(self):
        return self._current_page

    def _maintain_cache(self):
        if len(self._cache) <= self._max_pages:
            return
        candidates = set(self._cache.keys()) - {self._current_page.page_number()}
        selected = min(candidates)
        self._cache[selected].save(self._db_dir)
        del self._cache[selected]
