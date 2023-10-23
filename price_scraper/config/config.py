from dataclasses import dataclass, asdict
from pathlib import Path

import json

class Meta:
    def asdict(self):
        return asdict(self)
    
    def __repr__(self) -> str:
        return json.dumps(self.asdict(), indent=2)


BASE_DIR = Path.resolve(Path(__file__)).parent.parent


@dataclass
class Config(Meta):
    product_name: str
    jobs: list

@dataclass
class Job(Meta):
    is_active: bool
    service: str
    protocol: str
    parser: str
    host: str
    port: str
    prefix: str


