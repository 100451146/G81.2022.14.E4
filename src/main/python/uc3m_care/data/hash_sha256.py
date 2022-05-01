from .attribute import Attribute

class SHA256(Attribute):
    def __init__(self, attr_value):
        """Method for validating sha256 values"""
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._error_message = "date_signature format is not valid"
        self._attr_value = self._validate(attr_value)

    #def _validate(self, attr_value: str) -> str:
    #    """Method for validating uuid  v4"""
    #    try:
    #        super()._validate(attr_value)
    #    except ValueError as value_error:
    #        raise VaccineManagementException("Id received is not a UUID") from value_error
    #    return attr_value
