import socket
import sys

KILOBYTE = 1024
SERVER_ADDRESS = ("", 8080)

message = "message text"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(SERVER_ADDRESS)
sock.sendall(bytes(message, "utf-8"))
print(f"client sent {len(message)} bytes")

received = sock.recv(KILOBYTE)
received_str = str(received, "utf-8")
print(f"client received {len(received)} bytes: '{received_str}'")
