from dataclasses import dataclass, asdict, field
from datetime import datetime

import json

class JSONMeta:
    def asdict(self):
        return asdict(self)

    def __repr__(self) -> str:
        return json.dumps(self.asdict(), indent=2)


@dataclass
class Product(JSONMeta):
    name: str
    short_name: str
    source: str
    price: float
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def header(self):
        keys = self.asdict().keys()
        return list(keys)