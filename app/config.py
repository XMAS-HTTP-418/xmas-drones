import numpy as np


# image files
MISSION_AREA_IMAGE = 'data/mission_area.png'
TARGETS_SCANNING_IMAGE = 'data/targets_scanning.png'
TARGETS_POLLINATION_IMAGE = 'data/targets_pollinating.png'
WHITE_COLOR = np.array([255, 255, 255], dtype='uint8')
BLACK_COLOR = np.array([0, 0, 0], dtype='uint8')


# colors
MIN_COLOR_VALUE = 255 + 255 + 255

# словарь для поиска нужных значений цветов
COLOR_DICT_HSV = {
    'black': np.array([0, 0, 0], dtype='uint8'),
    'white': np.array([255, 255, 255], dtype='uint8'),
    'red': np.array([0, 0, 125], dtype='uint8'),
    'green': np.array([125, 0, 0], dtype='uint8'),
}

# distance
DISTANCE_ARRIVAL_THRESHOLD = 3
DRONE_BATTERY_THRESHOLD = 10.0

# sockets
SOCKET_HOST = "127.0.0.1"  # The server's hostname or IP address
SOCKET_PORT = 65432  # The port used by the server


# ALIASES

POINT = tuple[int, int]
POINT_LIST = list[POINT]


# SOCKETS

dataPackageEncoding = "utf-8"
dataClosingSequence = b"\r\n\r\n"
dataPackageSize = 1024
timeFormat = "%H:%M:%S"