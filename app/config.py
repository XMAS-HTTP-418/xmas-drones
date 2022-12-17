import numpy as np


# image files
MISSION_AREA_IMAGE = 'data/mission_area.png'
TARGETS_SCANNING_IMAGE = 'data/targets_scanning.png'
TARGETS_POLLINATING_IMAGE = 'data/targets_pollinating.png'

# colors
MIN_COLOR_VALUE = 255 + 255 + 255

# словарь для поиска нужных значений цветов
COLOR_DICT_HSV = {
    'black': np.array([0, 0, 0], dtype='uint8'),
    'white': np.array([255, 255, 255], dtype='uint8'),
    'red': np.array([125, 0, 0], dtype='uint8'),
    'green': np.array([174, 174, 174], dtype='uint8'),
}

# distance
DISTANCE_ARRIVAL_THRESHOLD = 3
DRONE_BATTERY_THRESHOLD = 10.0

# sockets
SOCKET_HOST = "127.0.0.1"  # The server's hostname or IP address
SOCKET_PORT = 65438  # The port used by the server


# ALIASES

POINT = tuple[int, int]
POINT_LIST = list[POINT]


# SOCKETS

DATA_PACKAGE_ENCODING = "utf-8"
DATA_CLOSING_SEQUENCE = b"\r\n\r\n"
DATA_PACKAGE_SIZE = 1024
TIME_FORMAT = "%H:%M:%S"
TIME_PING = 10
TIME_DRONE = 25
TIME_MASTER = TIME_PING * 4 
