from uc3m_care.enum.enumerations import Mess_Attr, Correct_Pattern
from .attribute import Attribute

class PhoneNumber(Attribute):
    def __init__(self, phone_number: str)-> None:
        self._validation_pattern = Correct_Pattern.PHONE_PATTERN.value
        self._error_message = Mess_Attr.MESS_PHONE_INVALID.value
        self._attr_value = self._validate(phone_number)


        #try:
        #    myregex = re.compile(r"^(\+)[0-9]{11}")
        #    res = myregex.fullmatch(data["ContactPhoneNumber"])
        #    if not res:
        #        raise VaccineManagementException("phone number is not valid")
        #except KeyError as ex:
        #    raise VaccineManagementException("Bad label contact phone") from ex