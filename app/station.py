import numpy as np
from dataclasses import dataclass

@dataclass
class Station:
    id: int
    position: np.array
    energy: float
    load_ids: list[int]

