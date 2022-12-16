from app.drones.drone import Drone
from models import LoadType, Station, StationType
import numpy as np

# Перекинуть из utils к дронам
def get_closest_station_to_drone(drone: Drone, stations: list[Station], station_type: StationType):
    return min(
        filter(lambda x: x.type == station_type, stations),
        key=lambda x: np.inner((drone.position - x.position), (drone.position - x.position)),
    )
