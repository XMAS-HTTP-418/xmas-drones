from config import SOCKET_HOST, SOCKET_PORT
from drones import DroneController
import socket as Socket
from json import JSONDecodeError
from threading import Thread
from config import DATA_CLOSING_SEQUENCE, DATA_PACKAGE_ENCODING, DATA_PACKAGE_SIZE
from communicate.models import Request, Response
from logger import Logger

class SlaveMaster(Thread):
    def __init__(self, address, port):
        super().__init__()
        self.address = address
        self.port = port
        self.socket = Socket.socket()
        self.response_queue = []

        self.on_error = lambda *_: None
        self.on_server_disconnected = lambda *_: None
        self.on_changes_received = lambda *_: None

    def run(self):
        self.listenResponse()

    def connect_to_server(self):
        try:
            self.socket.connect((self.address, self.port))
        except ConnectionRefusedError:
            return False
        return True

    def closeConnection(self):
        self.on_server_disconnected = lambda: None
        self.socket.close()

    def listenResponse(self):
        response_parts = []
        while received_data := self.get_data_package():
            response_parts.append(received_data.decode(DATA_PACKAGE_ENCODING))
            if received_data.endswith(DATA_CLOSING_SEQUENCE):
                response_data = ''.join(response_parts)[: -len(DATA_CLOSING_SEQUENCE)]
                self.handle_response(response_data)
                response_parts = []
        self.on_server_disconnected()

    def get_data_package(self):
        try:
            return self.socket.recv(DATA_PACKAGE_SIZE)
        except ConnectionError:
            return 0

    def requestData(self, request: Request, response_callback):
        request_data = request.to_json().encode(DATA_PACKAGE_ENCODING)
        request_data += DATA_CLOSING_SEQUENCE
        self.response_queue.append(response_callback)
        self.socket.sendall(request_data)

    def handle_response(self, response_data: str):
        try:
            response = Response.from_json(response_data)
            Logger.log(response.body)
        except JSONDecodeError:
            message = f"Invalid data received: {response_data}"
            if response_data.startswith("-m"):
                server_message = response_data[2:]
                message = f"Message from server:\n{server_message}"
            self.on_error(message)
            return
        if response.changes:
            self.on_changes_received(response)
        elif len(self.response_queue) > 0:
            callback = self.response_queue.pop(0)
            callback(response)
        else:
            self.on_error(f"Unsupportable response {response_data}")


class Slave(DroneController, Thread):
    def __init__(self, slaveWorker: SlaveMaster):
        self.slave_worker = slaveWorker

    def run(self):
        self.init()

    def init(self):
        try_connect_to_server = self.slave_worker.connect_to_server()



