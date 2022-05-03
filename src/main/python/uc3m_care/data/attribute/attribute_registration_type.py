from uc3m_care.enum.enumerations import MessAttr, CorrectPattern
from uc3m_care.data.attribute.attribute import Attribute


class RegistrationType(Attribute):
    def __init__(self, registration_type: str) -> None:
        super().__init__()
        self._validation_pattern = CorrectPattern.REGISTRATION_PATTERN.value
        self._error_message = MessAttr.MESS_REGISTRATION_INVALID.value
        self._attr_value = self._validate(registration_type)
