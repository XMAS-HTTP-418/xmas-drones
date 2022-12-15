from typing import Union
import numpy as np
from mission import Mission
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

    def evaluate_mission_cost(self, mission: Mission) -> np.float:
        pass

