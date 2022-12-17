from communicate.master import Server
from config import SOCKET_HOST, SOCKET_PORT
from drones.drone_controller import DroneController

if __name__ == '__main__':
    master = DroneController(2, 12, 40, True, None, None, None, None, None, None, None, None)
    master.run()
