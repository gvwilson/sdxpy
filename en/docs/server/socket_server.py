import socketserver

KILOBYTE = 1024
SERVER_ADDRESS = ("", 8080)


class MyHandler(socketserver.BaseRequestHandler):
    """The request handler class for our server."""

    def handle(self):
        """Handle a single request."""
        data = self.request.recv(KILOBYTE)
        msg = f"got request from {self.client_address[0]}: {len(data)}"
        print(msg)
        self.request.sendall(bytes(msg, "utf-8"))


if __name__ == "__main__":
    server = socketserver.TCPServer(SERVER_ADDRESS, MyHandler)
    server.serve_forever()
