from typing import Optional
import numpy as np
from mission import Mission
from station import Station
from load import LoadType, Load
from dataclasses import dataclass

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
    load_id: int | None
    mission_id: int | None
    load: Optional[Load]

    def calculate_energy_for_flying(self, start_position: np.array, end_position: np.array) -> float:
        pass

    def get_closest_station(self) -> Station:
        pass

    def get_closest_station_with_load_type(self, load_type: LoadType) -> Station:
        pass

    def evaluate_mission_cost(self, mission: Mission) -> np.float:
        additional_cost = 0.0
        if self.load_id:
            if self.load.type == LoadType[mission.type]:
                additional_cost = 0.0
            else: # return to station to store and pickup
                additional_cost = self.calculate_energy_for_flying(self.position, self.get_closest_station())
                additional_cost += self.calculate_energy_for_flying(self.get_closest_station(), self.get_closest_station_with_load_type(LoadType[mission.type]))
        else: # return to station to pickup
            additional_cost = self.calculate_energy_for_flying(self.position, self.get_closest_station_with_load_type(LoadType[mission.type]))
        flying_to_mission_cost = self.calculate_energy_for_flying(self.position, mission.get_closest_position())
        return additional_cost + flying_to_mission_cost



