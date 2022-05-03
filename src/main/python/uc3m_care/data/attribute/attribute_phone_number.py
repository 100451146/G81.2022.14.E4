from uc3m_care.enum.enumerations import MessAttr, CorrectPattern
from uc3m_care.data.attribute.attribute import Attribute


class PhoneNumber(Attribute):
    def __init__(self, phone_number: str) -> None:
        super().__init__()
        self._validation_pattern = CorrectPattern.PHONE_PATTERN.value
        self._error_message = MessAttr.MESS_PHONE_INVALID.value
        self._attr_value = self._validate(phone_number)

        # try:
        #    regex = re.compile(r"^(\+)[0-9]{11}")
        #    res = regex.full match(data["ContactPhoneNumber"])
        #    if not res:
        #        raise VaccineManagementException("phone number is not valid")
        # except KeyError as ex:
        #    raise VaccineManagementException("Bad label contact phone") from ex
