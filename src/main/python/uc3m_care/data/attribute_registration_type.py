from uc3m_care.enum.enumerations import Mess_Attr, Correct_Pattern
from .attribute import Attribute

class RegistrationType(Attribute):
    def __init__(self, registration_type: str)-> None:
        self._validation_pattern = Correct_Pattern.REGISTRATION_PATTERN.value
        self._error_message = Mess_Attr.MESS_REGISTRATION_INVALID.value
        self._attr_value = self._validate(registration_type)


