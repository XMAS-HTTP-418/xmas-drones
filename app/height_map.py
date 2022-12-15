import cv2
import numpy as np

from config import MIN_COLOR_VALUE

# Черный цвет соответствует минимальной высоте (0 м), белый – максимальной

def get_mission_area():
    image = cv2.imread("data/mission_area.png")
    return image


def get_color_value(color_list):
    """
    Минимальное значение - 255, 255, 255 (0м)
    Максимальное - 0, 0, 0
    """
    return MIN_COLOR_VALUE - np.sum(color_list)