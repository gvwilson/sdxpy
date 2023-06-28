import socketserver

BLOCK_SIZE = 1024

# [class]
class LoggingHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.debug("server about to start receiving")
        data = bytes()
        while True:
            latest = self.request.recv(BLOCK_SIZE)
            self.debug(f"...server received {len(latest)} bytes")
            data += latest
            if len(latest) < BLOCK_SIZE:
                self.debug(f"...server breaking")
                break
        self.debug(f"server finished received, about to reply")
        self.request.sendall(bytes(f"{len(data)}", "utf-8"))

    # [debug]
    def debug(self, *args):
        print(*args)
    # [/debug]
# [/class]

if __name__ == "__main__":
    import sys
    host, port = sys.argv[1], int(sys.argv[2])
    server = socketserver.TCPServer((host, port), LoggingHandler)
    server.serve_forever()
