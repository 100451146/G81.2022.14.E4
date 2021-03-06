from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.enum.enumerations import MessError, DictData
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage_mangement.json_storage import JsonStore


#  file not found has not gotten any test
class AppointmentsStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_date.json"

    class __AppointmentsStore(JsonStore):
        @staticmethod
        def load_patient_file(input_file: str) -> dict:
            """Loads the patient file"""
            try:
                file_data = JsonStore.load_json(input_file)
            except FileNotFoundError as exception:
                raise VaccineManagementException(MessError.ERR_MESS_FILE_NOT_FOUND.value) from exception
            return file_data

        @staticmethod
        def save_vaccination_appointment(date) -> None:  # date: VaccinationAppointment
            """Saves the appointment into a file"""
            # first read the file
            # data_list = JsonStore.load_from_json(APPOINTMENTS_STORE, False)
            try:
                data_list = JsonStore.load_json(AppointmentsStore._FILE_PATH)
            except FileNotFoundError:
                data_list = []
            # append the date
            data_list.append(date.__dict__)
            JsonStore.save_json_data(data_list, AppointmentsStore._FILE_PATH)

        @staticmethod
        def search_date_appointment(date_signature: str) -> str:
            # check if this date is in store_date
            # first read the file
            # appointments_list = JsonStore.load_from_json(APPOINTMENTS_STORE, is_appointment=True)
            try:
                appointments_list = JsonStore.load_json(AppointmentsStore._FILE_PATH)
            except FileNotFoundError as exception:
                raise VaccineManagementException(MessError.ERR_MESS_STORE_DATE_NOT_FOUND.value) from exception
            # search this date_signature
            found = False
            date_time = None
            for item in appointments_list:
                if item[DictData.KEY_LABEL_DATE_SIGNATURE.value] == date_signature:
                    found = True
                    date_time = item[DictData.KEY_LABEL_DATE_APPOINTMENT_DATE.value]
            if not found:
                raise VaccineManagementException(MessError.ERR_MESS_DATE_NOT_FOUND.value)
            return date_time

    __is_instance = None

    def __new__(cls):
        if AppointmentsStore.__is_instance is None:
            AppointmentsStore.__is_instance = AppointmentsStore.__AppointmentsStore()
        return AppointmentsStore.__is_instance

    @staticmethod
    def load_patient_file(input: str) -> dict:
        if AppointmentsStore.__is_instance is None:
            AppointmentsStore.__is_instance = AppointmentsStore.__AppointmentsStore()
        return AppointmentsStore.__is_instance.load_patient_file(input)

    @staticmethod
    def save_vaccination_appointment(date: str) -> None:
        if AppointmentsStore.__is_instance is None:
            AppointmentsStore.__is_instance = AppointmentsStore.__AppointmentsStore()
        return AppointmentsStore.__is_instance.save_vaccination_appointment(date)

    @staticmethod
    def search_date_appointment(date_signature: str) -> str:
        if AppointmentsStore.__is_instance is None:
            AppointmentsStore.__is_instance = AppointmentsStore.__AppointmentsStore()
        return AppointmentsStore.__is_instance.search_date_appointment(date_signature)

    _FILE_PATH = JSON_FILES_PATH + "store_date.json"
