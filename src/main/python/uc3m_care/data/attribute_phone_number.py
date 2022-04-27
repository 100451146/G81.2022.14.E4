
from .attribute import Attribute

class PhoneNumber(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._error_message = "phone number is not valid"
        self._attr_value = self._validate(attr_value)


        #try:
        #    myregex = re.compile(r"^(\+)[0-9]{11}")
        #    res = myregex.fullmatch(data["ContactPhoneNumber"])
        #    if not res:
        #        raise VaccineManagementException("phone number is not valid")
        #except KeyError as ex:
        #    raise VaccineManagementException("Bad label contact phone") from ex