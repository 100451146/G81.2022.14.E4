from .attribute import Attribute
from datetime import datetime
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class Date(Attribute):
    def __init__(self, date):
        self._validation_pattern = None
        self._error_message = "Today is not the date"
        self._attr_value = self._validate(date)

    def _validate(self, date: int) -> int:
        if datetime.fromtimestamp(date).date() != datetime.today().date():
            raise VaccineManagementException("Today is not the date")
        return date