from .attribute import Attribute
from uc3m_care.vaccine_management_exception import VaccineManagementException


class Age(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = None
        self._error_message = "age is not valid"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value: int) -> int:
        if attr_value.isnumeric():
            if (int(attr_value) < 6 or int(attr_value) > 125):
                raise VaccineManagementException("age is not valid")
        else:
            raise VaccineManagementException("age is not valid")
        return attr_value
