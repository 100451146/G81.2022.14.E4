"""Module """
import datetime
from datetime import datetime
from freezegun import freeze_time

from .parser.appointment_parser import AppointmentParser
from .storage_mangement.appointments_storage import AppointmentsStore
from .storage_mangement.registry_storage import RegistryStore
from .storage_mangement.vaccinated_storage import VaccinationStorage
from .vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment
from uc3m_care.data.attribute_date import Date
from uc3m_care.data.hash_sha256 import SHA256
from uc3m_care.data.hash_md5 import MD5
from uc3m_care.enum.enumerations import Dict_Data


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=too-many-arguments
    @staticmethod
    def request_vaccination_id(patient_id: str,
                               name_surname: str,
                               registration_type: str,
                               phone_number: str,
                               age: str) -> str:
        my_patient = VaccinePatientRegister(patient_id,
                                            name_surname,
                                            registration_type,
                                            phone_number,
                                            age)

        RegistryStore.save_patient_in_storage(my_patient)

        return my_patient.patient_sys_id

    def get_vaccine_date(self, input_file):
        """Gets an appointment for a registered patient"""

        patient = AppointmentsStore.load_patient_file(input_file)

        AppointmentParser.validate_system_id_label(patient)
        AppointmentParser.validate_phone_label(patient)

        patient_found = RegistryStore.search_patient_on_storage(patient)

        patient_guid = self.check_patient_data(patient, patient_found)
        my_sign = VaccinationAppoinment(patient_guid, patient[Dict_Data.KEY_LABEL_PATIENT_SYS_ID.value],
                                        patient[Dict_Data.KEY_LABEL_PHONE_NUMBER.value], 10)
        # save the date in store_date.json
        AppointmentsStore.save_vaccination_appointment(my_sign)
        return my_sign.date_signature

    @staticmethod
    def vaccine_patient(date_signature: str) -> True:
        """Register the vaccination of the patient"""

        SHA256(date_signature)
        vaccination_time = AppointmentsStore.search_date_appointment(date_signature)
        Date(vaccination_time)
        # JsonStore.save_vaccinated(date_signature)
        VaccinationStorage.save_vaccinated(date_signature)
        return True

    @staticmethod
    def check_patient_data(patient_from_input: dict, patient_from_storage: dict) -> str:
        guid = patient_from_storage["_VaccinePatientRegister__patient_id"]
        name = patient_from_storage["_VaccinePatientRegister__full_name"]
        reg_type = patient_from_storage["_VaccinePatientRegister__registration_type"]
        phone = patient_from_storage["_VaccinePatientRegister__phone_number"]
        patient_timestamp = patient_from_storage["_VaccinePatientRegister__time_stamp"]
        age = patient_from_storage["_VaccinePatientRegister__age"]
        # set the date when the patient was registered for checking the md5
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
        freezer.stop()
        if patient.patient_system_id != patient_from_input[Dict_Data.KEY_LABEL_PATIENT_SYS_ID.value]:
            raise VaccineManagementException("Patient's data have been manipulated")
        return guid
