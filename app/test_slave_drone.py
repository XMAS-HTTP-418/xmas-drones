from config import SOCKET_HOST, SOCKET_PORT
from communicate.slave import SlaveMaster, Request
from data_parser import DataParser

from drones.drone_controller import DroneController

if __name__ == '__main__':
    master = DroneController(1, [1,0,0], 40, False, None, None, None, None, None, None, None, None)
    master.run()
