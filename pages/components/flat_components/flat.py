from dataclasses import dataclass
from datetime import date


@dataclass
class Flat:
    url: str
    name: str
    price: str
    square: str
    publication_date: date
