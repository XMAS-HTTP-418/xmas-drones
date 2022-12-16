from config import SOCKET_HOST, SOCKET_PORT
from drones import DroneController
import socket as Socket
from json import JSONDecodeError
from threading import Thread
from config import DATA_CLOSING_SEQUENCE, DATA_PACKAGE_ENCODING, DATA_PACKAGE_SIZE
from models import Request, Response


class SlaveMaster(Thread):
    def __init__(self, address, port):
        super().__init__()
        self.address = address
        self.port = port
        self.socket = Socket.socket()
        self.responseQueue = []

        self.onError = lambda *_: None
        self.onServerDisconnected = lambda *_: None
        self.onChangesReceived = lambda *_: None

    def run(self):
        self.listenResponse()

    def connectToServer(self):
        try:
            self.socket.connect((self.address, self.port))
        except ConnectionRefusedError:
            return False
        return True

    def closeConnection(self):
        self.onServerDisconnected = lambda: None
        self.socket.close()

    def listenResponse(self):
        responseParts = []
        while receivedData := self.getDataPackage():
            responseParts.append(receivedData.decode(DATA_PACKAGE_ENCODING))
            if receivedData.endswith(DATA_CLOSING_SEQUENCE):
                responseData = ''.join(responseParts)[: -len(DATA_CLOSING_SEQUENCE)]
                self.handleResponse(responseData)
                responseParts = []
        self.onServerDisconnected()

    def getDataPackage(self):
        try:
            return self.socket.recv(DATA_PACKAGE_SIZE)
        except ConnectionError:
            return 0

    def requestData(self, request: Request, responseCallback):
        requestData = request.toJson().encode(DATA_PACKAGE_ENCODING)
        requestData += DATA_CLOSING_SEQUENCE
        self.responseQueue.append(responseCallback)
        self.socket.sendall(requestData)

    def handleResponse(self, responseData: str):
        try:
            response = Response.fromJson(responseData)
        except JSONDecodeError:
            message = f"Invalid data received: {responseData}"
            if responseData.startswith("-m"):
                serverMessage = responseData[2:]
                message = f"Message from server:\n{serverMessage}"
            self.onError(message)
            return
        if response.changes:
            self.onChangesReceived(response)
        elif len(self.responseQueue) > 0:
            callback = self.responseQueue.pop(0)
            callback(response)
        else:
            self.onError(f"Unsupportable response {responseData}")


class Slave(DroneController, Thread):
    def __init__(self, slaveWorker: SlaveMaster):
        self.slaveWorker = slaveWorker

    def run(self):
        self.init()

    def init(self):
        tryConnectToServer = self.slaveWorker.connectToServer()


if __name__ == '__main__':
    server2 = SlaveMaster(SOCKET_HOST, SOCKET_PORT)
    if server2.connectToServer():
        server2.run()
    # slave = Slave(server2)
