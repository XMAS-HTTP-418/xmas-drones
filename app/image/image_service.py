from PIL import Image
from enum import Enum
from typing import NamedTuple

# import cv2
import numpy as np

from config import (
    MIN_COLOR_VALUE,
    MISSION_AREA_IMAGE,
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
        self.mission_area = self.read_image(MISSION_AREA_IMAGE)
        self.mission_targets_image = mission_targets
        self.mission_targets = self.read_image(mission_targets)
        self.target_type: TargetType | None = None
        self.__target_coords = []

    @staticmethod
    def read_image(filename: str) -> np.array:
        """
        filename: str - название файла
        return np.array - трёхмерный массив image[x][y] == color
        """
        im = Image.open(filename).convert("RGB")
        data = iter(im.getdata())
        rows, cows = im.size
        return np.array(tuple(np.array(tuple(next(data) for j in range(cows)), dtype="uint8") for i in range(rows)))

    @property
    def targets_coords(self) -> list[Point]:
        """
        Получаем координаты цели
        """
        image = self.read_image(self.mission_targets_image)
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

    @staticmethod
    def get_color_value(color_list):
        """
        Получить цвет для визуализации
        Минимальное значение - 255, 255, 255 (0м)
        Максимальное - 0, 0, 0
        """
        return MIN_COLOR_VALUE - np.sum(color_list)
