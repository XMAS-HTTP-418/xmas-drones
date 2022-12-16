# client

import socket

from app.config import SOCKET_HOST, SOCKET_PORT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SOCKET_HOST, SOCKET_PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")
