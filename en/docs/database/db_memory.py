from util import PAGE_SIZE, DBError, record_size
from page_memory import PageMemory as Page


class DBMemory:
    def __init__(self, page_size=PAGE_SIZE):
        self._page_size = page_size
        self._pages = [Page(self._page_size)]

    def append(self, buf):
        if not self._pages[-1].fits(buf):
            self._pages.append(Page(self._page_size))
        self._pages[-1].append(buf)

    def size(self):
        return sum(page.size() for page in self._pages)

    def num_pages(self):
        return len(self._pages)

    def get(self, index):
        records_per_page = self._page_size // record_size()
        page_number = index // records_per_page
        if page_number >= self.num_pages():
            raise DBError("Index out of range")
        within_page = index % records_per_page
        return self._pages[page_number].get(within_page)
