from uc3m_care import VaccinePatientRegister  # , VaccinationAppoinment
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH, PATIENTS_STORE, APPOINTMENTS_STORE
from uc3m_care.enum.enumerations import Mess_Error, Dict_Data
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage_mangement.json_storage import JsonStore

#  file not found has not gotten any test
class AppointmentsStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_date.json"

    @staticmethod
    def load_patient_file(input_file: str) -> dict:
        """Loads the patient file"""
        try:
            file_data = JsonStore.load_json(input_file)
        except FileNotFoundError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_FILE_NOT_FOUND.value) from exception
        return file_data

    @staticmethod
    def save_vaccination_appointment(date) -> None:  # date: VaccinationAppoinment
        """Saves the appointment into a file"""
        # first read the file
        #data_list = JsonStore.load_from_json(APPOINTMENTS_STORE, False)
        try:
            data_list = JsonStore.load_json(APPOINTMENTS_STORE)
        except FileNotFoundError as exception:
            data_list = []
        # append the date
        data_list.append(date.__dict__)
        JsonStore.save_json_data(data_list, APPOINTMENTS_STORE)

    @staticmethod
    def search_date_appointment(date_signature: str)-> str:
        # check if this date is in store_date
        # first read the file
        #appointments_list = JsonStore.load_from_json(APPOINTMENTS_STORE, is_appointment=True)
        try:
            appointments_list = JsonStore.load_json(APPOINTMENTS_STORE)
        except FileNotFoundError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_STORE_DATE_NOT_FOUND.value) from exception
        # search this date_signature
        found = False
        for item in appointments_list:
            if item[Dict_Data.KEY_LABEL_DATE_SIGNATURE.value] == date_signature:
                found = True
                date_time = item[Dict_Data.KEY_LABEL_DATE_APPOINTMENT_DATE.value]
        if not found:
            raise VaccineManagementException(Mess_Error.ERR_MESS_DATE_NOT_FOUND.value)
        return date_time
