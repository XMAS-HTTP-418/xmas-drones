import numpy as np


MIN_COLOR_VALUE = 255 + 255 + 255
MISSION_AREA_IMAGE = 'data/mission_area.png'
TARGETS_SCANNING_IMAGE = 'data/targets_scanning.png'
TARGETS_POLLINATION_IMAGE = 'data/targets_pollinating.png'
WHITE_COLOR = np.array([255, 255, 255], dtype='uint8')
BLACK_COLOR = np.array([0, 0, 0], dtype='uint8')

SOCKET_HOST = "127.0.0.1"  # The server's hostname or IP address
SOCKET_PORT = 65432  # The port used by the server
