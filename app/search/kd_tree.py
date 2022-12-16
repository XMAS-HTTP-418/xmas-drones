import operator
from typing import NamedTuple

from config import POINT_LIST


class BT(NamedTuple):
    """
    Бинарное дерево со значением узла, левым и правым поддеревом
    """

    value: int
    left: int
    right: int


class NNRecord(NamedTuple):
    """
    Используется для отслеживания текущего наилучшего предположения во время ближайшего
    поиска соседей.
    """

    point: int
    distance: int


def SED(X, Y):
    """Compute the squared Euclidean distance between X and Y."""
    return sum((i - j) ** 2 for i, j in zip(X, Y))


def kdtree(points):
    """
    Создаёт kd дерево из итерируемого набора точек
    """
    k = len(points[0])

    def build(*, points: list, depth):
        """
        Строим kd дерево из набора точек в заданной глубине
        Build a k-d tree from a set of points at a given
        depth.
        """
        if len(points) == 0:
            return None

        points.sort(key=operator.itemgetter(depth % k))
        middle = len(points) // 2

        return BT(
            value=points[middle],
            left=build(
                points=points[:middle],
                depth=depth + 1,
            ),
            right=build(
                points=points[middle + 1 :],
                depth=depth + 1,
            ),
        )

    return build(points=list(points), depth=0)


def find_nearest_neighbor(*, tree: BT, point: NNRecord):
    """
    Поиск ближайшего соседа в дереве kd для данной точки.
    """
    k = len(point)

    best: NNRecord | None = None

    def search(*, tree: BT, depth):
        """
        Рекурсивный поиск сквозь kd дерево для поиска ближайших соседей
        """
        nonlocal best

        if tree is None:
            return

        distance = SED(tree.value, point)
        if best is None or distance < best.distance:
            best = NNRecord(point=tree.value, distance=distance)

        axis = depth % k
        diff = point[axis] - tree.value[axis]
        if diff <= 0:
            close, away = tree.left, tree.right
        else:
            close, away = tree.right, tree.left

        search(tree=close, depth=depth + 1)
        if diff**2 < best.distance:
            search(tree=away, depth=depth + 1)

    search(tree=tree, depth=0)
    return best.point


def nearest_neighbor_kdtree(*, query_points: POINT_LIST, reference_points: POINT_LIST):
    """
    Используя kd дерево, решаем проблему ближайших соседей
    """
    tree = kdtree(reference_points)
    return {query_p: find_nearest_neighbor(tree=tree, point=query_p) for query_p in query_points}
