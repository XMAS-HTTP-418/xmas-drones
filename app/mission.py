from typing import Optional
from dataclasses import dataclass
import numpy as np
from enum import Enum

class MissionType(Enum):
    SPRAYING_SYSTEM: str = 'SPRAYING_SYSTEM'
    LIDAR: str = 'LIDAR'
    HD_CAMERA: str = 'HD_CAMERA'
    VIDEO_CAMERA: str = 'VIDEO_CAMERA'
    CARGO: str = 'CARGO'
    GEORADAR: str = 'GEORADAR'

@dataclass
class Mission:
    id: int
    type: MissionType
    priority: int
    periodic: float
    progress: Optional[float]

    def get_closest_position(self) -> np.array:
        pass