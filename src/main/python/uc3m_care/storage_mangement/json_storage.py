import datetime
import json

from uc3m_care import VaccinePatientRegister
from uc3m_care.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.cfg.vaccine_manager_config import PATIENTS_STORE, APPOINTMENTS_STORE, VACCINES_STORE
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import Mess_Error, Dict_Data

class JsonStore:

    @staticmethod
    def save_patient_in_storage(json_data: VaccinePatientRegister) -> True:
        """Method for saving the patients store"""
        # first read the file
        data_list = JsonStore.load_from_json(PATIENTS_STORE)

        JsonStore.check_patient_duplicated(data_list, json_data)

        JsonStore.append_json_data(data_list, PATIENTS_STORE)
        return True

    @staticmethod
    def save_vaccination_appointment(date: VaccinationAppoinment) -> None:
        """Saves the appointment into a file"""
        # first read the file
        data_list = JsonStore.load_from_json(APPOINTMENTS_STORE, False)
        # append the date
        data_list.append(date.__dict__)
        JsonStore.append_json_data(data_list, APPOINTMENTS_STORE)

    @staticmethod
    def save_vaccinated(date_signature: str)-> None:
        data_list = JsonStore.load_from_json(VACCINES_STORE, False)
        # append the date
        data_list.extend({date_signature.__str__(), datetime.datetime.utcnow().__str__()})

        JsonStore.append_json_data(data_list, VACCINES_STORE)

    @staticmethod
    def load_from_json(input_file: str, is_registry=False, is_patient_file=False, is_appointment=False)-> dict:
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as exception:
            if is_registry:
                raise VaccineManagementException(Mess_Error.ERR_MESS_STORE_PATIENT_NOT_FOUND.value) from exception
            if is_patient_file:
                raise VaccineManagementException(Mess_Error.ERR_MESS_FILE_NOT_FOUND.value) from exception
            if is_appointment:
                raise VaccineManagementException(Mess_Error.ERR_MESS_STORE_DATE_NOT_FOUND.value) from exception
            data_list = []  # file is not found , so  init my data_list
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_WRONG_JSON_FORMAT.value) from exception
        return data_list

    @staticmethod
    def append_json_data(data_list, file_store: str) -> None:
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_WRONG_FILE.value) from exception

    @staticmethod
    def search_patient(patient: dict) -> dict:
        """Method for searching the patient in the store"""
        patient_list = JsonStore.load_from_json(PATIENTS_STORE, is_registry=True)
        # search this patient
        for item in patient_list:
            if item[Dict_Data.KEY_LABEL_VACC_PATIENT_SYS_ID.value] == patient[Dict_Data.KEY_LABEL_PATIENT_SYS_ID.value]:
                return item
        raise VaccineManagementException(Mess_Error.ERR_MESS_PATIENT_SYSID_NOT_FOUND.value)

    @staticmethod
    def search_date_appointment(date_signature: str)-> str:
        # check if this date is in store_date
        # first read the file
        appointments_list = JsonStore.load_from_json(APPOINTMENTS_STORE, is_appointment=True)
        # search this date_signature
        found = False
        for item in appointments_list:
            if item[Dict_Data.KEY_LABEL_DATE_SIGNATURE.value] == date_signature:
                found = True
                date_time = item[Dict_Data.KEY_LABEL_DATE_APPOINTMENT_DATE.value]
        if not found:
            raise VaccineManagementException(Mess_Error.ERR_MESS_DATE_NOT_FOUND.value)
        return date_time

    @staticmethod
    def check_patient_duplicated(data_list: dict, json_data: dict)-> None:
        key_found = False
        for item in data_list:
            if item[Dict_Data.KEY_LABEL_VACCINE_PATIENT_ID.value] == json_data.patient_id:
                if (item[Dict_Data.KEY_LABEL_VACCINE_REG_TYPE.value] == json_data.vaccine_type) and \
                        (item[Dict_Data.KEY_LABEL_VACCINE_NAME.value] == json_data.full_name):
                    key_found = True
        if key_found is False:
            data_list.append(json_data.__dict__)
        elif key_found is True:
            raise VaccineManagementException(Mess_Error.ERR_MESS_PATIENT_REGISTERED.value)

    @staticmethod
    def found_patient_on_store(patient: str)-> str:
        try:
            patient_found = JsonStore.search_patient(patient)
        except KeyError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_PATIENT_DATA_MANIPULATED.value) from exception
        return patient_found