import socketserver

CHUNK_SIZE = 1024
SERVER_ADDRESS = ("localhost", 8080)

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(CHUNK_SIZE)
        cli = self.client_address[0]
        msg = f"got request from {cli}: {len(data)}"
        print(msg)
        self.request.sendall(bytes(msg, "utf-8"))

if __name__ == "__main__":
    server = socketserver.TCPServer(SERVER_ADDRESS, MyHandler)
    server.serve_forever()
