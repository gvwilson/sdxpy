from http.server import HTTPServer, BaseHTTPRequestHandler

# Page to send back.
PAGE = """\
<html>
<body>
<p>Hello, web!</p>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests by returning a fixed "page"."""

    # Handle a GET request.
    def do_GET(self):
        content = bytes(PAGE, "utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    server_address = ("", 8080)
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()
