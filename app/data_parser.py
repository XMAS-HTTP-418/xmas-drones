import json
import numpy as np
from mission import Mission, MissionType
from drone import Drone
from load import Load, LoadType
from station import Station


class DataParser:
    drones: list[Drone]
    loads: list[Load]
    missions: list[Mission]
    stations: list[Station]

    @staticmethod
    def __parse_drone(raw: dict) -> Drone:
        raw.setdefault(None)
        return Drone(
            id=raw['id'],
            position=np.array(raw['position']),
            velocity=np.array(raw['velocity']),
            mass=raw['mass'],
            max_load=raw['max_load'],
            battery=raw['battery'],
            max_battery=raw['max_battery'],
            is_master=raw['is_master'],
            load_id=raw['load_id'],
            task_id=raw['task_id'],
        )

    @staticmethod
    def __parse_load(raw: dict) -> Load:
        raw.setdefault(None)
        return Load(
            id=raw['id'],
            type=LoadType[raw['type']],
            power=raw['power'],
            mass=raw['mass'],
            used=raw['used'],
            rate=raw['rate'],
        )

    @staticmethod
    def __parse_mission(raw: dict) -> Mission:
        raw.setdefault(None)
        return Mission(
            id=raw['id'],
            type=MissionType[raw['type']],
            priority=raw['priority'],
            periodic=raw['periodic'],
            progress=raw['progress'],
        )

    @staticmethod
    def __parse_station(raw: dict) -> Station:
        raw.setdefault(None)
        return Station(id=raw['id'], position=np.array(raw['position']), energy=raw['energy'], load_ids=raw['load_ids'])

    @classmethod
    def load_data(cls, filename: str) -> None:
        data = json.load(open(filename))
        cls.drones = [cls.__parse_drone(raw) for raw in data['drones']]
        cls.loads = [cls.__parse_load(raw) for raw in data['loads']]
        cls.missions = [cls.__parse_mission(raw) for raw in data['missions']]
        cls.stations = [cls.__parse_station(raw) for raw in data['stations']]

    @classmethod
    def get_closest_station_by_load_type(cls, drone: Drone, load_type: LoadType):
        return min(
            list(filter(lambda x: load_type in [load.type for load in cls.loads if load.id in x.load_ids])),
            key=lambda x: np.inner((drone.position - x.position), (drone.position - x.position)),
        )

    @classmethod
    def get_closest_station_to_drone(cls, drone: Drone):
        return min(cls.stations, key=lambda x: np.inner((drone.position - x.position), (drone.position - x.position)))
