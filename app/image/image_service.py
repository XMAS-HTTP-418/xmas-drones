from PIL import Image
from enum import Enum
from typing import NamedTuple

# import cv2
import numpy as np

from config import (
    MIN_COLOR_VALUE,
    MISSION_AREA_IMAGE,
    TARGETS_POLLINATING_IMAGE,
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
    def __init__(self, mission_targets: str = TARGETS_POLLINATING_IMAGE, target_type: TargetType | None = None) -> None:
        self.mission_area = self.read_image(MISSION_AREA_IMAGE)
        self.mission_targets_image = mission_targets
        self.mission_targets = self.read_image(mission_targets)
        self.target_type: TargetType | None = target_type
        self.target_shell_list = {}
        self.target_coords = self.__targets_coords()

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

    def __targets_coords(self) -> list[Point]:
        """
        Получаем координаты цели
        """
        target_coords = []
        first_subtask = {}
        image = self.read_image(self.mission_targets_image)
        for i, row in enumerate(image):
            target_shell = []
            j = 0
            while j < len(row) - 1:
                sublist = []
                while (row[j] != COLOR_DICT_HSV['white']).any() and (row[j] != COLOR_DICT_HSV['black']).any():
                    # Определение типа миссии по цвету
                    if not self.target_type:
                        if (row[j] == COLOR_DICT_HSV['green']).all():
                            self.target_type = TargetType.POLLINATION
                        elif (row[j] == COLOR_DICT_HSV['red']).all():
                            self.target_type = TargetType.SCANNING

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
                find_key = None
                if not self.target_shell_list:
                    self.target_shell_list[i] = {i: sublist}

                for key, value in self.target_shell_list.items():
                    if sublist in value.values() and key == i - 1:
                        find_key = key
                        break

                if find_key is not None:
                    item = self.target_shell_list.get(find_key)
                    if item is not None:
                        self.target_shell_list[find_key] = {**item | {i: sublist}}
                    else:
                        self.target_shell_list[find_key] = {i: sublist}
                        

                for x_value in (max(sublist), min(sublist)):
                    target_coords.append(Point(x=i, y=x_value))

        if not self.target_type:
            raise RuntimeError('He определён тип миссии')
        return target_coords

    @staticmethod
    def get_color_value(color_list):
        """
        Получить цвет для визуализации
        Минимальное значение - 255, 255, 255 (0м)
        Максимальное - 0, 0, 0
        """
        return MIN_COLOR_VALUE - np.sum(color_list)
