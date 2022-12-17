import numpy as np
from dataclasses import dataclass
from enum import Enum


class StationType(Enum):
    LOAD: str = 'LOAD'
    RECHARGE: str = 'RECHARGE'


@dataclass
class Station:
    id: int
    position: np.array
    type: StationType
