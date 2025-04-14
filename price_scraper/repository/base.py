import abc


class Repository(abc.ABC):
    def __call__(self, table_name: str, **kwargs) -> "Repository":
        return self.__init__(table_name, **kwargs)

    @abc.abstractmethod
    def add(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_all(self) -> None:
        raise NotImplementedError
