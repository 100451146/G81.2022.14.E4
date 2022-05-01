"""Module """
import datetime
from datetime import datetime
from freezegun import freeze_time

from uc3m_care.storage_mangement.json_storage import JsonStore
from .vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment
from uc3m_care.data.attribute_date import Date
from uc3m_care.data.hash_sha256 import SHA256
from uc3m_care.data.hash_md5 import MD5
from uc3m_care.data.attribute_phone_number import PhoneNumber


class VaccineManager():
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=too-many-arguments
    def request_vaccination_id(self, patient_id: str,
                               name_surname: str,
                               registration_type: str,
                               phone_number: str,
                               age: str) -> str:

        my_patient = VaccinePatientRegister(patient_id,
                                            name_surname,
                                            registration_type,
                                            phone_number,
                                            age)

        JsonStore.save_patient_in_storage(my_patient)

        return my_patient.patient_sys_id

    def get_vaccine_date(self, input_file):
        """Gets an appointment for a registered patient"""

        patient = JsonStore.load_from_json(input_file, is_patient_file=True)

        self.validate_system_id_label(patient)
        self.validate_phone_label(patient)

        patient_found = JsonStore.found_patient_on_store(patient)

        patient_guid = self.check_patient_data(patient, patient_found)
        my_sign = VaccinationAppoinment(patient_guid, patient["PatientSystemID"], patient["ContactPhoneNumber"], 10)
        # save the date in store_date.json
        JsonStore.save_vaccination_appointment(my_sign)
        return my_sign.date_signature

    def found_patient(self, patient):
        try:
            patient_found = JsonStore.search_patient(patient)
        except KeyError as exception:
            raise VaccineManagementException("Patient's data have been manipulated") from exception
        return patient_found

    def vaccine_patient(self, date_signature):
        """Register the vaccination of the patient"""

        SHA256(date_signature)

        vaccination_time = JsonStore.search_date_appointment(date_signature)

        Date(vaccination_time)

        JsonStore.save_vaccinated(date_signature)

        return True

    def validate_phone_label(self, patient):
        try:
            PhoneNumber(patient["ContactPhoneNumber"])
        except KeyError as exception:
            raise VaccineManagementException("Bad label contact phone") from exception

    def validate_system_id_label(self, patient):
        try:
            MD5(patient["PatientSystemID"])
        except KeyError as exception:
            raise VaccineManagementException("Bad label patient_id") from exception

    def check_patient_data(self, patient_from_input:dict, patient_from_storage:dict):
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
        if patient.patient_system_id != patient_from_input["PatientSystemID"]:
            raise VaccineManagementException("Patient's data have been manipulated")
        return guid