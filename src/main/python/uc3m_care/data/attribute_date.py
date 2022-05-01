from .attribute import Attribute
from datetime import datetime
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import Mess_Attr

class Date(Attribute):
    def __init__(self, date: int)-> None:
        self._validation_pattern = None
        self._error_message = Mess_Attr.MESS_NOT_DAY.value
        self._attr_value = self._validate(date)

    def _validate(self, date: int) -> int:
        if datetime.fromtimestamp(date).date() != datetime.today().date():
            raise VaccineManagementException(Mess_Attr.MESS_NOT_DAY.value)
        return date