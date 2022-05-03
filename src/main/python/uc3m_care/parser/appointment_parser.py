from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.hash_md5 import MD5
from uc3m_care.enum.enumerations import DictData
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import MessAttr


class AppointmentParser:

    class __AppointmentParser:
        @staticmethod
        def validate_phone_label(patient: dict) -> None:
            try:
                PhoneNumber(patient[DictData.KEY_LABEL_PHONE_NUMBER.value])
            except KeyError as exception:
                raise VaccineManagementException(MessAttr.MESS_BAD_LABEL_PHONE.value) from exception

        @staticmethod
        def validate_system_id_label(patient: dict) -> None:
            try:
                MD5(patient[DictData.KEY_LABEL_PATIENT_SYS_ID.value])
            except KeyError as exception:
                raise VaccineManagementException(MessAttr.MESS_BAD_LABEL_PATIENT_ID.value) from exception

    __instance = None

    def __new__(cls):
        if AppointmentParser.__instance is None:
            AppointmentParser.__instance = AppointmentParser.__AppointmentParser
        return AppointmentParser.__instance

    @staticmethod
    def validate_phone_label(patient: dict) -> None:
        if AppointmentParser.__instance is None:
            AppointmentParser.__instance = AppointmentParser.__AppointmentParser
        return AppointmentParser.__instance.validate_phone_label(patient)

    @staticmethod
    def validate_system_id_label(patient: dict) -> None:
        if AppointmentParser.__instance is None:
            AppointmentParser.__instance = AppointmentParser.__AppointmentParser
        return AppointmentParser.__instance.validate_system_id_label(patient)




