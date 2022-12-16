from app.search.dijkstra import Dijkstra, get_array_height_map
from app.drones.drone import Drone
from app.communicate.models import Request
from app.data_parser.stations import StationType
from app.tasks.task import Task
from app.data_parser import DataParser
from app.tasks.task_assignment import calculate_task_assignments, get_cost_matrix
from app.config import DISTANCE_ARRIVAL_THRESHOLD, MISSION_AREA_IMAGE, DRONE_BATTERY_THRESHOLD
import numpy as np
class DroneController(Drone):
    def socket_get_incomming_mission(self):
        pass

    def socket_check_for_incomming_mission(self):
        pass

    def socket_check_for_incomming_task(self):
        pass

    def socket_send_task_assignment(self, drone_id: int, task: Task) -> None:
        request = Request(
            controller=self.id,
            action='task assignment',
            body=task.id
        )

    def socket_get_task_assignment(self) -> Task:
        pass

    def socket_receive_status_from_slave(self):
        pass

    def socket_send_status_to_master(self):
        request = Request(
            controller=self.id,
            action='status',
            body={
                'id': self.id,
                'battery': self.battery,
                'position': [self.position[0], self.position[1]]
            }
        )

    def socket_send_status_to_master(self):
        pass

    def socket_check_master(self):
        pass

    def vote_for_master(self):
        pass

    def pathfinder_regen(self):
        heightmap = get_array_height_map(MISSION_AREA_IMAGE)
        self.pathfinder = Dijkstra(heightmap, start=(int(self.position[0]), int(self.position[1])))

    def fly_towards_recharge_station(self):
        target_pos = self.get_closest_station_to_drone(self, self.stations, StationType.RECHARGE)
        next_move = self.pathfinder.getRoute((target_pos[0], target_pos[1]))[1]
        self.position[0], self.position[1] = next_move[0], next_move[1]

    def fly_towards_task(self):
        task_pos = self.task.get_closest_position(self)
        next_move = self.pathfinder.getRoute((task_pos[0], task_pos[1]))[1]
        self.position[0], self.position[1] = next_move[0], next_move[1]

    def check_task_area(self):
        delta = self.task.get_closest_position(self) - self.position
        return np.sqrt(delta[0]**2+delta[1]**2) < DISTANCE_ARRIVAL_THRESHOLD

    def activate_load(self):
        pass

    def assign_task(self, task: Task):
        self.task = task

    def run(self):
        if self.is_master:
            if self.check_for_incomming_mission():
                # recalculate mission
                data = self.get_incomming_mission()
                DataParser.load_data(data)
                cost_matrix = get_cost_matrix(DataParser.drones, DataParser.missions)
                tasks = calculate_task_assignments(cost_matrix)
                for task in enumerate(tasks):
                    self.socket_send_task_assignment()
            if self.socket_receive_status_from_slave():
                pass
        else:
            if not self.socket_check_master():
                self.vote_for_master()
            if self.check_for_incomming_task():
                task = self.get_task_assignment()
                self.assign_task(task)
                self.send_status_to_master()

        if self.battery < DRONE_BATTERY_THRESHOLD:
            self.fly_towards_recharge_station()
        else:
            self.fly_towards_task()
            if self.check_task_area():
                self.activate_load()