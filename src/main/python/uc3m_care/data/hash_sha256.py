from .attribute import Attribute
from uc3m_care.enum.enumerations import Correct_Pattern, Mess_Attr

class SHA256(Attribute):
    def __init__(self, sha256: str)-> None:
        """Method for validating sha256 values"""
        self._validation_pattern = Correct_Pattern.SHA256_PATTERN.value
        self._error_message = Mess_Attr.MESS_SHA256_INVALID.value
        self._attr_value = self._validate(sha256)

    #def _validate(self, attr_value: str) -> str:
    #    """Method for validating uuid  v4"""
    #    try:
    #        super()._validate(attr_value)
    #    except ValueError as value_error:
    #        raise VaccineManagementException("Id received is not a UUID") from value_error
    #    return attr_value
