from communicate.master import Server
from config import SOCKET_HOST, SOCKET_PORT

if __name__ == '__main__':
    server = Server(SOCKET_HOST, SOCKET_PORT)
    server.start()
