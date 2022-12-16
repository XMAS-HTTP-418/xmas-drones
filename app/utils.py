from drone import Drone
from load import LoadType
import numpy as np
from station import Station, StationType


def get_closest_station_to_drone(drone: Drone, stations: list[Station], station_type: StationType):
        return min(filter(lambda x: x.type == station_type, stations), key=lambda x: np.inner((drone.position - x.position), (drone.position - x.position)))