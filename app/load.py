from typing import Optional
from dataclasses import dataclass
from enum import Enum

class LoadType(Enum, str):
    SPRAYING_SYSTEM = 'SPRAYING_SYSTEM'
    LIDAR = 'LIDAR'
    HD_CAMERA = 'HD_CAMERA'
    VIDEO_CAMERA = 'VIDEO_CAMERA'
    CARGO = 'CARGO'
    GEORADAR = 'GEORADAR'

@dataclass
class Load:
    id: int
    type: LoadType
    power: Optional[float]
    mass: float
    used: Optional[float]
    rate: Optional[float]