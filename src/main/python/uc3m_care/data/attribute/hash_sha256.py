from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.enum.enumerations import CorrectPattern, MessAttr


class SHA256(Attribute):
    def __init__(self, sha256: str) -> None:
        """Method for validating sha256 values"""
        super().__init__()
        self._validation_pattern = CorrectPattern.SHA256_PATTERN.value
        self._error_message = MessAttr.MESS_SHA256_INVALID.value
        self._attr_value = self._validate(sha256)

    # def _validate(self, attr_value: str) -> str:
    #    """Method for validating uuid  v4"""
    #    try:
    #        super()._validate(attr_value)
    #    except ValueError as value_error:
    #        raise VaccineManagementException("Id received is not a UUID") from value_error
    #    return attr_value
