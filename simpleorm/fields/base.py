from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, field_type):
        self.type = field_type

    def __str__(self):
        return f"{self.__class__.__name__}({self.type.__name__})"

    @abstractmethod
    def validate(self, value):
        pass
