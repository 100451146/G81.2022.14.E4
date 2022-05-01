from .attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import Mess_Attr

class Age(Attribute):
    def __init__(self, age: int)-> None:
        self._validation_pattern = None
        self._error_message = Mess_Attr.MESS_AGE_INVALID.value
        self._attr_value = self._validate(age)

    def _validate(self, age: int) -> int:
        if age.isnumeric():
            if (int(age) < 6 or int(age) > 125):
                raise VaccineManagementException(Mess_Attr.MESS_AGE_INVALID.value)
        else:
            raise VaccineManagementException(Mess_Attr.MESS_AGE_INVALID.value)
        return age
