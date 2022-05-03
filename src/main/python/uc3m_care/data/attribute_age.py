from uc3m_care.data.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import MessAttr


class Age(Attribute):
    def __init__(self, age: str) -> None:
        super().__init__()
        self._validation_pattern = None
        self._error_message = MessAttr.MESS_AGE_INVALID.value
        self._attr_value = self._validate(age)

    def _validate(self, age: str) -> str:
        if age.isnumeric():
            if int(age) < 6 or int(age) > 125:
                raise VaccineManagementException(MessAttr.MESS_AGE_INVALID.value)
        else:
            raise VaccineManagementException(MessAttr.MESS_AGE_INVALID.value)
        return age
