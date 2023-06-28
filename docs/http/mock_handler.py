from io import BytesIO

class MockRequestHandler:
    def __init__(self, path):
        self.path = path
        self.status = None
        self.headers = {}
        self.wfile = BytesIO()

    def send_response(self, status):
        self.status = status

    def send_header(self, key, value):
        if key not in self.headers:
            self.headers[key] = []
        self.headers[key].append(value)

    def end_headers(self):
        pass
