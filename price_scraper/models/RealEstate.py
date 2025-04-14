from dataclasses import dataclass, field
from datetime import datetime

from price_scraper.models.base import JSONMeta


@dataclass
class RealEstate(JSONMeta):
    name: str
    description: str
    type: str
    type_extended: str
    source: str
    location: str
    price: float
    square_m: float
    square_property_m: float
    wood_shed: str = None
    garage: str = None
    parking: str = None
    balcony: str = None
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def price_per_square_m(self) -> float:
        return self.price / self.square_m
