import abc

class Repository(abc.ABC):
    @abc.abstractmethod
    def add(self) -> None:
        raise NotImplemented
    
    @abc.abstractmethod
    def list(self) -> None:
        raise NotImplemented
