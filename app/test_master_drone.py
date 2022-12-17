from communicate.master import Server
from config import SOCKET_HOST, SOCKET_PORT
from drones.drone_controller import DroneController
from app.tasks.task_assignment import calculate_task_assignments
from numpy import array

if __name__ == '__main__':
    master = DroneController(2, [0,0,0], 40, True, None, None, None, None, None, None, None, None)
    master.run()
