import datetime
import json

from uc3m_care import VaccinePatientRegister
from uc3m_care.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.vaccine_management_exception import VaccineManagementException


class JsonStore:
    @staticmethod
    def save_patient_in_storage(json_data: VaccinePatientRegister)-> True:
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
    def save_vaccinated(date_signature):
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