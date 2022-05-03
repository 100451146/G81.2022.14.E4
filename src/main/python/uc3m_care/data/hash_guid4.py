import uuid
from uc3m_care.data.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import MessAttr, CorrectPattern


class Uuid(Attribute):
    def __init__(self, guid: str) -> None:
        super().__init__()
        self._validation_pattern = CorrectPattern.UUID_PATTERN.value
        self._error_message = MessAttr.MESS_UUID_INVALID.value
        self._attr_value = self._validate(guid)

    def _validate(self, guid: str) -> str:
        """Method for validating uuid  v4"""
        try:
            uuid.UUID(guid)
            super()._validate(guid)
        except ValueError as value_error:
            raise VaccineManagementException(MessAttr.MESS_NOT_UUID.value) from value_error
        return guid
