# server
import socket as Socket
import time
from drones.drone_controller import DroneController
from config import SOCKET_HOST, SOCKET_PORT
from threading import Thread
from logger import Logger
from models import SlaveInfo
from slaveHandler import SlaveHandler


class Server(Thread):
    def __init__(self, address, port):
        super().__init__()
        self.socket = Socket.socket()
        self.socket.bind((address, port))
        self.__isWorking = False
        self.slaves = {}
        self.clientIndex = 0

    @property
    def isWorking(self):
        return self.__isWorking

    def run(self):
        self.__isWorking = True
        self.listenClients()

    def listenClients(self):
        while self.__isWorking:
            self.socket.listen()
            slaveInfo = self.waitSlaveConnection()
            if not self.__isWorking:
                return
            self.serveClient(slaveInfo)

    def serveClient(self, slaveInfo: SlaveInfo):
        slaveHandler = SlaveHandler(slaveInfo, self.clientIndex)
        self.slaves[self.clientIndex] = slaveHandler
        self.clientIndex += 1
        slaveHandler.onClientDisconnected = self.onClientDisconnected
        slaveHandler.start()

        Logger.log(f"Slave #{slaveHandler.index} {slaveHandler.address} has connected")

    def waitSlaveConnection(self):
        try:
            slaveInfo = self.socket.accept()
            return SlaveInfo(slaveInfo)
        except OSError:
            if self.__isWorking:
                raise

    def onClientDisconnected(self, client: SlaveHandler):
        try:
            self.slaves.pop(client.index)
        except KeyError as e:
            Logger.log(f"Error {e} slaves={self.slaves}")
        Logger.log(f"Slave #{client.index} {client.address} has disconnected")

    def stop(self):
        self.__isWorking = False
        self.socket.close()
        client: SlaveHandler
        for client in self.slaves.values():
            client.pendedToDisconnect = True
            client.disconnect()
        Logger.command("Server has stopped")

class Master(DroneController, Server):
    pass


