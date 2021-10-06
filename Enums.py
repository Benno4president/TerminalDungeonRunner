from enum import Enum


class Kind(Enum):
    FRIENDLY = 0
    ENEMY = 1


class Direction(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class EntType(Enum):
    OBJECT = 0
    PLAYER = 1
    ENEMY = 2
    BULLET = 3
    COIN = 4
    WALL = 5
    TRIGGER = 6
    SHOP = 7
    FLOOR = 8

