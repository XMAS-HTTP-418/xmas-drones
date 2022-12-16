from datetime import datetime
from socket import socket
from threading import Thread

from config import dataPackageEncoding, dataClosingSequence, dataPackageSize, timeFormat
from models import SlaveInfo


class SlaveHandler(Thread):
    def __init__(self, SlaveInfo: SlaveInfo, clientIndex):
        super().__init__()
        self.connection: socket = SlaveInfo.connection
        self.address = SlaveInfo.fullAddress
        self.index = clientIndex
        self.connectionTime = datetime.now().strftime(timeFormat)
        # self.requestHandler = RequestHandler(changesEvent, clientIndex)
        self.onClientDisconnected = lambda *_: None
        self.pendedToDisconnect = False

    def disconnect(self):
        self.connection.close()

    def run(self):
        requestParts = []
        while receivedData := self.getDataPackage():
            requestParts.append(receivedData.decode(dataPackageEncoding))
            if receivedData.endswith(dataClosingSequence):
                requestData = ''.join(requestParts)[: -len(dataClosingSequence)]
                for singleRequestData in requestData.split(dataClosingSequence.decode(dataPackageEncoding)):
                    self.handleRequest(singleRequestData)
                requestParts = []
        if not self.pendedToDisconnect:
            self.onClientDisconnected(self)

    def getDataPackage(self):
        try:
            recvData = self.connection.recv(dataPackageSize)
            return recvData
        except ConnectionError:
            return 0

    def handleRequest(self, requestData):
        response = self.requestHandler.handle(requestData)
        self.respond(response.toJson())

    def respond(self, data: str):
        data = data.encode(dataPackageEncoding) + dataClosingSequence
        try:
            self.connection.sendall(data)
        except ConnectionError:
            self.onClientDisconnected(self)
