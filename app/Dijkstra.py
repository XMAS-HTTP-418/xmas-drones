from heapq import heappop, heappush
from PIL import Image
import numpy as np


def getArrayHeightMap() -> np.ndarray:
    im = Image.open('map.bmp').convert("L")  # Can be many different formats.
    data = iter(im.getdata())
    rows, cows = im.size

    return np.array(
        tuple(np.array(tuple(next(data) for j in range(cows)), dtype="uint8") for i in range(rows))
    )


class Node:
    __slots__ = "row", "cow", "cost"

    def __init__(self, row, cow, cost):
        self.row = row
        self.cow = cow
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


class Dijkstra:
    def __init__(self, heightMap, start=(0, 0)):
        self.start = start
        self.kRowCow = tuple(zip((-1, -1, -1, 0, 1, 1, 1, 0), (-1, 0, 1, 1, 1, 0, -1, -1)))
        self.size = (len(heightMap), len(heightMap[0]))
        self.heightMap = heightMap
        self.distances = np.array(tuple(np.array([1 << 30] * self.size[0])
                                        for _ in range(self.size[1])))
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
        dct = dict()
        heappush(OPEN, Node(self.start[0], self.start[1], int(self.heightMap[self.start])))
        # mx = self.size[0]*self.size[1]
        while OPEN:
            cur: Node = heappop(OPEN)
            if using[cur.row][cur.cow]:
                continue
            using[cur.row][cur.cow] = 1
            self.distances[cur.row][cur.cow] = cur.cost
            for krow, kcow in self.kRowCow:
                i, j = n = self.validate(cur.row + krow, cur.cow + kcow)
                if not using[i][j]:
                    h = np.sqrt(
                        np.square(np.subtract(int(self.heightMap[i][j]), self.heightMap[cur.row][
                            cur.cow])) + 1)
                    heappush(OPEN, Node(i, j, cur.cost + h))
                    lst = dct.get(n, [])
                    heappush(lst, Node(i, j, cur.cost + h))
