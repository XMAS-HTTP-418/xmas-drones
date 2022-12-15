from typing import Optional
from dataclasses import dataclass
from enum import Enum

class LoadType(Enum):
    SPRAYING_SYSTEM: str = 'SPRAYING_SYSTEM'
    LIDAR: str = 'LIDAR'
    HD_CAMERA: str = 'HD_CAMERA'
    VIDEO_CAMERA: str = 'VIDEO_CAMERA'
    CARGO: str = 'CARGO'
    GEORADAR: str = 'GEORADAR'

@dataclass
class Load:
    id: int
    type: LoadType
    power: Optional[float]
    mass: float
    used: Optional[float]
    rate: Optional[float]