import abc


class Repository(abc.ABC):
    @abc.abstractmethod
    def add(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> None:
        raise NotImplementedError
