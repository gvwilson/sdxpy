from convert import record_size
from page import PAGE_SIZE, DBError, Page

class DBMemory:
    def __init__(self, page_size=PAGE_SIZE):
        self.page_size = page_size
        self.pages = [Page(self.page_size)]

    def append(self, buf):
        if not self.pages[-1].fits(buf):
            self.pages.append(Page(self.page_size))
        self.pages[-1].append(buf)

    def size(self):
        return sum(page.size() for page in self.pages)

    def num_pages(self):
        return len(self.pages)

    def get(self, index):
        records_per_page = self.page_size // record_size()
        page_number = index // records_per_page
        if page_number >= self.num_pages():
            raise DBError("Index out of range")
        within_page = index % records_per_page
        return self.pages[page_number].get(within_page)
