import numpy as np


MIN_COLOR_VALUE = 255 + 255 + 255
MISSION_AREA_IMAGE = 'data/mission_area.png'
TARGETS_SCANNING_IMAGE = 'data/targets_scanning.png'
TARGETS_POLLINATION_IMAGE = 'data/targets_pollinating.png'
WHITE_COLOR = np.array([255, 255, 255], dtype='uint8')
BLACK_COLOR = np.array([0, 0, 0], dtype='uint8')

DISTANCE_ARRIVAL_THRESHOLD = 3
DRONE_BATTERY_THRESHOLD = 10.0

SOCKET_HOST = "127.0.0.1"  # The server's hostname or IP address
SOCKET_PORT = 65432  # The port used by the server

COLOR_DICT_HSV = {
    'black': [[180, 255, 30], [0, 0, 0]],
    'white': [[180, 18, 255], [0, 0, 231]],
    'red1': [[180, 255, 255], [159, 50, 70]],
    'red2': [[9, 255, 255], [0, 50, 70]],
    'green': [[89, 255, 255], [36, 50, 70]],
    'blue': [[128, 255, 255], [90, 50, 70]],
    'yellow': [[35, 255, 255], [25, 50, 70]],
    'purple': [[158, 255, 255], [129, 50, 70]],
    'orange': [[24, 255, 255], [10, 50, 70]],
    'gray': [[180, 18, 230], [0, 0, 40]],
}

# ALIASES

POINT = tuple[int, int]
POINT_LIST = list[POINT]