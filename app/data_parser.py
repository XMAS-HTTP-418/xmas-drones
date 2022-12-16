import json
import numpy as np
from task import Task, TaskType
from drone import Drone
from load import Load, LoadType
from station import Station, StationType


class DataParser:
    drones: list[Drone]
    loads: list[Load]
    missions: list[Task]
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
    def __parse_mission(raw: dict) -> Task:
        raw.setdefault(None)
        return Task(
            id=raw['id'],
            type=TaskType[raw['type']],
            priority=raw['priority'],
            periodic=raw['periodic'],
            progress=raw['progress'],
        )

    @staticmethod
    def __parse_station(raw: dict) -> Station:
        raw.setdefault(None)
        return Station(id=raw['id'], position=np.array(raw['position']), type=StationType.RECHARGE)

    @classmethod
    def load_data(cls, data:dict) -> None:
        cls.drones = [cls.__parse_drone(raw) for raw in data['drones']]
        cls.loads = [cls.__parse_load(raw) for raw in data['loads']]
        cls.missions = [cls.__parse_mission(raw) for raw in data['missions']]
        cls.stations = [cls.__parse_station(raw) for raw in data['stations']]


