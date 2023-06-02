import socket

KILOBYTE = 1024

def handler():
    host, port = socket.gethostbyname("localhost"), 8080
    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1)
    conn, address = server_socket.accept()
    print(f"Connection from {address}")

    data = str(conn.recv(KILOBYTE), "utf-8")
    msg = f"got request from {address}: {len(data)}"
    print(msg)

    conn.send(bytes(msg, "utf-8"))
    conn.close()

# [main]
if __name__ == '__main__':
    handler()
# [/main]
