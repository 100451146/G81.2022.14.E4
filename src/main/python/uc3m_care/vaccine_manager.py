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


class VaccineManager():
    """Class for providing the methods for managing the vaccination process"""

    @staticmethod
    def validate_date_signature(date_signature: str) -> None:
        """Method for validating sha256 values"""
        signature_pattern = re.compile(r"[0-9a-fA-F]{64}$")
        result = signature_pattern.fullmatch(date_signature)
        if not result:
            raise VaccineManagementException("date_signature format is not valid")

    # pylint: disable=too-many-arguments
    def request_vaccination_id(self, patient_id: str,
                               name_surname: str,
                               registration_type: str,
                               phone_number: str,
                               age: str) -> str:
        """Register the patient into the patients file"""

        my_patient = VaccinePatientRegister(patient_id,
                                            name_surname,
                                            registration_type,
                                            phone_number,
                                            age)

        JsonStore.save_patient_in_storage(my_patient)

        return my_patient.patient_sys_id

    def validate_phone(self, phone_number):
        phone_pattern = re.compile(r"^(\+)[0-9]{11}")
        result = phone_pattern.fullmatch(phone_number)
        if not result:
            raise VaccineManagementException("phone number is not valid")

    def get_vaccine_date(self, input_file):
        """Gets an appointment for a registered patient"""

        data = self.find_patient(input_file)

        guid = self.check_patient_data(data)

        my_sign = VaccinationAppoinment(guid, data["PatientSystemID"], data["ContactPhoneNumber"], 10)

        # save the date in store_date.json
        JsonStore.store_vaccination_date(my_sign)

        return my_sign.date_signature

    def find_patient(self, input_file: str):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            # file is not found
            raise VaccineManagementException("File is not found") from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data

    def check_patient_data(self, patient_data):
        # check all the information
        try:
            sys_id_pattern = re.compile(r"[0-9a-fA-F]{32}$")
            result = sys_id_pattern.fullmatch(patient_data["PatientSystemID"])
            if not result:
                raise VaccineManagementException("patient system id is not valid")
        except KeyError as exception:
            raise VaccineManagementException("Bad label patient_id") from exception

        try:
            self.validate_phone(patient_data["ContactPhoneNumber"])
        except KeyError as exception:
            raise VaccineManagementException("Bad label contact phone") from exception

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

        self.validate_date_signature(date_signature)

        # check if this date is in store_date
        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise VaccineManagementException("Store_date not found") from ex
        # search this date_signature
        found = False
        for item in data_list:
            if item["_VaccinationAppoinment__date_signature"] == date_signature:
                found = True
                date_time = item["_VaccinationAppoinment__appoinment_date"]
        if not found:
            raise VaccineManagementException("date_signature is not found")

        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(date_time).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")

        JsonStore.save_vaccinated(date_signature)
        return True
