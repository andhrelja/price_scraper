from dataclasses import dataclass, field
from datetime import datetime

from price_scraper.models.base import JSONMeta


@dataclass
class Product(JSONMeta):
    name: str
    short_name: str
    source: str
    price: float
    created_at: datetime = field(default_factory=datetime.now)
    product_type: str = None
