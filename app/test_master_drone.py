from communicate.master import Server
from config import SOCKET_HOST, SOCKET_PORT
from drones.drone_controller import DroneController
from tasks.task_assignment import calculate_task_assignments
from numpy import array
from models import Load
from tasks.task import Task

if __name__ == '__main__':
    mission = Task(1,"SPRAYING_SYSTEM",1,None, 0.0)
    loads = [ Load( 1,"SPRAYING_SYSTEM", 50, 2,0.5,1)]

    master = DroneController(2, [0,5,10], 40, True,loads, mission, None, None, None, None, None, None)
    master.run()
