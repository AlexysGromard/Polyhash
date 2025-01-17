from dataclasses import dataclass
from core.models import Vector3

@dataclass
class sonde:
    path: list[int] #Liste des variations d'altitudes suivies par le ballons (-1, 0, ou 1)
    position: list[Vector3] #Liste des positions des ballons
    score: int #Score marqué par ce ballon