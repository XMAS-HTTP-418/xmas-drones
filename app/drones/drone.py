from typing import List, Optional
import numpy as np
from tasks.task import Task
from models import Station, StationType, LoadType, Load
from dataclasses import dataclass
from search.dijkstra import Dijkstra, get_array_height_map
from config import MISSION_AREA_IMAGE


@dataclass
class Drone:
    id: int
    position: np.array
    # velocity: np.array
    # power: float
    # mass: float
    # max_load: float
    battery: float
    # max_battery: float
    # recharge_rate: float
    is_master: bool
    load: Optional[Load]
    task: Task | None
    slaves: Optional[list]
    stations: Optional[list[Station]]
    assignments: Optional[list[tuple]]
    mission: Optional[dict]
    tasks: Optional[Task]
    pathfinder: Optional[Dijkstra]
    max_time_fly: float = 0.5

    def get_time_fly(self) -> np.float64:
        return self.max_time_fly * self.battery / self.max_battery

    time_fly = property(get_time_fly)

    def calculate_energy_for_flying(self, start_position: np.array, end_position: np.array) -> float:
        if not self.pathfinder:
            heightmap = get_array_height_map(MISSION_AREA_IMAGE)
            self.pathfinder = Dijkstra(heightmap, start=(int(start_position[0]), int(start_position[1])))
        distance = self.pathfinder.get_distances((int(end_position[0]), int(end_position[1])))
        return distance

    def evaluate_mission_cost(self, task: Task) -> np.float64:
        additional_cost = 0.0
        if self.load:
            if self.load.type == LoadType[task.type]:
                additional_cost = 0.0
            else:  # return to station to store and pickup
                additional_cost += self.calculate_energy_for_flying(
                    self.position, get_closest_station_to_drone(self, self.stations, StationType.LOAD).position
                )
        else:  # return to station to pickup
            additional_cost = self.calculate_energy_for_flying(
                self.position, get_closest_station_to_drone(self, self.stations, StationType.LOAD).position
            )
        flying_to_mission_cost = self.calculate_energy_for_flying(
            self.position, task.get_closest_position(self.position)
        )
        return additional_cost + flying_to_mission_cost


# ???? ???????? ?????????????? ?????????? ??????????????
def drone_with_max_fly(list: List[Drone]) -> Drone:
    return max(list, key=lambda d: d.time_fly)


# ???????????????????? ???? utils ?? ????????????
def get_closest_station_to_drone(drone: Drone, stations: list[Station], station_type: StationType):
    return min(
        filter(lambda x: x.type == station_type, stations),
        key=lambda x: (drone.position[0]-x.position[0])**2+(drone.position[1]-x.position[1])**2,
    )
