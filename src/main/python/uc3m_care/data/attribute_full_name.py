from uc3m_care.enum.enumerations import Mess_Attr, Correct_Pattern
from .attribute import Attribute

class FullName(Attribute):
    def __init__(self, full_name: str)-> None:
        self._validation_pattern = Correct_Pattern.NAME_PATTERN.value
        self._error_message = Mess_Attr.MESS_NAME_INVALID.value
        self._attr_value = self._validate(full_name)