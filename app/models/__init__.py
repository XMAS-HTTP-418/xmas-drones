from typing import Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np


class LoadType(str, Enum):
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


class StationType(Enum):
    LOAD: str = 'LOAD'
    RECHARGE: str = 'RECHARGE'


@dataclass
class Station:
    id: int
    position: np.array
    type: StationType
