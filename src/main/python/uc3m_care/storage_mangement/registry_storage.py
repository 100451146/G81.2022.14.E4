from uc3m_care import VaccinePatientRegister
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.enum.enumerations import MessError, DictData
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage_mangement.json_storage import JsonStore


# save patient in storage, if non-existent, create new file
class RegistryStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_patient.json"

    class __RegistryStore(JsonStore):
        @staticmethod
        def load_registry():
            """
            Load the registry from the file
            :return:
            """
            try:
                data = JsonStore.load_json(RegistryStore._FILE_PATH)
            except FileNotFoundError as exception:
                raise VaccineManagementException(MessError.ERR_MESS_STORE_PATIENT_NOT_FOUND.value) from exception
            return data

        @staticmethod
        def search_patient(patient: dict) -> dict:
            """Method for searching the patient in the store"""
            patient_list = JsonStore.load_json(RegistryStore._FILE_PATH)
            # search this patient
            for item in patient_list:
                if item[DictData.KEY_LABEL_VACC_PATIENT_SYS_ID.value] == patient[DictData.KEY_LABEL_PATIENT_SYS_ID.value]:
                    return item
            raise VaccineManagementException(MessError.ERR_MESS_PATIENT_SYSID_NOT_FOUND.value)

        @staticmethod
        def search_patient_on_storage(patient: dict) -> dict:
            try:
                patient_found = RegistryStore.search_patient(patient)
            except KeyError as exception:
                raise VaccineManagementException(MessError.ERR_MESS_PATIENT_DATA_MANIPULATED.value) from exception
            return patient_found

        @staticmethod
        def save_patient_in_storage(json_data: VaccinePatientRegister) -> True:
            """Method for saving the patients store"""
            # first read the file
            try:
                data_list = JsonStore.load_json(RegistryStore._FILE_PATH)
            except FileNotFoundError:
                data_list = []

            RegistryStore.check_if_patient_duplicated(data_list, json_data)

            JsonStore.save_json_data(data_list, RegistryStore._FILE_PATH)
            return True

        @staticmethod
        def check_if_patient_duplicated(data_list: dict, json_data: VaccinePatientRegister) -> None:
            key_found = False
            for item in data_list:
                if item[DictData.KEY_LABEL_VACCINE_PATIENT_ID.value] == json_data.patient_id:
                    if (item[DictData.KEY_LABEL_VACCINE_REG_TYPE.value] == json_data.vaccine_type) and \
                            (item[DictData.KEY_LABEL_VACCINE_NAME.value] == json_data.full_name):
                        key_found = True
            if key_found is False:
                data_list.append(json_data.__dict__)
            elif key_found is True:
                raise VaccineManagementException(MessError.ERR_MESS_PATIENT_REGISTERED.value)

    __is_instance = None

    def __new__(cls):
        if not cls.__is_instance:
            cls.__is_instance = super(RegistryStore, cls).__new__(cls)
        return cls.__is_instance

    @staticmethod
    def load_registry():
        if RegistryStore.__is_instance is None:
            RegistryStore.__is_instance = RegistryStore.__RegistryStore()
        return RegistryStore.__is_instance.load_registry()

    @staticmethod
    def search_patient(patient: dict) -> dict:
        if RegistryStore.__is_instance is None:
            RegistryStore.__is_instance = RegistryStore.__RegistryStore()
        return RegistryStore.__is_instance.search_patient(patient)

    @staticmethod
    def search_patient_on_storage(patient: dict) -> dict:
        if RegistryStore.__is_instance is None:
            RegistryStore.__is_instance = RegistryStore.__RegistryStore()
        return RegistryStore.__is_instance.search_patient_on_storage(patient)

    @staticmethod
    def save_patient_in_storage(json_data: VaccinePatientRegister) -> True:
        if RegistryStore.__is_instance is None:
            RegistryStore.__is_instance = RegistryStore.__RegistryStore()
        return RegistryStore.__is_instance.save_patient_in_storage(json_data)

    @staticmethod
    def check_if_patient_duplicated(data_list: dict, json_data: VaccinePatientRegister) -> None:
        if RegistryStore.__is_instance is None:
            RegistryStore.__is_instance = RegistryStore.__RegistryStore()
        return RegistryStore.__is_instance.check_if_patient_duplicated(data_list, json_data)
