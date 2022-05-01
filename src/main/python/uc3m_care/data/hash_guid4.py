import uuid
from .attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import Mess_Attr, Correct_Pattern

class Uuid(Attribute):
    def __init__(self, guid: str)-> None:
        self._validation_pattern = Correct_Pattern.UUID_PATTERN.value
        self._error_message = Mess_Attr.MESS_UUID_INVALID.value
        self._attr_value = self._validate(guid)

    def _validate(self, guid: str) -> str:
        """Method for validating uuid  v4"""
        try:
            my_uuid = uuid.UUID(guid)
            super()._validate(guid)
        except ValueError as value_error:
            raise VaccineManagementException(Mess_Attr.MESS_NOT_UUID.value) from value_error
        return guid
