import uuid
from .attribute import Attribute
from uc3m_care.vaccine_management_exception import VaccineManagementException

class Uuid(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]"\
                                   "{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
        self._error_message = "UUID invalid"
        self._attr_value = self._validate(attr_value)


    def _validate(self, attr_value: str)-> str:
        "Method for validating uuid  v4"
        try:
            my_uuid = uuid.UUID(attr_value)
            super()._validate(attr_value)
        except ValueError as value_error:
            raise VaccineManagementException ("Id received is not a UUID") from value_error
        return attr_value