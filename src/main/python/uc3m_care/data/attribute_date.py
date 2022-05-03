from datetime import datetime

from uc3m_care.enum.enumerations import MessAttr
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.attribute import Attribute


class Date(Attribute):
    def __init__(self, date: str) -> None:
        super().__init__()
        self._validation_pattern = None
        self._error_message = MessAttr.MESS_NOT_DAY.value
        self._attr_value = self._validate(date)

    def _validate(self, date: str) -> int:
        if datetime.fromtimestamp(float(date)).date() != datetime.today().date():
            raise VaccineManagementException(MessAttr.MESS_NOT_DAY.value)
        return date
