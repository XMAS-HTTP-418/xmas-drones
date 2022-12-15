from typing import Optional
from dataclasses import dataclass
import numpy as np
from enum import Enum

class MissionType(Enum, str):
    SPRAYING_SYSTEM = 'SPRAYING_SYSTEM'
    LIDAR = 'LIDAR'
    HD_CAMERA = 'HD_CAMERA'
    VIDEO_CAMERA = 'VIDEO_CAMERA'
    CARGO = 'CARGO'
    GEORADAR = 'GEORADAR'

@dataclass
class Mission:
    id: int
    type: MissionType
    priority: int
    periodic: float
    progress: Optional[float]

    def get_closest_position(self) -> np.array:
        pass