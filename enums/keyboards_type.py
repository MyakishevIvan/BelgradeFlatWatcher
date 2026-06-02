from enum import Enum, auto


class KeyboardType(str, Enum):
    ROOMS = "ROOMS"
    PRICE = "PRICE"
    SQUARE = "SQUARE"
    SEARCH = "SEARCH"
    