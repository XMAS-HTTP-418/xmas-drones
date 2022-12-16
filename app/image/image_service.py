from enum import Enum
from typing import NamedTuple

import cv2
import numpy as np
from kd_tree import nearest_neighbor_kdtree

from config import (
    MIN_COLOR_VALUE,
    MISSION_AREA_IMAGE,
    POINT_LIST,
    TARGETS_POLLINATION_IMAGE,
    TARGETS_SCANNING_IMAGE,
    COLOR_DICT_HSV,
)


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


class TargetType(str, Enum):
    SCANNING = 'scanning'
    POLLINATION = 'pollination'


class ImageService:
    def __init__(self, mission_targets: str = TARGETS_SCANNING_IMAGE) -> None:
        self.mission_area = cv2.imread(MISSION_AREA_IMAGE)
        self.mission_targets_image = mission_targets
        self.mission_targets = cv2.imread(mission_targets)
        self.target_type: TargetType | None = None
        self.__target_coords = []

    @property
    def targets_coords(self) -> list[Point]:
        """
        Получаем координаты цели
        """
        image = cv2.imread(self.mission_targets_image)
        for i, row in enumerate(image):
            target_shell = []
            j = 0
            while j < len(row) - 1:
                sublist = []
                while (row[j] != COLOR_DICT_HSV['white']).any() and (row[j] != COLOR_DICT_HSV['black']).any():
                    # if COLOR_DICT_HSV['green'].any():
                    #     self.target_type = TargetType.POLLINATION

                    sublist.append(j)
                    if j < len(row) - 1:
                        j += 1
                    else:
                        sublist.append(j)
                        break
                if sublist:
                    target_shell.append(sublist)
                j += 1

            for sublist in target_shell:
                for x_value in (max(sublist), min(sublist)):
                    self.__target_coords.append(Point(x=i, y=x_value))

        return self.__target_coords

    def get_nearest_target(self, search_points: POINT_LIST):
        return nearest_neighbor_kdtree(query_points=search_points, reference_points=self.targets_coords)

    def overlay_images(self):
        ...

    @staticmethod
    def get_color_value(color_list):
        """
        Минимальное значение - 255, 255, 255 (0м)
        Максимальное - 0, 0, 0
        """
        return MIN_COLOR_VALUE - np.sum(color_list)


if __name__ == "__main__":
    imageservice = ImageService()
    nearest_point = imageservice.get_nearest_target([(20, 2)])
    print(nearest_point)
