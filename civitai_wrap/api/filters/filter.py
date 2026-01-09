from abc import ABC, abstractmethod

class Filter(ABC):
    @abstractmethod
    def __call__(self, item):
        pass