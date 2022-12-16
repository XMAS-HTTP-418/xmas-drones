# server

import socket
import time

from app.config import SOCKET_HOST, SOCKET_PORT


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SOCKET_HOST, SOCKET_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            # if not data:
            #     break
            conn.sendall(f'hello: {addr}'.encode())
            time.sleep(10)
