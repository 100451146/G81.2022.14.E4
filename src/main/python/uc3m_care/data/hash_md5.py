from .attribute import Attribute
from uc3m_care.enum.enumerations import Correct_Pattern, Mess_Attr

class MD5(Attribute):
    def __init__(self, md5: str)-> None:
        """Method for validating sha256 values"""
        self._validation_pattern = Correct_Pattern.MD5_PATTERN.value
        self._error_message = Mess_Attr.MESS_MD5_INVALID.value
        self._attr_value = self._validate(md5)



        #try:
        #    sys_id_pattern = re.compile(r"[0-9a-fA-F]{32}$")
        #    result = sys_id_pattern.fullmatch(patient_data["PatientSystemID"])
        #    if not result:
        #        raise VaccineManagementException("patient system id is not valid")
        #except KeyError as exception:
        #    raise VaccineManagementException("Bad label patient_id") from exception



    #def _validate(self, attr_value: str) -> str:
    #    """Method for validating uuid  v4"""
    #    try:
    #        super()._validate(attr_value)
    #    except ValueError as value_error:
    #        raise VaccineManagementException("Id received is not a UUID") from value_error
    #    return attr_value
