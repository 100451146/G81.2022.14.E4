from uc3m_care.data.attribute_phone_number import PhoneNumber
from uc3m_care.data.hash_md5 import MD5
from uc3m_care.enum.enumerations import Dict_Data
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class AppointmentParser:
    @staticmethod
    def validate_phone_label(patient):
        try:
            PhoneNumber(patient[Dict_Data.KEY_LABEL_PHONE_NUMBER.value])
        except KeyError as exception:
            raise VaccineManagementException("Bad label contact phone") from exception

    @staticmethod
    def validate_system_id_label(patient):
        try:
            MD5(patient[Dict_Data.KEY_LABEL_PATIENT_SYS_ID.value])
        except KeyError as exception:
            raise VaccineManagementException("Bad label patient_id") from exception