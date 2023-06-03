import socket
import sys

CHUNK_SIZE = 1024
SERVER_ADDRESS = ("localhost", 8080)

# [make]
def make_socket(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))
    return conn
# [/make]

# [send]
def send_file(conn, filename):
    with open(filename, "rb") as reader:
        data = reader.read()
    print(f"client sending {len(data)} bytes")
    total = 0
    while total < len(data):
        sent = conn.send(data[total:])
        print(f"...client sent {sent} bytes")
        if sent == 0:
            break
        total += sent
        print(f"...client total now {total} bytes")
    return total
# [/send]

# [receive]
def receive_ack(conn):
    received = conn.recv(CHUNK_SIZE)
    return int(str(received, "utf-8"))
# [/receive]

# [main]
def main(host, port, filename):
    conn = make_socket(host, port)
    bytes_sent = send_file(conn, filename)
    print(f"client main sent {bytes_sent} bytes")
    bytes_received = receive_ack(conn)
    print(f"client main received {bytes_received} bytes")
    print(bytes_sent == bytes_received)
# [/main]

if __name__ == "__main__":
    host, port, filename = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    main(host, port, filename)
