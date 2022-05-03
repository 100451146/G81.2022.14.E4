import re
from datetime import datetime
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class VaccineLog:
    def __init__(self, date_signature):
        self.validate_date_signature(date_signature)
        self.__date_signature = datetime.utcnow().__str__()

    @staticmethod
    def validate_date_signature(date_signature: str) -> str:
        date_signature_pattern = re.compile(r"[0-9A-fA-F]{64}$")
        result = date_signature_pattern.fullmatch(date_signature)
        if not result:
            raise VaccineManagementException("date_signature format is not valid")
        return date_signature

    @property
    def date_signature(self):
        return self.__date_signature
