from abc import ABC, abstractmethod

class BaseReader(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
