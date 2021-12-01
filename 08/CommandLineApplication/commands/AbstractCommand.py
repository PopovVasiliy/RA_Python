from abc import abstractmethod

from notes.Storage import AbstractStorage


class AbstractCommand(object):
    def __init__(self, storage: AbstractStorage):
        self._storage = storage

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def can_execute(self, command: str) -> bool:
        pass

    @abstractmethod
    def execute(self):
        pass
