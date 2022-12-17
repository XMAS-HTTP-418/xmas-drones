from tasks.task_assignment import calculate_task_assignments, get_cost_matrix
from search.dijkstra import Dijkstra, get_array_height_map
from drones.drone import Drone
from communicate.models import Request, Response
from data_parser.stations import StationType
from tasks.task import Task
from data_parser import DataParser
from config import SOCKET_HOST, SOCKET_PORT
from communicate.slave import SlaveMaster, Request
from communicate.master import Server

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
        server.requestData(request, lambda data: (setattr(self, 'task', Task(**data))))

    def socket_send_task_assignment(self, server: SlaveMaster, drone_id: int, task: Task) -> None:
        request = Request(controller=self.id, action='task assignment', body={'task_id': task.id, 'drone_id': drone_id})
        server.requestData(request, lambda _: print('sent'))

    def socket_get_task_assignment(self) -> Task:
        pass

    def socket_receive_status_from_slave(self):
        pass

    def socket_send_status_to_master(self):
        request = Request(
            controller=self.id,
            action='status',
            body={'id': self.id, 'battery': self.battery, 'position': [self.position[0], self.position[1]]},
        )

    def socket_master_message_handler(self, request_data: Request.from_Json) -> Response | None:
        if request_data.action == 'status':
            drone = request_data['body']
            if list(filter(lambda x: x.id == drone['id'], self.slaves)):
                for slave in self.slaves:
                    if slave.id == drone['id']:
                        slave.position = drone['position']
                        slave.battery = drone['battery']
            else:
                self.slaves.append(
                    Drone(
                        id=drone['id'],
                        position=np.array(drone['position']),
                        battery=np.array['battery'],
                        is_master=False,
                    )
                )
            return Response(True, self.id, "Done", False)
        if request_data.action == 'ask task':
            task = filter(lambda x: x.id == self.assignments[request_data['controller']][1], self.tasks)[0]
            return Response(True, self.id, task, False)
        if request_data.action == 'ping_slave':
            return Response(True, self.id, 'ping_response', False)
        if request_data.action == 'connect':
            return Response(True, self.id, 'accept')
        if request_data.action == 'ping_master':
            return None
        return None

    def socket_mission_recalculate(self):
        DataParser.load_data(self.mission)
        cost_matrix = get_cost_matrix(DataParser.drones, DataParser.missions)
        tasks = calculate_task_assignments(cost_matrix)
        self.assignments = tasks
        self.tasks = DataParser.missions

    def socket_check_master(self):
        pass

    def vote_for_master(self):
        pass

    def pathfinder_regen(self):
        heightmap = get_array_height_map(MISSION_AREA_IMAGE)
        self.pathfinder = Dijkstra(heightmap, start=(int(self.position[0]), int(self.position[1])))

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
            if self.socket_check_for_incomming_mission():
                # recalculate mission
                data = self.socket_get_incomming_mission()
                self.mission = data
                DataParser.load_data(data)
                cost_matrix = get_cost_matrix(DataParser.drones, DataParser.missions)
                tasks = calculate_task_assignments(cost_matrix)
                self.assignments = tasks
                self.tasks = DataParser.missions
            if self.socket_receive_status_from_slave():
                pass
        else:
            server = SlaveMaster(SOCKET_HOST, SOCKET_PORT, self.socket_master_message_handler)
            if server.connect_to_server():
                server.start()
                server.requestData(Request("dsa", "dsa", "ti dyrek"), lambda _: print('sent'))
            if not self.socket_check_master():
                self.vote_for_master()
            if self.socket_check_for_incomming_task():
                task = self.get_task_assignment()
                self.assign_task(task)
                self.send_status_to_master()

        if self.battery < DRONE_BATTERY_THRESHOLD:
            self.fly_towards_recharge_station()
        else:
            self.fly_towards_task()
            if self.check_task_area():
                self.activate_load()
