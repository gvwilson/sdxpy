import os
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# [error_page]
ERROR_PAGE = """\
<html>
  <head>
    <title>Error accessing {path}</title>
  </head>
  <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
  </body>
</html>
"""
# [/error_page]

# [exception]
class ServerException(Exception):
    pass
# [/exception]

# [do_get]
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url_path = self.path.lstrip("/")
            full_path = Path.cwd().joinpath(url_path)
            if not full_path.exists():
                raise ServerException(f"'{self.path}' not found")
            elif full_path.is_file():
                self.handle_file(self.path, full_path)
            else:
                raise ServerException(f"Unknown object '{self.path}'")
        except Exception as msg:
            self.handle_error(msg)
# [/do_get]

    # [handle_file]
    def handle_file(self, given_path, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content, HTTPStatus.OK)
        except IOError:
            raise ServerException(f"'{given_path}' cannot be read")
    # [/handle_file]

    # [handle_error]
    def handle_error(self, msg):
        content = ERROR_PAGE.format(path=self.path, msg=msg)
        content = bytes(content, "utf-8")
        self.send_content(content, HTTPStatus.NOT_FOUND)
    # [/handle_error]

    # [send_content]
    def send_content(self, content, status):
        self.send_response(int(status))
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    # [/send_content]

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
