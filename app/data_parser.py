from typing import Tuple, List
from json import load
import numpy as np
from mission import Mission, MissionType
from drone import Drone
from load import Load, LoadType
from station import Station

def parse_drone(raw: dict) -> Drone:
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
        task_id=raw['task_id']
    )

def parse_load(raw: dict) -> Load:
    raw.setdefault(None)
    return Load(
        id=raw['id'],
        type=LoadType[raw['type']],
        power=raw['power'],
        mass=raw['mass'],
        used=raw['used'],
        rate=raw['rate']
    )

def parse_mission(raw: dict) -> Mission:
    raw.setdefault(None)
    return Mission(
        id=raw['id'],
        type=MissionType[raw['type']],
        priority=raw['priority'],
        periodic=raw['periodic'],
        progress=raw['progress']
    )

def parse_station(raw: dict) -> Station:
    raw.setdefault(None)
    return Station(
        id=raw['id'],
        position=np.array(raw['position']),
        energy=raw['energy'],
        load_ids=raw['load_ids']
    )

def load_data(filename: str) -> Tuple[List[Drone],List[Mission],List[Load], List[Station]]:
    data = load(open(filename))
    drones = [parse_drone(raw) for raw in data['drones']]
    loads = [parse_load(raw) for raw in data['loads']]
    missions = [parse_mission(raw) for raw in data['missions']]
    stations = [parse_station(raw) for raw in data['stations']]
    return (drones,missions,loads,stations)