from config import SOCKET_HOST, SOCKET_PORT
from communicate.slave import SlaveMaster, Request


if __name__ == '__main__':
    server2 = SlaveMaster(SOCKET_HOST, SOCKET_PORT)
    if server2.connect_to_server():
        server2.start()
        server2.requestData(Request("dsa","dsa","ti dyrek"), lambda _: print('sent'))
    # slave = Slave(server2)