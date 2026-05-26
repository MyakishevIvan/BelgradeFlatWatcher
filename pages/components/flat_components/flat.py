from dataclasses import dataclass
from datetime import date


@dataclass
class Flat:
    id: int
    url: str
    name: str
    price: str
    square: str
    publication_date: date

    def __str__(self):
        return (
            f'<a href="{self.url}">{self.name}</a>\n'
            f'id: {self.id}\n'
            f'price: {self.price}\n'
            f'square: {self.square}\n'
            f'publication date: {self.publication_date}\n'
        )
