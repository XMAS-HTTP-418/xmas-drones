from communicate.master import Server 

if __name__ == '__main__':
    server = Server(SOCKET_HOST, SOCKET_PORT)
    server.start()