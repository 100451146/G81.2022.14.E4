
from .attribute import Attribute

class FullName(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
        self._error_message = "name surname is not valid"
        self._attr_value = self._validate(attr_value)