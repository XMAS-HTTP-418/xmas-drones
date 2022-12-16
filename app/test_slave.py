from config import SOCKET_HOST, SOCKET_PORT
from communicate.slave import SlaveMaster


if __name__ == '__main__':
    server2 = SlaveMaster(SOCKET_HOST, SOCKET_PORT)
    if server2.connect_to_server():
        server2.run()
    # slave = Slave(server2)