from typing import Iterable, Union
from sqlalchemy import create_engine

from .base import Repository
from ..config import BASE_DIR
from ..models.db import metadata_obj, product

SQLITE_DIR = BASE_DIR / "data"


class SqLiteRepository(Repository):
    database_name = __package__

    def __init__(self, table_name: Union[str, None] = None, **kwargs) -> None:
        self.session = create_engine(
            "sqlite://{}".format(SQLITE_DIR / self.database_name + ".db")
        )
        instance = self.session.query(product).first()
        if not instance:
            metadata_obj.create_all(self.session)

    def add(self, row: str) -> None:
        self.session.add(product, row)

    def list(self) -> Iterable:
        return self.session.query(product)
