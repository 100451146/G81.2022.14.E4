"""Module """
import datetime
import re
import json
from datetime import datetime
from freezegun import freeze_time

from .json_storage import JsonStore
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.data.attribute_sha256 import SHA256
from uc3m_care.data.md5 import MD5
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

        patient = JsonStore.load_patient(input_file)

        try:
            MD5(patient["PatientSystemID"])
        except KeyError as exception:
            raise VaccineManagementException("Bad label patient_id") from exception

        try:
            PhoneNumber(patient["ContactPhoneNumber"])
        except KeyError as exception:
            raise VaccineManagementException("Bad label contact phone") from exception

        try:
            patient_found = JsonStore.search_patient(patient)
        except KeyError as exception:
            raise VaccineManagementException("Patient's data have been manipulated") from exception

        #if patient_found is None:
        #    raise VaccineManagementException("patient_sys_id not found")

        patient_guid = self.check_patient_data(patient)

        my_sign = VaccinationAppoinment(patient_guid, patient["PatientSystemID"], patient["ContactPhoneNumber"], 10)

        # save the date in store_date.json
        JsonStore.store_vaccination_date(my_sign)

        return my_sign.date_signature

    def check_patient_data(self, patient_data):

        file_store = JSON_FILES_PATH + "store_patient.json"
        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)

        found_key = False
        for item in data_list:
            if item["_VaccinePatientRegister__patient_sys_id"] == patient_data["PatientSystemID"]:
                found_key = True
                # retrieve the patients data
                guid = item["_VaccinePatientRegister__patient_id"]
                name = item["_VaccinePatientRegister__full_name"]
                reg_type = item["_VaccinePatientRegister__registration_type"]
                phone = item["_VaccinePatientRegister__phone_number"]
                patient_timestamp = item["_VaccinePatientRegister__time_stamp"]
                age = item["_VaccinePatientRegister__age"]
                # set the date when the patient was registered for checking the md5
                freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
                freezer.start()
                patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
                freezer.stop()
                if patient.patient_system_id != patient_data["PatientSystemID"]:
                    raise VaccineManagementException("Patient's data have been manipulated")

        if not found_key:
            raise VaccineManagementException("patient_system_id not found")
        return guid

    def vaccine_patient(self, date_signature):
        """Register the vaccination of the patient"""

        #self.validate_date_signature(date_signature)
        SHA256(date_signature)

        vaccination_time = JsonStore.search_date_appointment(date_signature)

        if datetime.fromtimestamp(vaccination_time).date() != datetime.today().date():
            raise VaccineManagementException("Today is not the date")

        JsonStore.save_vaccinated(date_signature)
        return True
