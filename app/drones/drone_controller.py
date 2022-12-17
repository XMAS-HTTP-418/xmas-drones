import json

from search.dijkstra import Dijkstra, get_array_height_map
from drones.drone import Drone
from communicate.models import Request, Response
from data_parser.stations import StationType
from tasks.task import Task
from data_parser import DataParser
from config import SOCKET_HOST, SOCKET_PORT
from communicate.slave import SlaveMaster, Request
from communicate.master import Server
from tasks.task_assignment import get_cost_matrix, calculate_task_assignments
from logger import Logger

# from tasks.task_assignment import calculate_task_assignments, get_cost_matrix
from config import DISTANCE_ARRIVAL_THRESHOLD, MISSION_AREA_IMAGE, DRONE_BATTERY_THRESHOLD
import numpy as np


class DroneController(Drone):
    def socket_get_incomming_mission(self):
        pass

    def socket_check_for_incomming_mission(self):
        pass

    def socket_check_for_incomming_task(self):
        pass

    def socket_ask_for_task_assignment(self, server: SlaveMaster) -> None:
        request = Request(controller=self.id, action="ask task", body={})
        server.requestData(request, lambda data: (setattr(self, 'task', Task(**data) if data else None)))
        Logger.log("Task assignment asked")

    def socket_send_task_assignment(self, server: SlaveMaster, drone_id: int, task: Task) -> None:
        request = Request(controller=self.id, action='task assignment', body={'task_id': task.id, 'drone_id': drone_id})
        server.requestData(request, lambda _: print('sent'))

    def socket_get_task_assignment(self) -> Task:
        pass

    def socket_receive_status_from_slave(self):
        pass

    def socket_send_status_to_master(self, server: SlaveMaster):
        request = Request(
            controller=self.id,
            action='status',
            body={'id': self.id, 'battery': self.battery, 'position': [self.position[0], self.position[1]]},
        )
        server.requestData(request, lambda _: print('Status sent to master'))

    def socket_master_message_handler(self, request_data: Request) -> Response | None:
        if request_data.action == 'status':
            drone = request_data.body
            print(drone)
            if self.slaves and list(filter(lambda x: x.id == drone['id'], self.slaves)):
                for slave in self.slaves:
                    if slave.id == drone['id']:
                        slave.position = drone['position']
                        slave.battery = drone['battery']
            else:
                if not self.slaves:
                    self.slaves = []
                self.slaves.append(
                    Drone(
                        drone['id'],
                        np.array(drone['position']),
                        drone['battery'],
                        False,
                        None,None,None,None,None,None,None,None
                    )
                )
            return Response(True, self.id, "Done", False)
        if request_data.action == 'ask task':
            print(self.assignments)
            if self.assignments:
                print(self.id)
                return Response(True, self.id, self.assignments[self.id-1][1], False)
            else:
                return Response(True, self.id, {}, False)
        if request_data.action == 'ping_slave':
            return Response(True, self.id, 'ping_response', False)
        if request_data.action == 'connect':
            return Response(True, self.id, 'accept')
        if request_data.action == 'ping_master':
            return None
        return None

    def socket_mission_recalculate(self):
        if not self.mission:
            with open('../data/input.json') as f:
                data = json.load(f)
                self.mission = data
        DataParser.load_data(self.mission)
        cost_matrix = get_cost_matrix(self.slaves, DataParser.missions, DataParser.stations)
        tasks = calculate_task_assignments(cost_matrix)
        self.assignments = tasks
        for i in range(len(self.assignments)):
            self.assignments[i][0] = self.slaves[i]
        self.tasks = DataParser.missions
        self.stations = DataParser.stations
        Logger.log("Mission recalculated")
    def socket_check_master(self):
        pass

    def vote_for_master(self):
        pass

    def pathfinder_regen(self):
        heightmap = get_array_height_map(MISSION_AREA_IMAGE)
        self.pathfinder = Dijkstra(heightmap, start=(int(self.position[0]), int(self.position[1])))
        # отправка в json TODO
        self.go_to_output_json(self)

    # создание дрона в json
    def create_drons(self):
        return {"id": self.id,"route":[self.pathfinder.get_route()]}


    def go_to_output_json(self):
        with open('../data/output.json') as f:
                data = json.loads(f)
        if data["drons"]:
            for drone in data["drons"]:
                if drone["id"] == self.id:
                    drone["route"] = drone["route"] + [self.pathfinder.get_route()]
        else :
            data["drons"] = [self.create_drons(self)]

        with open("data/output.json", mode='w+') as f:
            f.write(json.dumps(data))
        



    def fly_towards_recharge_station(self):
        target_pos = self.get_closest_station_to_drone(self, self.stations, StationType.RECHARGE)
        next_move = self.pathfinder.get_route((target_pos[0], target_pos[1]))[1]
        self.position[0], self.position[1] = next_move[0], next_move[1]

    def fly_towards_task(self):
        task_pos = self.task.get_closest_position(self)
        next_move = self.pathfinder.get_route((task_pos[0], task_pos[1]))[1]
        self.position[0], self.position[1] = next_move[0], next_move[1]

    def check_task_area(self):
        delta = self.task.get_closest_position(self) - self.position
        return np.sqrt(delta[0] ** 2 + delta[1] ** 2) < DISTANCE_ARRIVAL_THRESHOLD

    def activate_load(self):
        pass

    def run(self):
        if self.is_master:
            server = Server(
                SOCKET_HOST, SOCKET_PORT, self.socket_master_message_handler, self.socket_mission_recalculate
            )
            server.start()
        else:
            server = SlaveMaster(SOCKET_HOST, SOCKET_PORT, self.socket_master_message_handler)
            if server.connect_to_server():
                server.start()
                self.socket_send_status_to_master(server)
                self.socket_ask_for_task_assignment(server)
            if not self.socket_check_master():
                self.vote_for_master()
            if self.socket_check_for_incomming_task():
                task = self.get_task_assignment()
                self.assign_task(task)
                self.send_status_to_master()

        if self.battery < DRONE_BATTERY_THRESHOLD:
            self.fly_towards_recharge_station()
        else:
            if self.task:
                self.fly_towards_task()
                if self.check_task_area():
                    self.activate_load()
