from typing import NamedTuple

import cv2
import numpy as np

from config import MIN_COLOR_VALUE, MISSION_AREA_IMAGE, MISSION_TARGETS_IMAGE, WHITE_COLOR, BLACK_COLOR

# Черный цвет соответствует минимальной высоте (0 м), белый – максимальной
class Point(NamedTuple):
    x: int
    y: int
    
    def __repr__(self) -> str:
        return f'({self.x},{self.y})'

class ImageService:

    def __init__(self) -> None:
        self.mission_area = cv2.imread(MISSION_AREA_IMAGE)
        self.mission_targets = cv2.imread(MISSION_TARGETS_IMAGE)
        self.targets_coords = []

    def get_targets_coords(self) -> list[Point]:
        """
        Получаем координаты цели
        """
        image = cv2.imread(MISSION_TARGETS_IMAGE)
        for i, row in enumerate(image):
            for j, color_list in enumerate(row):
                if (color_list != WHITE_COLOR).any() and (color_list != BLACK_COLOR).any():
                    self.targets_coords.append(Point(x=i, y=j))

        return self.targets_coords
    
    def overlay_images(self):
        ...

    @staticmethod
    def get_color_value(color_list):
        """
        Минимальное значение - 255, 255, 255 (0м)
        Максимальное - 0, 0, 0
        """
        return MIN_COLOR_VALUE - np.sum(color_list)


a = ImageService().get_targets_coords()
print(a)