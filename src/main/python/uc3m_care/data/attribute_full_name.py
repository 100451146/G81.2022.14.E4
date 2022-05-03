from uc3m_care.enum.enumerations import MessAttr, CorrectPattern
from uc3m_care.data.attribute import Attribute


class FullName(Attribute):
    def __init__(self, full_name: str) -> None:
        super().__init__()
        self._validation_pattern = CorrectPattern.NAME_PATTERN.value
        self._error_message = MessAttr.MESS_NAME_INVALID.value
        self._attr_value = self._validate(full_name)
