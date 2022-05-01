from .attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class Age(Attribute):
    def __init__(self, age):
        self._validation_pattern = None
        self._error_message = "age is not valid"
        self._attr_value = self._validate(age)

    def _validate(self, age: int) -> int:
        if age.isnumeric():
            if (int(age) < 6 or int(age) > 125):
                raise VaccineManagementException("age is not valid")
        else:
            raise VaccineManagementException("age is not valid")
        return age
