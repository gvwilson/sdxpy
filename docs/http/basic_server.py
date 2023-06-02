from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<html><body><p>test page</p></body></html>"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content = bytes(PAGE, "utf-8")
        self.send_response(200)
        self.send_header(
            "Content-Type", "text/html; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == "__main__":
    server_address = ("localhost", 8080)
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()
