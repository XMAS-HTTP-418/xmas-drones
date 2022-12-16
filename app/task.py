from typing import Optional
from dataclasses import dataclass
from image_service import ImageService
import numpy as np
from drone import Drone
from enum import Enum

class TaskType(str, Enum):
    SPRAYING_SYSTEM = 'SPRAYING_SYSTEM'
    LIDAR = 'LIDAR'
    HD_CAMERA = 'HD_CAMERA'
    VIDEO_CAMERA = 'VIDEO_CAMERA'
    CARGO = 'CARGO'
    GEORADAR = 'GEORADAR'

@dataclass
class Task:
    id: int
    type: TaskType
    priority: int
    periodic: float
    progress: Optional[float]

    def get_closest_position(self, drone: Drone) -> np.array:
        imageservice = ImageService()
        nearest_point = imageservice.get_nearest_target([(drone.position[0], drone.position[1])])
        return nearest_point