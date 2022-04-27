import datetime
import json

from uc3m_care import VaccinePatientRegister
from uc3m_care.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class JsonStore:
    @staticmethod
    def save_patient_in_storage(json_data: VaccinePatientRegister) -> True:
        """Method for saving the patients store"""
        file_store = JSON_FILES_PATH + "store_patient.json"
        # first read the file
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

        key_found = False
        for item in data_list:
            if item["_VaccinePatientRegister__patient_id"] == json_data.patient_id:
                if (item["_VaccinePatientRegister__registration_type"] == json_data.vaccine_type) and \
                         (item["_VaccinePatientRegister__full_name"] == json_data.full_name):
                    key_found = True

        if key_found is False:
            data_list.append(json_data.__dict__)

        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

        if key_found is True:
            raise VaccineManagementException("patien_id is registered in store_patient")
        return True

    @staticmethod
    def store_vaccination_date(date: VaccinationAppoinment) -> None:
        """Saves the appointment into a file"""
        file_store_date = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(file_store_date, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

        # append the date
        data_list.append(date.__dict__)

        try:
            with open(file_store_date, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

    @staticmethod
    def save_vaccinated(date_signature: str):
        file_store_vaccine = JSON_FILES_PATH + "store_vaccine.json"
        try:
            with open(file_store_vaccine, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

            # append the date
        data_list.append(date_signature.__str__())
        data_list.append(datetime.datetime.utcnow().__str__())
        try:
            with open(file_store_vaccine, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise VaccineManagementException("Wrong file or file path") from ex

    @staticmethod
    def save_fast(json_data: VaccinePatientRegister) -> None:
        """Method for saving the patients store"""
        patients_store = JSON_FILES_PATH + "store_patient.json"
        with open(patients_store, "r+", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
            data_list.append(json_data.__dict__)
            file.seek(0)
            json.dump(data_list, file, indent=2)

    @staticmethod
    def load_patient(input_file: str):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            # file is not found
            raise VaccineManagementException("File is not found") from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data

    @staticmethod
    def search_patient(patient: dict) -> dict:
        """Method for searching the patient in the store"""
        patients_store = JSON_FILES_PATH + "store_patient.json"
        try:
            with open(patients_store, "r", encoding="utf-8", newline="") as file:
                patient_list = json.load(file)
        except FileNotFoundError as ex:
            raise VaccineManagementException("Store_patient not found") from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # search this patient
        for item in patient_list:
            if item["_VaccinePatientRegister__patient_sys_id"] == patient["PatientSystemID"]:
                return item
        raise VaccineManagementException("patient_system_id is not found")

    @staticmethod
    def search_date_appointment(date_signature: str):
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
        return date_time


