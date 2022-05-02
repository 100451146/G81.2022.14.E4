from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.enum.enumerations import Mess_Error
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage_mangement.json_storage import JsonStore


class RegistryStore(JsonStore):
    def load_registry():
        """
        Load the registry from the file
        :return:
        """
        file_store_registry = JSON_FILES_PATH + "store_registry.json"
        try:
            data = JsonStore.load_json(file_store_registry)
        except FileNotFoundError as exception:
            raise VaccineManagementException(Mess_Error.ERR_MESS_STORE_PATIENT_NOT_FOUND.value) from exception

        return data




