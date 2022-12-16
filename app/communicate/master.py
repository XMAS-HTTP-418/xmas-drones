# server
from typing import Callable
import socket as Socket
# from drones import DroneController
from threading import Thread
from logger import Logger
from communicate.models import SlaveInfo
from communicate.slave_handler import SlaveHandler


class Server(Thread):
    def __init__(self, address, port, message_callback: Callable = lambda _: _):
        super().__init__()
        self.socket = Socket.socket()
        self.socket.bind((address, port))
        self.__isWorking = False
        self.slaves = {}
        self.client_index = 0
        self.message_callback = message_callback

    @property
    def isWorking(self):
        return self.__isWorking

    def run(self):
        self.__isWorking = True
        self.listen_clients()

    def listen_clients(self):
        while self.__isWorking:
            self.socket.listen()
            slave_info = self.wait_slave_connection()
            if not self.__isWorking:
                return
            self.serve_client(slave_info)

    def serve_client(self, slave_info: SlaveInfo):
        slave_handler = SlaveHandler(slave_info, self.client_index, self.message_callback)
        self.slaves[self.client_index] = slave_handler
        self.client_index += 1
        slave_handler.on_client_disconnected = self.on_client_disconnected
        slave_handler.start()

        Logger.log(f"Slave #{slave_handler.index} {slave_handler.address} has connected")

    def wait_slave_connection(self):
        try:
            slaveInfo = self.socket.accept()
            return SlaveInfo(slaveInfo)
        except OSError:
            if self.__isWorking:
                raise

    def on_client_disconnected(self, client: SlaveHandler):
        try:
            self.slaves.pop(client.index)
            #TODO перерасчет группы так как кто-то отвалился
        except KeyError as e:
            Logger.log(f"Error {e} slaves={self.slaves}")
        Logger.log(f"Slave #{client.index} {client.address} has disconnected")

    def stop(self):
        self.__isWorking = False
        self.socket.close()
        client: SlaveHandler
        for client in self.slaves.values():
            client.pended_to_disconnect = True
            client.disconnect()
        Logger.command("Server has stopped")

#
# class Master(DroneController, Server):
#     pass
