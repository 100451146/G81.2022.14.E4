from uc3m_care import VaccinePatientRegister
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH, PATIENTS_STORE
from uc3m_care.enum.enumerations import Mess_Error, Dict_Data
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage_mangement.json_storage import JsonStore


# save patient in storage si no hay storage crea uno vacío
class RegistryStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_patient.json"

    def load_registry():
        """
        Load the registry from the file
        :return:
        """
        file_store_registry = JSON_FILES_PATH + "store_registry.json"
        try:
            data = JsonStore.load_json(RegistryStore._FILE_PATH)
        except FileNotFoundError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_STORE_PATIENT_NOT_FOUND.value) from exception

        return data

    @staticmethod
    def search_patient(patient: dict) -> dict:
        """Method for searching the patient in the store"""
        patient_list = JsonStore.load_json(RegistryStore._FILE_PATH)
        # search this patient
        for item in patient_list:
            if item[Dict_Data.KEY_LABEL_VACC_PATIENT_SYS_ID.value] == patient[Dict_Data.KEY_LABEL_PATIENT_SYS_ID.value]:
                return item
        raise VaccineManagementException(Mess_Error.ERR_MESS_PATIENT_SYSID_NOT_FOUND.value)

    @staticmethod
    def search_patient_on_storage(patient: str) -> dict:
        try:
            patient_found = RegistryStore.search_patient(patient)
        except KeyError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_PATIENT_DATA_MANIPULATED.value) from exception
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
    def check_if_patient_duplicated(data_list: dict, json_data: dict) -> None:
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
