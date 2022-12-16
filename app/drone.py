from typing import List, Optional
import numpy as np
from task import Task
from station import Station, StationType
from load import LoadType, Load
from dataclasses import dataclass
from dijkstra import Dijkstra, getArrayHeightMap
from utils import get_closest_station_to_drone


@dataclass
class Drone:
    id: int
    position: np.array
    velocity: np.array
    power: float
    mass: float
    max_load: float
    battery: float
    max_battery: float
    recharge_rate: float
    is_master: bool
    load: Optional[Load]
    task: Optional[Task]
    stations: Optional[list[Station]]
    pathfinder: Optional[Dijkstra]
    max_time_fly: float = 0.5

    def get_time_fly(self) -> np.float64:
        return self.max_time_fly * self.battery / self.max_battery

    time_fly = property(get_time_fly)

    def calculate_energy_for_flying(self, start_position: np.array, end_position: np.array) -> float:
        if not self.pathfinder:
            heightmap = getArrayHeightMap('data/height_map.png')
            self.pathfinder = Dijkstra(heightmap, start=(int(start_position[0]), int(start_position[1])))
        distance = self.pathfinder.getDistances((int(end_position[0]), int(end_position[1])))
        return distance * self.power

    def evaluate_mission_cost(self, mission: Task) -> np.float64:
        additional_cost = 0.0
        if self.load_id:
            if self.load.type == LoadType[mission.type]:
                additional_cost = 0.0
            else:  # return to station to store and pickup
                additional_cost += self.calculate_energy_for_flying(
                    self.position, get_closest_station_to_drone(self, self.stations, StationType.LOAD)
                )
        else:  # return to station to pickup
            additional_cost = self.calculate_energy_for_flying(
                self.position, get_closest_station_to_drone(self, self.stations, StationType.LOAD)
            )
        flying_to_mission_cost = self.calculate_energy_for_flying(self.position, mission.get_closest_position())
        return additional_cost + flying_to_mission_cost


# по сути функция поиск мастера
def drone_with_max_fly(list: List[Drone]) -> Drone:
    return max(list, key=lambda d: d.time_fly)
