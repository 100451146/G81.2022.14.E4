from .attribute import Attribute
from datetime import datetime
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class Date(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = None
        self._error_message = "Today is not the date"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value: int) -> int:
        if datetime.fromtimestamp(attr_value).date() != datetime.today().date():
            raise VaccineManagementException("Today is not the date")
        return attr_value