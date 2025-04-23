from .base import Field

class IntegerField(Field):
    def __init__(self):
        super().__init__(int)

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected an integer value")
