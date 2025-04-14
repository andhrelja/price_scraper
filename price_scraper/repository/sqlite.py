import os
from typing import Iterable, Union
from sqlalchemy import create_engine, insert

from .base import Repository
from ..config import BASE_DIR
from ..models import db  # import metadata_obj, product, real_estate

DATABASE_JDBC_URL = os.getenv("DATABASE_JDBC_URL", "sqlite:///:memory:")
SQLITE_DIR = BASE_DIR / "data"


class SqLiteRepository(Repository):
    database_name = __package__

    def __init__(self, table_name: Union[str, None] = None, **kwargs) -> None:
        self.session = create_engine(DATABASE_JDBC_URL)

        self.table = getattr(db, table_name, None)
        if not self.table:
            raise ValueError(f"Table '{table_name}' does not exist in the database.")

        instance = self.session.query(self.table).first()
        if not instance:
            db.metadata_obj.create_all(self.session)

    def add(self, row: dict) -> None:
        self.session.add(self.table, row)

    def add_all(self, rows: Iterable) -> None:
        self.session.execute(insert(self.table), rows)

    def list(self) -> Iterable:
        return self.session.query(self.table)

    def delete_all(self) -> None:
        os.remove(SQLITE_DIR / self.database_name + ".db")
