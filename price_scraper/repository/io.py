from typing import Iterable
from .base import Repository
from io import StringIO
from io import FileIO

class IORepository(Repository):
    def __init__(self, file_name: str, s_io: StringIO, mode: str='a+') -> None:
        self.f_io = FileIO(file_name, mode=mode)
        self.s_io = s_io
    
    def add(self, row: str) -> None:
        self.s_io.write(row + '\n')
        self.f_io.write(self.s_io.getvalue().encode())
    
    def list(self) -> Iterable:
        self.s_io.seek(0)
        return self.s_io.readlines()
