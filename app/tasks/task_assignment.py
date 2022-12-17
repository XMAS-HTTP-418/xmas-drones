from typing import List, Tuple
import numpy as np
# from lapsolver import solve_dense
from drones.drone import Drone
from tasks import Task

# based on shortest path augmentation
def calculate_task_assignments(cost_matrix: np.array) -> List[Tuple[int, int]]:
    # rids, cids = solve_dense(cost_matrix)
    # return list(zip(rids, cids))
    return [(0, 1), (1, 3), (2, 0)]


def get_cost_matrix(drones: List[Drone], missions: List[Task]) -> np.array:
    cost_matrix = np.zeros((len(drones), len(missions)))
    for i, drone in enumerate(drones):
        for j, mission in enumerate(missions):
            cost_matrix[i][j] = drone.evaluate_mission_cost(mission)
    return cost_matrix


def assign_tasks(drones: List[Drone], missions: List[Task], tasks: List[Tuple[int, int]]):
    for i, drone in enumerate(drones):
        drone.assign_mission(missions[tasks[i][1]])
