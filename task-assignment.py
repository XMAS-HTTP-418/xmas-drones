from typing import List, Tuple
from numpy import array
from lapsolver import solve_dense

# based on shortest path augmentation
def calculate_task_assignments(cost_matrix: array) -> List[Tuple[int,int]]:
    rids, cids = solve_dense(cost_matrix)
    return list(zip(rids,cids))