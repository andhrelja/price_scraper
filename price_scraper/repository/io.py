from typing import Iterable
from pathlib import Path
import os
import csv

from .base import Repository
from ..config import BASE_DIR

REPOSITORY_IO_PATH = Path(os.getenv("REPOSITORY_IO_PATH", BASE_DIR.parent / "data"))


class IORepository(Repository):
    mode: str = "a+"
    encoding: str = "utf-8"
    file_ext: str = ".csv"

    def __init__(self, table_name: str, **kwargs) -> None:
        self.file_path = REPOSITORY_IO_PATH / (table_name + self.file_ext)
        self.header = kwargs.get("header", [])
        self.delimiter = kwargs.get("delimiter", ",")
        self.newline = kwargs.get("newline", "\n")

    def add(self, row: str) -> None:
        with open(
            self.file_path, mode=self.mode, encoding=self.encoding, newline=self.newline
        ) as fp:
            dw = csv.DictWriter(f=fp, fieldnames=self.header, delimiter=self.delimiter)
            dw.writerow(row)

    def list(self) -> Iterable:
        with open(
            self.file_path, mode="r", encoding=self.encoding, newline=self.newline
        ) as fp:
            dr = csv.DictReader(f=fp, fieldnames=self.header, delimiter=self.delimiter)
            return list(dr)
