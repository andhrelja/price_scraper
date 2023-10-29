from typing import Iterable, Union

from .base import Repository

class InMemoryRepository(Repository):
    def __init__(self, table_name: Union[str, None]=None, mode: str='r+', encoding: str='utf-8', **kwargs) -> None:
        self.objects = []
    
    def add(self, row: str) -> None:
        self.objects.append(row)
    
    def list(self) -> Iterable:
        return self.objects
