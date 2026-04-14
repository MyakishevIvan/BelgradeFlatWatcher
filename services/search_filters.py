from dataclasses import dataclass

ROOMS_MAP = {
    "1": "jednosoban",
    "2": "dvosoban",
    "3": "trosoban",
}

@dataclass(frozen=True)
class SearchFilters:
    min_price: str
    max_price: str
    min_square: str
    max_square: str
    rooms_count: str

    def __post_init__(self):
        if self.rooms_count not in ROOMS_MAP:
            raise ValueError(
                f"rooms_count must be one of {list(ROOMS_MAP)}, "
                f"got {self.rooms_count}"
            )
    
    @property
    def room_type(self) -> str:
        return ROOMS_MAP[self.rooms_count]

    def __str__(self) -> str:
        return (
            f"Searching by filter:\n"
            f"price: {self.min_price}-{self.max_price}\n"
            f"rooms count: {self.rooms_count}\n"
            f"square: {self.min_square}-{self.max_square}"
        )