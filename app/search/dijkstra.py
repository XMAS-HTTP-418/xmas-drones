from heapq import heappop, heappush
from PIL import Image
import numpy as np
from typing import List


def get_array_height_map(filename: str) -> np.ndarray:
    im = Image.open(filename).convert("L")  # Can be many different formats.
    data = iter(im.getdata())
    rows, cows = im.size

    return np.array(tuple(np.array(tuple(next(data) for j in range(cows)), dtype="uint8") for i in range(rows)))


class Node:
    __slots__ = "row", "cow", "cost"

    def __init__(self, row, cow, cost):
        self.row = row
        self.cow = cow
        self.cost = cost

    def __lt__(self, other: 'Node'):
        return self.cost < other.cost


class Dijkstra:
    """Алгоритм Дейкстры"""
    def __init__(self, heightMap, start=(0, 0)):
        self.start = start
        self.kRowCow = tuple(zip((-1, -1, -1, 0, 1, 1, 1, 0), (-1, 0, 1, 1, 1, 0, -1, -1)))
        self.size = (len(heightMap), len(heightMap[0]))
        self.heightMap = heightMap
        self.distances = np.array(tuple(np.array([1 << 30] * self.size[0]) for _ in range(self.size[1])))
        self.run()

    def validate(self, row, cow) -> tuple:
        if row < 0:
            row = 0
        elif row >= self.size[0]:
            row = self.size[0] - 1
        if cow < 0:
            cow = 0
        elif cow >= self.size[1]:
            cow = self.size[1] - 1
        return row, cow

    def run(self):
        using = np.array(tuple(np.zeros(self.size[0], dtype="uint8") for _ in range(self.size[1])))
        OPEN = list()
        heappush(OPEN, Node(self.start[0], self.start[1], int(self.heightMap[self.start])))
        while OPEN:
            cur: Node = heappop(OPEN)
            if using[cur.row][cur.cow]:
                continue
            using[cur.row][cur.cow] = 1
            self.distances[cur.row][cur.cow] = cur.cost
            for krow, kcow in self.kRowCow:
                i, j = self.validate(cur.row + krow, cur.cow + kcow)
                if not using[i][j]:
                    h = np.sqrt(np.square(np.subtract(int(self.heightMap[i][j]), self.heightMap[cur.row][cur.cow])) + 1)
                    heappush(OPEN, Node(i, j, cur.cost + h))

    def get_nearest_minimum_coordinates(self, cur: tuple) -> tuple:
        mn = self.distances[cur]
        ans = cur
        for krow, kcow in self.kRowCow:
            nx = self.validate(cur[0] + krow, cur[1] + kcow)
            if self.distances[nx] < mn:
                mn = self.distances[nx]
                ans = nx
        return ans

    def get_route(self, cur: tuple) -> List[tuple]:
        route = [cur]
        while cur != self.start:
            cur = self.get_nearest_minimum_coordinates(cur)
            route.append(cur)
        route.reverse()
        return route

    def get_distances(self, cur: tuple) -> int:
        return self.distances[cur]
