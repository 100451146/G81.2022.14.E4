import uuid
from .attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class Uuid(Attribute):
    def __init__(self, guid: str)-> None:
        self._validation_pattern = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]" \
                                   "{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
        self._error_message = "UUID invalid"
        self._attr_value = self._validate(guid)

    def _validate(self, guid: str) -> str:
        """Method for validating uuid  v4"""
        try:
            my_uuid = uuid.UUID(guid)
            super()._validate(guid)
        except ValueError as value_error:
            raise VaccineManagementException("Id received is not a UUID") from value_error
        return guid
