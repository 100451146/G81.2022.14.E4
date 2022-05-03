"""Contains the class Vaccination Appointment"""
import hashlib
from datetime import datetime
from freezegun import freeze_time

from uc3m_care import VaccinePatientRegister
from uc3m_care.data.hash_md5 import MD5
from uc3m_care.data.hash_guid4 import Uuid
from uc3m_care.data.attribute_phone_number import PhoneNumber


# pylint: disable=too-many-instance-attributes
from uc3m_care.enum.enumerations import DictData, MessError
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.parser.appointment_parser import AppointmentParser
from uc3m_care.storage_mangement.appointments_storage import AppointmentsStore
from uc3m_care.storage_mangement.registry_storage import RegistryStore


class VaccinationAppoinment:
    """Class representing an appointment  for the vaccination of a patient"""
    def __init__(self, input_file):
        """Initializes the class"""
        self.__patient = AppointmentsStore.load_patient_file(input_file)
        AppointmentParser.validate_system_id_label(self.__patient)
        AppointmentParser.validate_phone_label(self.__patient)
        self.__patient_found = RegistryStore.search_patient_on_storage(self.__patient)
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_id = self.check_patient_data_signature(self.__patient, self.__patient_found)
        self.__patient_sys_id = MD5(self.__patient[DictData.KEY_LABEL_PATIENT_SYS_ID.value]).value
        self.__phone_number = PhoneNumber(self.__patient[DictData.KEY_LABEL_PHONE_NUMBER.value]).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        days = 10
        if days == 0:
            self.__appoinment_date = 0
        else:
            # timestamp is represented in seconds.microseconds
            # age must be expressed in seconds to be added to the timestamp
            self.__appoinment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appoinment_date.__str__() + "}"

    @property
    def patient_id(self):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = Uuid(value).value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id

    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = MD5(value).value

    @property
    def phone_number(self):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def appoinment_date(self):
        """Returns the vaccination date"""
        return self.__appoinment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    @staticmethod
    def check_patient_data_signature(patient_from_input: dict, patient_from_storage: dict) -> str:
        guid = patient_from_storage[DictData.KEY_LABEL_VACCINE_PATIENT_ID.value]
        name = patient_from_storage[DictData.KEY_LABEL_VACCINE_NAME.value]
        reg_type = patient_from_storage[DictData.KEY_LABEL_VACCINE_REG_TYPE.value]
        phone = patient_from_storage[DictData.KEY_LABEL_VACCINE_PATIENT_PHONE.value]
        patient_timestamp = patient_from_storage[DictData.KEY_LABEL_TIME.value]
        age = patient_from_storage[DictData.KEY_LABEL_AGE.value]
        # set the date when the patient was registered for checking the md5
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
        freezer.stop()
        if patient.patient_system_id != patient_from_input[DictData.KEY_LABEL_PATIENT_SYS_ID.value]:
            raise VaccineManagementException(MessError.ERR_MESS_PATIENT_DATA_MANIPULATED.value)
        return guid
