from dataclasses import asdict, fields
import json


class JSONMeta:
    def asdict(self):
        return asdict(self)

    @classmethod
    def header(cls):
        keys = fields(cls)
        return [key.name for key in keys]

    def __repr__(self) -> str:
        return json.dumps(self.asdict(), indent=2)
