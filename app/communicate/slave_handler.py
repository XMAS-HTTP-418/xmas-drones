from datetime import datetime
from socket import socket
from threading import Thread
from config import DATA_PACKAGE_ENCODING, DATA_CLOSING_SEQUENCE, DATA_PACKAGE_SIZE, TIME_FORMAT, TIME_DRONE, TIME_PING
from typing import Callable
from communicate.models import SlaveInfo, Response
from logger import Logger
from communicate.controller_message import MessageController


class SlaveHandler(Thread):
    def __init__(self, slave_info: SlaveInfo, client_index, message_callback: Callable = lambda _:_):
        super().__init__()
        self.connection: socket = slave_info.connection
        self.address = slave_info.full_address
        self.index = client_index
        self.connectionTime = datetime.now().strftime(TIME_FORMAT)
        self.requestHandler = MessageController(client_index, message_callback)
        self.on_client_disconnected = lambda *_: None
        self.pended_to_disconnect = False


    def disconnect(self):
        self.connection.close()

    def run(self):
        try:
            request_parts = []
            while received_data := self.get_data_package():
                request_parts.append(received_data.decode(DATA_PACKAGE_ENCODING))
                if received_data.endswith(DATA_CLOSING_SEQUENCE):
                    request_data = ''.join(request_parts)[: -len(DATA_CLOSING_SEQUENCE)]
                    for single_request_data in request_data.split(DATA_CLOSING_SEQUENCE.decode(DATA_PACKAGE_ENCODING)):
                        self.handle_request(single_request_data)
                    request_parts = []
            if not self.pended_to_disconnect:
                self.on_client_disconnected(self)
        except TimeoutError:
            self.on_client_disconnected(self)


    def get_data_package(self) -> bytes:
        try:
            self.connection.settimeout(TIME_DRONE) 
            recvData = self.connection.recv(DATA_PACKAGE_SIZE)
            return recvData
        except ConnectionError:
            return 0
        except TimeoutError:
            return self.time_to_ping()


    def handle_request(self, requestData):
        response = self.requestHandler.handle(requestData)
        print(response)
        self.respond(response.toJson())


    def time_to_ping(self) -> bytes:
        try:
            request = Response(True,self.index,"hello")
            self.respond(request.toJson())
            self.connection.settimeout(TIME_PING) # выкидывает ошибку
            recvData = self.connection.recv(DATA_PACKAGE_SIZE)
            return recvData
        except ConnectionError:
            return 0



    def respond(self, data: str) -> None:
        data = data.encode(DATA_PACKAGE_ENCODING) + DATA_CLOSING_SEQUENCE
        try:
            self.connection.sendall(data)
        except ConnectionError:
            self.on_client_disconnected(self)
